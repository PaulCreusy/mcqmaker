
import sys

sys.path.append(".")

import random
from lxml import etree
import shutil
from mcq_maker_tools.tools_class import *
from mcq_maker_tools.tools_docx import *

### QCM functions ###

def generate_QCM(config, class_content, progress_bar=None):
    """
    Generate the QCM data to then export it in the selected format.

    Parameters
    ----------
    config : dict
        Configuration dictionnary under the following form :
        {
            "QCM_name": str,
            "questions":
                [
                    {"folder_name": str, "file_name": str, "nb_questions": int},
                ],
            "template": str,
            "mix_all_questions": bool,
            "mix_among_databases": bool
        }

    progress_bar
        Kivy progress bar to update it on the interface.

    Returns
    -------
    dict
        QCM data under the following form :
        {
            "QCM_name": str,
            "questions": [
                {"question": str, "options": list, "answer": int}
            ]
        }
    """

    # Extract information from the config dict
    mix_all_questions = config["mix_all_questions"]
    mix_among_databases = config["mix_among_databases"]
    instructions = config["questions"]

    # Initialise data structures
    questions_sublists = []
    questions = []
    QCM_data = {}
    QCM_data["QCM_name"] = config["QCM_name"]
    QCM_data["template"] = config["template"]

    # Error boolean
    error_detected = False
    l_error_files = []

    # Build sublist of questions
    for i in range(len(instructions)):

        # Load the data
        current_dict = instructions[i]
        folder = current_dict["folder_name"].replace("\n", " ")
        file = current_dict["file_name"].replace("\n", " ")
        nb_questions = current_dict["nb_questions"]
        database_questions, error_list = load_database(file, folder)

        if len(error_list) > 0:
            error_detected = True
            l_error_files.append(folder + "/" + file)

        # Remove already selected questions
        if (folder, file) in class_content:
            used_questions_list = class_content[(
                folder, file)]["list_questions_used"]
            used_questions_list = sorted(used_questions_list)[::-1]
            for question_id in used_questions_list:
                database_questions.pop(question_id)

        # Mix if needed
        if mix_among_databases:
            selected_questions_id = random.sample(
                [j for j in range(len(database_questions))], nb_questions)
        else:
            selected_questions_id = [i for i in range(
                len(database_questions))][:nb_questions]

        # Insert the selected questions in the class content
        if (folder, file) in class_content:
            class_content[(folder, file)
                          ]["list_questions_used"] += selected_questions_id
            class_content[(folder, file)
                          ]["used_questions"] += len(selected_questions_id)
        else:
            class_content[(folder, file)] = {
                "list_questions_used": selected_questions_id, "used_questions": len(selected_questions_id)}

        # Extract the questions using the id
        selected_questions = [database_questions[j]
                              for j in selected_questions_id]

        # Insert inside the list
        questions_sublists.append(selected_questions)

    if error_detected:
        return None, l_error_files

    # Merge all sublists into a single one
    for sublist in questions_sublists:
        questions += sublist

    # Mix all questions if the option is selected
    if mix_all_questions:
        random.shuffle(questions)

    # Insert data inside the dict
    QCM_data["questions"] = questions

    return QCM_data, class_content

def create_folder_QCM(QCM_data):
    QCM_name = QCM_data["QCM_name"]
    folder_path = SETTINGS["path_export"] + QCM_name
    new_folder_path = folder_path
    i = 1
    while os.path.exists(new_folder_path):
        new_folder_path = folder_path + "_" + str(i)
        i += 1

    os.mkdir(new_folder_path)

    return new_folder_path + "/"


def export_QCM_txt(QCM_data, folder_path, progress_bar):
    """
    Export the QCM and its solution in a .txt file.

    Parameters
    ----------
    QCM_data : dict
        Data to generate the QCM under the following form :
        {
            "QCM_name": str,
            "questions": [
                {"question": str, "options": list, "answer": int}
            ]
        }

    progress_bar
        Kivy progress bar to update it on the interface.

    Returns
    -------
    None
    """

    # Build the path of the files
    QCM_path = folder_path + QCM_data["QCM_name"] + ".txt"
    solution_path = folder_path + QCM_data["QCM_name"] + "_solution.txt"

    # Open the files
    QCM_file = open(QCM_path, "w", encoding="utf-8")
    solution_file = open(solution_path, "w", encoding="utf-8")

    # Extract information from the dictionnary
    QCM_name = QCM_data["QCM_name"]
    questions = QCM_data["questions"]

    # Write the first lines
    solution_file.write(QCM_name + "\n\n")
    solution_file.write("Id de la question\tBonne reponse\n")
    QCM_file.write(QCM_name + "\n\n")
    QCM_file.write("Nom : " + " " * 20 + "Prénom : " + " " * 20 + "\n")
    QCM_file.write("Classe :\n\n")

    progress_bar.value = 3
    number_questions = len(questions)

    # Scan the list of questions
    for i in range(number_questions):

        # Extract the data
        question_dict = questions[i]
        question = question_dict["question"]
        options = question_dict["options"]
        answer = question_dict["answer"]

        # Write the current question
        QCM_file.write(f"{str(i+1)}. {question}\n")
        for j in range(len(options)):
            QCM_file.write(f"\t{convert_int_to_letter(j)}) {options[j]}")
        QCM_file.write("\n\n")

        # Write the solution
        solution_file.write(f"{i}\t{convert_int_to_letter(answer)}\n")

        # Update the value of the progress bar
        progress_bar.value += 17 / number_questions


def export_QCM_docx(QCM_data, folder_path, template, progress_bar):

    # Create the file object with the selected template
    QCM_file = Document(PATH_TEMPLATE_FOLDER + template + ".docx")

    # Replace the name of the MCQ
    replace_in_doc(QCM_file, "{NAME_MCQ}", QCM_data["QCM_name"])

    # Detect the id of the paragraph where the list of questions starts
    begin_para, begin_para_idx = find_paragraph(
        QCM_file, "### LIST_QUESTIONS_START ###")
    end_para, end_para_idx = find_paragraph(
        QCM_file, "### LIST_QUESTIONS_END ###")

    # Store in a list all paragraphs composing a question to dupplicate them
    para_list = []
    for i in range(begin_para_idx + 1, end_para_idx):
        para_list.append(QCM_file.paragraphs[i])

    copy_para_list = deepcopy(para_list)

    # Raise error if no paragraph is found
    if begin_para is None or end_para is None:
        raise ValueError(
            "The selected template does not include a list of question area.")

    progress_bar.value = 23

    nb_questions = len(QCM_data["questions"])

    # Add the questions to the document
    for (i, question_dict) in enumerate(QCM_data["questions"]):
        if i > 0:
            # Do a copy of the list to create the new paragraphs
            para_list = deepcopy(copy_para_list)
            for (j, para) in enumerate(para_list):
                new_para = para._p
                QCM_file.paragraphs[end_para_idx]._p.addnext(new_para)
                end_para_idx += 1

        # Replace the id and the question
        replace_in_doc(QCM_file, "{ID_QUESTION}", str(i + 1))
        replace_in_doc(QCM_file, "{QUESTION}", question_dict["question"])

        # Locate the paragraph containing the list of options
        options = question_dict["options"]
        options_para, end_para_idx = find_paragraph(QCM_file, "{LIST_OPTIONS}")
        copy_options_para = deepcopy(options_para)

        # Add the first option
        replace_in_doc(QCM_file, "{LIST_OPTIONS}",
                       convert_int_to_letter(0) + ". " + options[0])

        # Dupplicate the paragraph to add the answers
        nb_answers = len(options)
        for j in range(1, nb_answers):

            new_copy_options_para = deepcopy(copy_options_para)

            # Dupplicate the list options
            new_para = copy_options_para._p
            QCM_file.paragraphs[end_para_idx]._p.addnext(new_para)

            # Replace it with the current option
            replace_in_doc(QCM_file, "{LIST_OPTIONS}",
                           convert_int_to_letter(j) + ". " + options[j])

            copy_options_para = new_copy_options_para

            end_para_idx += 1

        progress_bar.value += 15 / nb_questions

    delete_indications(QCM_file)

    QCM_file.save(folder_path + QCM_data["QCM_name"] + ".docx")

    progress_bar.value = 40

def export_QCM_H5P_single_choice(QCM_data, folder_path, progress_bar):
    """
    Export the QCM and its solution in a .h5p file for sinle choice H5P integration.

    Parameters
    ----------
    QCM_data : dict
        Data to generate the QCM under the following form :
        {
            "QCM_name": str,
            "questions": [
                {"question": str, "options": list, "answer": int}
            ]
        }

    progress_bar
        Kivy progress bar to update it on the interface.

    Returns
    -------
    None
    """

    # Define the path of the export folder
    folder_path = folder_path + QCM_data["QCM_name"] + "_single_choice"

    # Copy the template folder
    if not os.path.exists(folder_path):
        shutil.copytree(PATH_SINGLE_CHOICE_H5P_FOLDER, folder_path)

    # Create the content dict
    content_dict = {
        "choices": [],
        "behaviour": {
            "timeoutCorrect": 1000,
            "timeoutWrong": 1000,
            "soundEffectsEnabled": True,
            "enableRetry": True,
            "enableSolutionsButton": True,
            "passPercentage": 100,
            "autoContinue": True
        },
        "l10n": {
            "showSolutionButtonLabel": "Show solution",
            "retryButtonLabel": "Retry",
            "solutionViewTitle": "Solution",
            "correctText": "Correct!",
            "incorrectText": "Incorrect!",
            "muteButtonLabel": "Mute feedback sound",
            "closeButtonLabel": "Close",
            "slideOfTotal": "Slide :num of :total",
            "nextButtonLabel": "Next question",
            "scoreBarLabel": "You got :num out of :total points",
            "solutionListQuestionNumber": "Question :num",
            "a11yShowSolution": "Show the solution. The task will be marked with its correct solution.",
            "a11yRetry": "Retry the task. Reset all responses and start the task over again.",
            "shouldSelect": "Should have been selected",
            "shouldNotSelect": "Should not have been selected"
        },
        "overallFeedback": [
            {
                "from": 0,
                "to": 100,
                "feedback": "You got :numcorrect of :maxscore correct"
            }
        ]}

    progress_bar.value = 43
    nb_questions = len(QCM_data["questions"])

    # Store the questions inside
    for (i, question_dict) in enumerate(QCM_data["questions"]):

        # Put the answer in first position
        answer_id = question_dict["answer"]
        crossed_list = [(i != answer_id, e)
                        for (i, e) in enumerate(question_dict["options"])]
        crossed_list = sorted(crossed_list)
        options_list = [e[1] for e in crossed_list]

        # Put the content inside the dict
        store_dict = {}
        store_dict["subContentId"] = str(i + 1)
        store_dict["question"] = question_dict["question"]
        store_dict["answers"] = options_list

        content_dict["choices"].append(store_dict)

        progress_bar.value += 15 / nb_questions

    # Create the json file
    save_json_file(folder_path + "/content/content.json", content_dict)

    # Zip the folder
    shutil.make_archive(folder_path, 'zip', folder_path)

    # Remove the file if it already exists
    if os.path.exists(folder_path + ".h5p"):
        os.remove(folder_path + ".h5p")

    # Rename the file to have the .h5p extension
    os.rename(folder_path + ".zip", folder_path + ".h5p")

    # Remove the construction folder
    shutil.rmtree(folder_path)

    progress_bar.value = 60

def export_QCM_H5P_text_single_choice(QCM_data, folder_path, progress_bar):
    """
    Export the QCM and its solution in a .h5p file for sinle choice H5P integration.

    Parameters
    ----------
    QCM_data : dict
        Data to generate the QCM under the following form :
        {
            "QCM_name": str,
            "questions": [
                {"question": str, "options": list, "answer": int}
            ]
        }

    progress_bar
        Kivy progress bar to update it on the interface.

    Returns
    -------
    None
    """

    # Define the path of the file
    file_path = folder_path + \
        QCM_data["QCM_name"] + "_H5P_text_single_choice.txt"

    nb_questions = len(QCM_data["questions"])

    # Open the file to write it
    with open(file_path, "w", encoding="utf-8") as file:
        for question_dict in QCM_data["questions"]:

            # Put the answer in first position
            answer_id = question_dict["answer"]
            crossed_list = [(i != answer_id, e)
                            for (i, e) in enumerate(question_dict["options"])]
            crossed_list = sorted(crossed_list)
            options_list = [e[1] for e in crossed_list]

            # Ecriture dans le fichier
            file.write(question_dict["question"] + "\n")
            for option in options_list:
                file.write(option + "\n")
            file.write("\n")

            progress_bar.value += 20 / nb_questions


def export_QCM_H5P_fill_blanks(QCM_data, folder_path, progress_bar):
    """
    Export the QCM and its solution in a .h5p file for sinle choice H5P integration.

    Parameters
    ----------
    QCM_data : dict
        Data to generate the QCM under the following form :
        {
            "QCM_name": str,
            "questions": [
                {"question": str, "options": list, "answer": int}
            ]
        }

    progress_bar
        Kivy progress bar to update it on the interface.

    Returns
    -------
    None
    """

    # Define the path of the export folder
    folder_path = folder_path + QCM_data["QCM_name"] + "_fill_in_the_blanks"

    # Copy the template folder
    if not os.path.exists(folder_path):
        shutil.copytree(PATH_FILL_IN_THE_BLANKS_H5P_FOLDER, folder_path)

    # Create the content dict
    content_dict = {
        "questions": [],
        "showSolutions": "Show solutions",
        "tryAgain": "Try again",
        "text": "<p>Insert the missing words in this text about berries found in Norwegian forests and mountainous regions.<\/p>\n",
        "checkAnswer": "Check",
        "notFilledOut": "Please fill in all blanks",
        "behaviour": {
            "enableSolutionsButton": True,
            "autoCheck": True,
            "caseSensitive": False,
            "showSolutionsRequiresInput": True,
            "separateLines": False,
            "enableRetry": True,
            "confirmCheckDialog": False,
            "confirmRetryDialog": False,
            "acceptSpellingErrors": False,
            "enableCheckButton": True
        },
        "answerIsCorrect": "&#039;:ans&#039; is correct",
        "answerIsWrong": "&#039;:ans&#039; is wrong",
        "answeredCorrectly": "Answered correctly",
        "answeredIncorrectly": "Answered incorrectly",
        "solutionLabel": "Correct answer:",
        "inputLabel": "Blank input @num of @total",
        "inputHasTipLabel": "Tip available",
        "tipLabel": "Tip",
        "confirmCheck": {
            "header": "Finish ?",
            "body": "Are you sure you wish to finish ?",
            "cancelLabel": "Cancel",
            "confirmLabel": "Finish"
        },
        "confirmRetry": {
            "header": "Retry ?",
            "body": "Are you sure you wish to retry ?",
            "cancelLabel": "Cancel",
            "confirmLabel": "Confirm"
        },
        "overallFeedback": [
            {
                "from": 0,
                "to": 100,
                "feedback": "You got @score of @total blanks correct."
            }
        ],
        "scoreBarLabel": "You got :num out of :total points",
        "submitAnswer": "Submit",
        "a11yCheck": "Check the answers. The responses will be marked as correct, incorrect, or unanswered.",
        "a11yShowSolution": "Show the solution. The task will be marked with its correct solution.",
        "a11yRetry": "Retry the task. Reset all responses and start the task over again.",
        "a11yCheckingModeHeader": "Checking mode"}

    progress_bar.value = 63
    nb_questions = len(QCM_data["questions"])

    # Store the questions inside
    for question_dict in QCM_data["questions"]:
        question = question_dict["question"]
        question = remove_three_dots(question)
        split_question = question.split("...", 1)
        answer = question_dict["options"][question_dict["answer"]]
        line = f"<p>{split_question[0]} *{answer}* {split_question[1]}<\/p>\n"
        content_dict["questions"].append(line)

        progress_bar.value += 15 / nb_questions

    # Create the json file
    save_json_file(folder_path + "/content/content.json", content_dict)

    # Zip the folder
    shutil.make_archive(folder_path, 'zip', folder_path)

    # Remove the file if it already exists
    if os.path.exists(folder_path + ".h5p"):
        os.remove(folder_path + ".h5p")

    # Rename the file to have the .h5p extension
    os.rename(folder_path + ".zip", folder_path + ".h5p")

    # Remove the construction folder
    shutil.rmtree(folder_path)

    progress_bar.value = 80


def export_QCM_H5P_text_fill_blanks(QCM_data, folder_path, progress_bar):
    """
    Export the QCM and its solution in a .h5p file for sinle choice H5P integration.

    Parameters
    ----------
    QCM_data : dict
        Data to generate the QCM under the following form :
        {
            "QCM_name": str,
            "questions": [
                {"question": str, "options": list, "answer": int}
            ]
        }

    progress_bar
        Kivy progress bar to update it on the interface.

    Returns
    -------
    None
    """

    # Define the path of the file
    file_path = folder_path + \
        QCM_data["QCM_name"] + "_H5P_text_fill_in_the_blanks.txt"

    nb_questions = len(QCM_data["questions"])

    # Open the file to write it
    with open(file_path, "w", encoding="utf-8") as file:
        for question_dict in QCM_data["questions"]:

            # Split the question
            question = question_dict["question"]
            question = remove_three_dots(question)
            split_question = question.split("...", 1)

            # Create the line
            answer = question_dict["options"][question_dict["answer"]]
            line = split_question[0] + " *" + answer + "* " + split_question[1]

            # Ecriture dans le fichier
            file.write(line + "\n")

            progress_bar.value += 20 / nb_questions


def export_QCM_moodle(QCM_data, folder_path, progress_bar):
    """
    Export the QCM and its solution in a .xml file for moodle.

    Parameters
    ----------
    QCM_data : dict
        Data to generate the QCM under the following form :
        {
            "QCM_name": str,
            "questions": [
                {"question": str, "options": list, "answer": int}
            ]
        }

    progress_bar
        Kivy progress bar to update it on the interface.

    Returns
    -------
    None
    """

    # Build the path of the file
    QCM_path = folder_path + QCM_data["QCM_name"] + ".xml"

    ### Build the xml tree ###

    # Introduction

    QCM_tree = etree.Element("quiz")

    QCM_intro = etree.SubElement(QCM_tree, "question")
    QCM_intro.set("type", "category")

    QCM_intro_cat = etree.SubElement(QCM_intro, "category")
    QCM_intro_cat_txt = etree.SubElement(QCM_intro_cat, "text")
    QCM_intro_cat_txt.text = QCM_data["QCM_name"]

    QCM_intro_info = etree.SubElement(QCM_intro, "info")
    QCM_intro_info.set("format", "moodle_auto_format")

    QCM_intro_info_txt = etree.SubElement(QCM_intro_info, "text")
    QCM_intro_info_txt.text = "QCM"

    QCM_intro_id = etree.SubElement(QCM_intro, "idnumber")

    progress_bar.value = 63

    # Questions

    # Extract the data
    questions = QCM_data["questions"]

    progress_bar.value = 83
    nb_questions = len(QCM_data["questions"])

    for i in range(len(questions)):
        question_dict = questions[i]

        # Create the tree of the question
        question = etree.SubElement(QCM_tree, "question")
        question.set("type", "multichoice")

        # Add the instruction
        question_name = etree.SubElement(question, "name")
        question_name_txt = etree.SubElement(question_name, "text")
        question_name_txt.text = "Choose the correct answer"

        # Add the question text
        question_text = etree.SubElement(question, "questiontext")
        question_text.set("format", "html")
        question_text_txt = etree.SubElement(question_text, "text")
        question_text_txt.text = "<![CDATA[<p>" + \
            question_dict["question"] + "<br></p>]]>"

        # Set the options of the question
        question_fb = etree.SubElement(question, "generalfeedback")
        question_fb.set("format", "html")
        question_fb_txt = etree.SubElement(question_fb, "text")
        question_fb_txt.text = ""

        question_dg = etree.SubElement(question, "defaultgrade")
        question_dg.text = "1.0"

        question_py = etree.SubElement(question, "penalty")
        question_py.text = "0.0"

        question_hi = etree.SubElement(question, "hidden")
        question_hi.text = "0"

        question_id = etree.SubElement(question, "idnumber")

        question_single = etree.SubElement(question, "single")
        question_single.text = "true"

        question_sa = etree.SubElement(question, "shuffleanswers")
        question_sa.text = "true"

        question_an = etree.SubElement(question, "answernumbering")
        question_an.text = "abc"

        question_ssi = etree.SubElement(question, "showstandardinstruction")
        question_ssi.text = "1"

        question_cfb = etree.SubElement(question, "correctfeedback")
        question_cfb.set("format", "html")
        question_cfb_txt = etree.SubElement(question_cfb, "text")
        question_cfb_txt.text = "Your answer is correct."

        question_pcfb = etree.SubElement(question, "partiallycorrectfeedback")
        question_pcfb.set("format", "html")
        question_pcfb_txt = etree.SubElement(question_pcfb, "text")
        question_pcfb_txt.text = "Your answer is partially correct."

        question_ifb = etree.SubElement(question, "partiallycorrectfeedback")
        question_ifb.set("format", "html")
        question_ifb_txt = etree.SubElement(question_ifb, "text")
        question_ifb_txt.text = "Your answer is incorrect."

        question_snc = etree.SubElement(question, "shownumcorrect")

        for j in range(len(question_dict["options"])):
            option = question_dict["options"][j]
            if j == question_dict["answer"]:
                fraction = "100"
            else:
                fraction = "0"
            question_answer = etree.SubElement(question, "answer")
            question_answer.set("fraction", fraction)
            question_answer.set("format", "html")
            question_answer_txt = etree.SubElement(question_answer, "text")
            question_answer_txt.text = "<![CDATA[<p>" + \
                option + "<br></p>]]>"
            question_answer_fb = etree.SubElement(question_answer, "feedback")
            question_answer_fb.set("format", "html")
            question_answer_fb_txt = etree.SubElement(
                question_answer_fb, "text")

        # Update the value of the progress bar
        progress_bar.value += 17 / nb_questions

    # Open the files
    QCM_file = open(QCM_path, "w", encoding="utf-8")

    # Write the xml in the file
    QCM_file.write(
        etree.tostring(QCM_tree, encoding="utf-8", pretty_print=True).decode('utf-8').replace("&lt;", "<").replace("&gt;", ">"))


def launch_export_QCM(config, class_name, dict_formats, progress_bar, close_button, label_popup, popup):
    """
    Export the QCM in txt, xml for moodle and docx if a template is choosen and save the data in the class.

    Parameters
    ----------
    config : dict
        Dictionnary of configuration.

    class_name : str
        Name of the selected class can also be None.

    dict_formats : dict
        Dictionary containing the formats wanted by the user.

    progress_bar
        Kivy progress bar to update the interface.

    Returns
    -------
    None
    """

    # Load the data of the class
    if class_name is not None:
        class_content = load_class(class_name)
    else:
        class_content = {}

    template = config["template"]

    # Create the data of the QCM
    QCM_data, class_content = generate_QCM(config, class_content, progress_bar)

    if QCM_data is None:
        progress_bar.value = 0
        close_button.disabled = False
        files_string = ""
        for e in class_content:
            files_string += e + "\n"
        label_popup.text = DICT_LANGUAGE["qcm"]["qcm_generation"]["label_error_popup"] + files_string
        popup.title = DICT_LANGUAGE["qcm"]["qcm_generation"]["title_error_popup"]
        return False

    # Create the folder
    folder_path = create_folder_QCM(QCM_data)

    # TEMP
    save_json_file(folder_path + QCM_data["QCM_name"] + ".json", QCM_data)

    # Export it as txt
    if dict_formats["txt"]:
        export_QCM_txt(QCM_data, folder_path, progress_bar)

    # Export it as docx if a template is choosen
    if dict_formats["docx"]:
        export_QCM_docx(QCM_data, folder_path, template, progress_bar)

    # Export it in xml for moodle
    if dict_formats["xml"]:
        export_QCM_moodle(QCM_data, folder_path, progress_bar)

    # Export it in single choice H5P
    if dict_formats["h5p"]:
        export_QCM_H5P_text_single_choice(QCM_data, folder_path, progress_bar)

    # Export it in fill in blanks H5P
    if dict_formats["h5p"]:
        export_QCM_H5P_text_fill_blanks(QCM_data, folder_path, progress_bar)

    # Save the class data if one is choosen
    if class_name is not None and config["update_class"]:
        save_class(class_name, class_content)

    # Final update of the content of the popup
    progress_bar.value = 100
    close_button.disabled = False
    label_popup.text = DICT_LANGUAGE["qcm"]["qcm_generation"]["label_end_popup"]
    popup.title = DICT_LANGUAGE["qcm"]["qcm_generation"]["title_end_popup"]
    return True
