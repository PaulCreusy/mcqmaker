"""
Module tools of QCMMaker
"""

###############
### Imports ###
###############

import json
import os
import random

#################
### Constants ###
#################

PATH_MAIN_DATABASE = "Banque de questions/"
PATH_CLASS_FOLDER = "Classes/"
PATH_DATA_FOLDER = "data/"
PATH_RESSOURCES_FOLDER = "ressources/"
PATH_EXPORT = "Export/"

#################
### Functions ###
#################

### Basics functions ###

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

### Classes functions ###

def list_classes():
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
    list
        Data of the class.
    """

    # Open the file
    file_path = PATH_CLASS_FOLDER + class_name + ".txt"
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Extract the content
    class_content = []

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
        questions_list = [str(e) for e in questions_list_str]

        # Add the data to the content
        current_dict = {}
        current_dict["name_folder"] = folder
        current_dict["name_file"] = file
        current_dict["used_questions"] = len(questions_list)
        current_dict["total_questions"] = get_nb_questions(file, folder)
        current_dict["list_questions_used"] = questions_list

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

    # Build path of the class
    path = PATH_CLASS_FOLDER + class_name + ".txt"

    with open(path, "w", encoding="utf-8") as file:

        # Write the name of the class
        file.write(class_name + "\n")

        # Write the content of the used files one by one
        for i in range(len(class_data)):
            current_dict = class_data[i]
            name_folder = current_dict["name_folder"]
            name_file = current_dict["name_file"]
            file_path = name_folder + "/" + name_file + ".txt"
            list_questions_used = current_dict["list_questions_used"]
            file.write(file_path + " : " + list_questions_used + "\n")

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
    save_class(class_name, [])

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
    return load_json_file(PATH_DATA_FOLDER + config_name + ".json")

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
    save_json_file(PATH_DATA_FOLDER + config_name + ".json", config)

### Database functions ###

def list_database_folders():
    """
    Return the list of the folders contained in the database.
    """
    folder_list = os.listdir(PATH_CLASS_FOLDER)
    cleaned_folder_list = filter_hidden_files(
        folder_list)
    return cleaned_folder_list

def list_database_files(folder_name):
    """
    Return the list of files contained in the specified folder of the database.
    """
    database_files_list = os.listdir(PATH_MAIN_DATABASE + folder_name)
    cleaned_database_files_list = filter_hidden_files(
        database_files_list, ".txt")
    res = [e.replace(".txt", "") for e in cleaned_database_files_list]
    return res

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
            question_and_answers = line.split(" : ")
            question = question_and_answers[0]
            answers = question_and_answers[1:]
            solution = solution.replace(" ", "")
            solution_id = convert_letter_to_int(solution)
        except:
            # raise ValueError(
            #     f"Erreur détectée dans le fichier {database_name} du dossier {database_folder} à la ligne {line_id + 1}")
            error_list.append(line_id)

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

    # Build the path of the file
    path = PATH_MAIN_DATABASE + database_folder + "/" + database_name + ".txt"

    # Raise an error if the path does not exist
    if not os.path.exists(path):
        raise ValueError(
            f"Le fichier de questions {database_name} du dossier {database_folder} n'existe pas.")

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
    new_folder_path = PATH_MAIN_DATABASE + folder_name
    os.mkdir(new_folder_path)

### QCM functions ###

def generate_QCM(config, progress_bar=None):
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
                    {"folder": str, "file": str, "nb_questions": int},
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
        folder = current_dict["folder"]
        file = current_dict["file"]
        nb_questions = current_dict["nb_questions"]
        database_questions = load_database(file, folder)

        # Mix if needed
        if mix_among_databases:
            selected_questions = random.sample(
                database_questions, nb_questions)
        else:
            selected_questions = database_questions[:nb_questions]

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

    return QCM_data


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

    # Scan the list of questions
    for i in range(len(questions)):

        # Extract the data
        question_dict = questions[i]
        question = question_dict["question"]
        options = question_dict["options"]
        answer = question_dict["answer"]

        # Write the current question
        QCM_file.write(f"{str(i)}. {question}\n")
        for j in range(len(options)):
            QCM_file.write(f"\t{convert_int_to_letter(j)}) {options[j]}")
        QCM_file.write("\n\n")

        # Write the solution
        solution_file.write(f"{i}\t{convert_int_to_letter(answer)}\n")


def export_QCM_docx(QCM_data, progress_bar):
    raise NotImplementedError

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
            {"folder": str, "file": str, "nb_questions": int},
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
