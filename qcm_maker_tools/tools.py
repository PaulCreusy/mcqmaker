"""
Module tools of QCMMaker
"""

###############
### Imports ###
###############

import json
import os
import random
import math
from lxml import etree

#################
### Constants ###
#################

PATH_MAIN_DATABASE = "Banque de questions/"
PATH_CLASS_FOLDER = "Classes/"
PATH_DATA_FOLDER = "data/"
PATH_RESSOURCES_FOLDER = "ressources/"
PATH_EXPORT = "Export/"
PATH_SETTINGS = PATH_DATA_FOLDER + "settings.json"
PATH_TEMPLATE_FOLDER = "Templates/"
PATH_CONFIG_FOLDER = PATH_DATA_FOLDER + "configuration/"

# Load the settings
with open(PATH_SETTINGS, "r", encoding="utf-8") as file:
    SETTINGS = json.load(file)

# Define caracter limits
CARACTER_LIMIT = 18
NO_CARACTER_LIMIT = math.inf

# Define json filetype
json_filetypes = [("json", ".json")]


#################
### Functions ###
#################

### Basics functions ###

def refactor_str_list_for_kivy(str_list, caracter_limit=CARACTER_LIMIT):
    return [cut_text_with_newlines(string, caracter_limit) for string in str_list]

def cut_text_with_newlines(string: str, caracter_limit=20):
    words = string.split(" ")
    res = words.pop(0)
    count = len(res)

    for word in words:
        if count + len(word) < caracter_limit:
            res += " " + word
            count += len(word)
        else:
            res += "\n" + word
            count = len(word)
    return res

def clean_newlines(string: str):
    return string.replace("\n", " ")

def convert_letter_to_int(letter: str):
    """
    Convert an upper case letter to its alphabetical id.

    Parameters
    ----------
    letter : str
        Letter in upper or lower case.

    Returns
    -------
    int
        Alphabetical id.
    """

    # Take the ASCII id of the letter
    letter_ord = ord(letter)

    # Select the reference according to the casing
    if letter_ord < 97:
        ref_ord = 65
    else:
        ref_ord = 97

    return letter_ord - ref_ord

def convert_int_to_letter(letter_ord: int):
    return chr(letter_ord + 65)

def load_json_file(file_path: str) -> dict:
    """
    Load a json file, according the specified path.

    Parameters
    ----------
    file_path : str
        Path of the json file.

    Returns
    -------
    dict
        Content of the json file
    """
    with open(file_path, "r", encoding="utf-8") as file:
        res = json.load(file)
    return res

def save_json_file(file_path: str, dict_to_save: dict) -> None:
    """
    Save the content of the given dictionnary inside the 
    specified json file.

    Parameters
    ----------
    file_path : str
        Path of the json file.

    dict_to_save : dict
        Dictionnary to save

    Returns
    -------
    None
    """
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(dict_to_save, file)

def filter_hidden_files(files_list, extension=""):
    """
    Clean the content of a list from hidden files and with different extensions
    from the selected one. If no extension is given, all of them are kept.

    Parameters
    ----------
    files_list : list
        List of names of files.

    extension : str
        Extension to keep.

    Returns
    -------
    list
        Cleaned list of files.
    """
    res = []
    for file in files_list:
        if file[0] != "." and extension == file[len(file) - len(extension):]:
            res.append(file)
    return res

def extract_filename_from_path(path):
    """
    Return the filename inside a path.

    Parameters
    ----------
    path : str
        Path of the file.

    Returns
    -------
    str
        Name of the file.
    """
    filename_with_ext = os.path.basename(path)
    inv_filename_with_ext = filename_with_ext[::-1]
    inv_filename = inv_filename_with_ext.split(".", 1)[1]
    filename = inv_filename[::-1]
    return filename

def update_settings(SETTINGS, key, value):
    SETTINGS[key] = value
    save_json_file(PATH_SETTINGS, SETTINGS)
    return SETTINGS

### Classes functions ###

def get_list_templates():
    """
    Return the list of names of the templates stored in the template folder.
    """
    template_files_list = os.listdir(PATH_TEMPLATE_FOLDER)
    cleaned_template_files_list = filter_hidden_files(
        template_files_list, ".docx")
    res = [e.replace(".docx", "") for e in cleaned_template_files_list]
    return res

def get_list_classes():
    """
    Return the list of names of the classes stored in the class folder.
    """
    classes_files_list = os.listdir(PATH_CLASS_FOLDER)
    cleaned_classes_files_list = filter_hidden_files(
        classes_files_list, ".txt")
    res = [e.replace(".txt", "") for e in cleaned_classes_files_list]
    return res

def load_class(class_name):
    """
    Return the content of the selected class.

    Parameters
    ----------
    class_name : str
        Name of the class to load.

    Returns
    -------
    dict
        Data of the class.
    """

    if class_name is None:
        return complete_and_filter_class_content({})

    class_name = clean_newlines(class_name)

    # Open the file
    file_path = PATH_CLASS_FOLDER + class_name + ".txt"
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Extract the content
    class_content = {}

    for i in range(len(lines)):

        # Read the line
        line = lines[i]
        line = line.replace("\n", "")
        if " : " not in line:
            continue

        # Extract the data
        database_path, questions = line.split(" : ")
        folder, file = database_path.split("/")
        file = file.replace(".txt", "")
        questions_list_str = questions.split(",")
        questions_list = [int(e) for e in questions_list_str]

        # Add the data to the content
        current_dict = {}
        current_dict["used_questions"] = len(questions_list)
        current_dict["total_questions"] = get_nb_questions(file, folder)
        current_dict["list_questions_used"] = questions_list
        class_content[(folder, file)] = current_dict

    return complete_and_filter_class_content(class_content)

def complete_and_filter_class_content(class_content: dict):
    """
    Complete the class content by adding all other files and delete the unexisting files.

    Parameters
    ----------
    class_content : dict
        Content of the class in a dictionnary with the keys (folder,file).

    Returns
    -------
    dict
        Filtered and completed content of the class.
    """

    # Extract the list of folders
    database_tree = get_database_tree()
    folders_list = database_tree.keys()

    # Scan the content to delete unexisting files
    for key in list(class_content.keys()):
        folder, file = key

        # Verify if folder exists
        if not folder in folders_list:
            class_content.pop((folder, file))
        else:
            files_list = database_tree[folder]

            # Verify if file exists
            if not file in files_list:
                class_content.pop((folder, file))

    # Add the missing files
    for folder in folders_list:
        files_list = database_tree[folder]
        for file in files_list:

            # If no info is in the content at the specified key, add a blank line
            if not (folder, file) in class_content:
                current_dict = {}
                current_dict["used_questions"] = 0
                current_dict["total_questions"] = get_nb_questions(
                    file, folder)
                current_dict["list_questions_used"] = []
                class_content[(folder, file)] = current_dict
    return class_content

def clean_class_content_from_empty_lines(class_content: dict):
    """
    Clean the data of the class to prepare saving by removing empty lines.
    """
    for key in list(class_content.keys()):
        current_dict = class_content[key]
        if "used_questions" in current_dict and current_dict["used_questions"] == 0:
            class_content.pop(key)
    return class_content

def save_class(class_name, class_data):
    """
    Save the given data in the selected class.

    Parameters
    ----------
    class_name : str
        Name of the class.

    class_data : list
        Data of the class.

    Returns
    -------
    None
    """

    class_data = clean_class_content_from_empty_lines(class_data)
    print(class_data)

    class_name = clean_newlines(class_name)

    # Build path of the class
    path = PATH_CLASS_FOLDER + class_name + ".txt"

    with open(path, "w", encoding="utf-8") as file:

        # Write the name of the class
        file.write(class_name + "\n")

        # Write the content of the used files one by one
        for key in class_data:
            current_dict = class_data[key]
            name_folder = key[0]
            name_file = key[1]
            file_path = name_folder + "/" + name_file + ".txt"
            list_questions_used = current_dict["list_questions_used"]
            file.write(file_path + " : " + str(list_questions_used)
                       [1:len(str(list_questions_used)) - 1] + "\n")

def reset_class(class_name):
    """
    Reset the data of the selected class

    Parameters
    ----------
    class_name : str
        Name of the selected class.

    Returns 
    -------
    None
    """
    save_class(class_name, {})

### Configuration functions ###

def load_config(config_name):
    """
    Load a configuration stored in the data folder.

    Parameters
    ----------
    config_name : str
        Name of the configuration.

    Returns
    -------
    dict
        Configuration.
    """
    config_name = clean_newlines(config_name)
    return load_json_file(PATH_CONFIG_FOLDER + config_name + ".json")

def save_config(config_name, config):
    """
    Save a configuration inside a json file in the data folder.

    Parameters
    ----------
    config_name : str
        Name of the configuration to save

    config : dict
        Configuration to save

    Returns
    -------
    None
    """
    config_name = clean_newlines(config_name)
    save_json_file(PATH_CONFIG_FOLDER + config_name + ".json", config)

### Database functions ###

def get_list_database_folders(caracter_limit=CARACTER_LIMIT):
    """
    Return the list of the folders contained in the database.
    """
    folder_list = os.listdir(PATH_MAIN_DATABASE)
    cleaned_folder_list = filter_hidden_files(
        folder_list)
    return refactor_str_list_for_kivy(cleaned_folder_list, caracter_limit=caracter_limit)

def get_list_database_files(folder_name, caracter_limit=CARACTER_LIMIT, exclusion_list=[]):
    """
    Return the list of files contained in the specified folder of the database.
    """
    file_exclusion_list = [e[1] + ".txt" for e in exclusion_list]
    folder_name = clean_newlines(folder_name)
    database_files_list = os.listdir(PATH_MAIN_DATABASE + folder_name)
    cleaned_database_files_list = filter_hidden_files(
        database_files_list, ".txt")
    res = [e.replace(".txt", "")
           for e in cleaned_database_files_list if not e in file_exclusion_list]
    return refactor_str_list_for_kivy(res, caracter_limit=caracter_limit)

def get_database_tree():
    """
    Return the files and folders contained in the database as a tree.
    """
    tree = {}
    folders_list = get_list_database_folders(caracter_limit=NO_CARACTER_LIMIT)
    for folder in folders_list:
        files_list = get_list_database_files(
            folder, caracter_limit=NO_CARACTER_LIMIT)
        tree[folder] = files_list

    return tree

def load_database(database_name, database_folder):
    """
    Load the file of the database with the given name contained in the selected folder.

    Parameters
    ----------
    database_name : str
        Name of the database file.

    database_folder : str
        Name of the database folder.

    Returns
    -------
    list
        Content of the file under the specified form :
    [
        {
            "question": str,
            "options":
                [
                    "string1",
                    "string2"
                ],
            "answer": int
        }
    ]
    """

    # Clean the names
    database_folder = clean_newlines(database_folder)
    database_name = clean_newlines(database_name)

    # Build the path of the file
    path = PATH_MAIN_DATABASE + database_folder + "/" + database_name + ".txt"

    # Raise an error if the path does not exist
    if not os.path.exists(path):
        raise ValueError(
            f"Le fichier de questions {database_name} du dossier {database_folder} n'existe pas.")

    # Read the content of the file
    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    file_content = []
    error_list = []

    # Scan the lines to extract the content
    for line_id in range(len(lines)):

        # Extraction of the line
        line = lines[line_id]
        line = line.replace("\n", "")

        # Clean empty lines
        if line.replace(" ", "") == "":
            continue

        # Split question, solution and answers
        try:
            question_and_answers, solution = line.split(" @ ")
            question_and_answers = question_and_answers.split(" : ")
            question = question_and_answers[0]
            answers = question_and_answers[1:]
            solution = solution.replace(" ", "")
            solution_id = convert_letter_to_int(solution)
        except:
            # raise ValueError(
            #     f"Erreur détectée dans le fichier {database_name} du dossier {database_folder} à la ligne {line_id + 1}")
            error_list.append(line_id)
            solution_id = 0
            question = line
            answers = [""]

        line_dict = {}
        line_dict["question"] = question
        line_dict["answer"] = solution_id
        line_dict["options"] = answers

        file_content.append(line_dict)

    return file_content, error_list

def get_nb_questions(database_name, database_folder):
    """
    Return the number of questions contained in the specified file.

    Parameters
    ----------
    database_name : str
        Name of the database file.

    database_folder : str
        Name of the database folder.

    Returns
    -------
    int
        Number of questions of the file.
    """

    # Clean the names
    database_folder = clean_newlines(database_folder)
    database_name = clean_newlines(database_name)

    # Build the path of the file
    path = PATH_MAIN_DATABASE + database_folder + "/" + database_name + ".txt"

    # Raise an error if the path does not exist
    if not os.path.exists(path):
        # raise ValueError(
        #     f"Le fichier de questions {database_name} du dossier {database_folder} n'existe pas.")
        return None

    # Read the content of the file
    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    nb_questions = 0

    for line_id in range(len(lines)):

        # Extraction of the line
        line = lines[line_id]
        line = line.replace("\n", "")

        # Check if line not empty
        if line.replace(" ", "") != "":
            nb_questions += 1

    return nb_questions

def save_database(database_name, database_folder, content):
    """
    Save the given content of a database inside the specified file.

    Parameters
    ----------
    database_name : str
        Name of the database.

    database_folder : str
        Name of the database folder.

    content : list
        Content of the database under the following form :
        [
            {
                "question": str,
                "options":
                    [
                        "string1",
                        "string2"
                    ],
                "answer": int
            }
        ]

    Returns
    -------
    None
    """

    # Clean the names
    database_folder = clean_newlines(database_folder)
    database_name = clean_newlines(database_name)

    # Build the path of the file
    path = PATH_MAIN_DATABASE + database_folder + "/" + database_name + ".txt"
    folder_path = PATH_MAIN_DATABASE + database_folder

    # Check if the folder exists
    if not os.path.exists(folder_path):
        raise ValueError(
            f"Le dossier {database_folder} n'existe pas dans la base de données.")

    # Write the content inside the file
    with open(path, "w", encoding="utf-8") as file:
        for i in range(len(content)):
            current_dict = content[i]
            question = current_dict["question"]
            options = current_dict["options"]
            answer = current_dict["answer"]
            answer_str = convert_int_to_letter(answer)
            file.write(question)
            for option in options:
                file.write(" : " + option)
            file.write(" @ " + answer_str + "\n")

def create_database_folder(folder_name):
    """
    Create a new folder in the database with the given name.

    Parameters
    ----------
    folder_name : str
        Name of the folder to create.
    """
    folder_name = clean_newlines(folder_name)
    new_folder_path = PATH_MAIN_DATABASE + folder_name
    os.mkdir(new_folder_path)

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

    # Build sublist of questions
    for i in range(len(instructions)):

        # Load the data
        current_dict = instructions[i]
        folder = current_dict["folder_name"].replace("\n", " ")
        file = current_dict["file_name"].replace("\n", " ")
        nb_questions = current_dict["nb_questions"]
        database_questions, _ = load_database(file, folder)

        # Remove already selected questions
        if (folder, file) in class_content:
            used_questions_list = class_content[(
                folder, file)]["list_questions_used"]
            print(used_questions_list)
            used_questions_list = sorted(used_questions_list)[::-1]
            for question_id in used_questions_list:
                database_questions.pop(question_id)

        # Mix if needed
        if mix_among_databases:
            selected_questions_id = random.sample(
                [j for j in range(len(database_questions))], nb_questions)
        else:
            selected_questions_id = [i for i in range(len(database_questions))][:nb_questions]

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
        selected_questions = [database_questions[j] for j in selected_questions_id]

        # Insert inside the list
        questions_sublists.append(selected_questions)

    # Merge all sublists into a single one
    for sublist in questions_sublists:
        questions += sublist

    # Mix all questions if the option is selected
    if mix_all_questions:
        random.shuffle(questions)

    # Insert data inside the dict
    QCM_data["questions"] = questions

    return QCM_data, class_content


def export_QCM_txt(QCM_data, progress_bar):
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
    QCM_path = PATH_EXPORT + QCM_data["QCM_name"] + ".txt"
    solution_path = PATH_EXPORT + QCM_data["QCM_name"] + "_solution.txt"

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
        progress_bar.value += 27/number_questions


def export_QCM_docx(QCM_data, template, progress_bar):
    progress_bar.value = 33 # au début
    progress_bar.value = 60 # PAUL à la fin
    pass

def export_QCM_moodle(QCM_data, progress_bar):
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
    QCM_path = PATH_EXPORT + QCM_data["QCM_name"] + ".xml"

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
    # TODO - modifier la description
    QCM_intro_info_txt.text = "QCM"

    QCM_intro_id = etree.SubElement(QCM_intro, "idnumber")
    
    progress_bar.value = 63

    # Questions

    # Extract the data
    questions = QCM_data["questions"]

    for i in range(len(questions)):
        question_dict = questions[i]

        # Create the tree of the question
        question = etree.SubElement(QCM_tree, "question")
        question.set("type", "multichoice")

        # Add the instruction
        question_name = etree.SubElement(question, "name")
        question_name_txt = etree.SubElement(question_name, "text")
        # TODO - modifier la consigne
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
        # TODO - modifier la consigne
        question_cfb_txt.text = "Your answer is correct."

        question_pcfb = etree.SubElement(question, "partiallycorrectfeedback")
        question_pcfb.set("format", "html")
        question_pcfb_txt = etree.SubElement(question_pcfb, "text")
        # TODO - modifier la consigne
        question_pcfb_txt.text = "Your answer is partially correct."

        question_ifb = etree.SubElement(question, "partiallycorrectfeedback")
        question_ifb.set("format", "html")
        question_ifb_txt = etree.SubElement(question_ifb, "text")
        # TODO - modifier la consigne
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
        progress_bar.value += 27/len(questions)

    # Open the files
    QCM_file = open(QCM_path, "w", encoding="utf-8")

    # Write the xml in the file
    QCM_file.write(
        etree.tostring(QCM_tree, encoding="utf-8", pretty_print=True).decode('utf-8').replace("&lt;", "<").replace("&gt;", ">"))


def launch_export_QCM(config, class_name, progress_bar, close_button, label_popup):
    """
    Export the QCM in txt, xml for moodle and docx if a template is choosen and save the data in the class.

    Parameters
    ----------
    config : dict
        Dictionnary of configuration.

    class_name : str
        Name of the selected class can also be None.

    template : str
        Name of the selected template can also be None.

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

    # Export it as txt
    export_QCM_txt(QCM_data, progress_bar)

    # Export it as docx if a template is choose
    if template is not None:
        export_QCM_docx(QCM_data, template, progress_bar)

    # Export it in xml for moodle
    export_QCM_moodle(QCM_data, progress_bar)

    # Save the class data if one is choosen
    if class_name is not None and config["update_class"]:
        save_class(class_name, class_content)

    # Final update of the content of the popup
    progress_bar.value = 100
    close_button.disabled = False
    label_popup.text = "La génération du QCM est terminée."


### Data structures ###

content = [
    {
        "question": str,
        "options":
            [
                "string1",
                "string2"
            ],
        "answer": int
    }
]

config = {
    "QCM_name": str,
    "questions":
        [
            {"folder_name": str, "file_name": str, "nb_questions": int},
        ],
    "template": str,
    "mix_all_questions": bool,
    "mix_among_databases": bool
}

class_data = [
    {"name_folder": str, "name_file": str,
        "used_questions": int, "total_questions": int, "list_questions_used": list}
]

QCM_data = {
    "QCM_name": str,
    "questions": [
        {"question": str, "options": list, "answer": int}
    ]
}
