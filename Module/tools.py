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

#################
### Functions ###
#################

### Basics functions ###

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
    file_path = PATH_CLASS_FOLDER + class_name
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
        questions_list_str = questions.split(",")
        questions_list = [str(e) for e in questions_list_str]

        # Add the data to the content
        current_dict = {}
        current_dict["name_folder"] = folder
        current_dict["name_file"] = file
        current_dict["used_questions"] = len(questions_list)
        current_dict["total_question"] = ...
        current_dict["list_questions_used"] = questions_list

    return class_content

def save_class(class_name, class_data):
    pass

def reset_class(class_name):
    pass

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

def load_database(database_name):
    pass

def save_database(database_name, content):
    pass

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

def generate_QCM_txt(config, progress_bar):
    pass

def generate_QCM_docx(config, progress_bar):
    pass


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
    "class": str,
    "questions":
        [
            ["folder1", "database_1", int],
            ["folder2", "database_2", int]
        ],
    "template": str,
    "mix_all_questions": bool,
    "mix_among_databases": bool
}
