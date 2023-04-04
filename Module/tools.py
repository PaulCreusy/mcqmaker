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

### Classes functions ###

def list_classes():
    pass

def load_class(class_name):
    pass

def save_class(class_name, class_data):
    pass

def reset_class(class_name):
    pass

### Configuration functions ###

def load_config(config_name):
    pass

def save_config(config_name, config):
    pass

### Database functions ###

def list_database_folders():
    pass

def list_database_files(folder_name):
    pass

def load_database(database_name):
    pass

def save_database(database_name, content):
    pass

def create_database_folder(folder_name):
    pass

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
