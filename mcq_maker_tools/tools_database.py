"""
Module tools database of MCQMaker

Constants
---------

CORRECT_ANSWER_SEPARATOR : str
    String used to separe the correct answer in the line in the database files.

QUESTION_ANSWER_SEPARATOR : str
    String used to separe the question and the answers in the line in the database files.

Functions
---------

get_list_database_folders

get_list_database_files

load_database

get_nb_questions

save_database

create_database_folder
"""

###############
### Imports ###
###############

import sys
import os

sys.path.append(".")

from mcq_maker_tools.tools import (
    SETTINGS,
    filter_hidden_files,
    convert_letter_to_int,
    convert_int_to_letter,
    load_json_file,
    save_json_file
)


#################
### Functions ###
#################

file_format = {
    "file_name": "My database",
    "list_questions": [
        {
            "question": "Quel est la couleur du cheval prune d'Henry IV ?",
            "id": 5,  # generated id
            "options": ["Blanc", "Bleu", "Prune"],
            "answer": 2
        }
    ]
}

### Database functions ###

def get_list_database_folders():
    """
    Return the list of the folders contained in the database.
    """
    folder_list = os.listdir(SETTINGS["path_database"])
    cleaned_folder_list = filter_hidden_files(
        folder_list)
    return cleaned_folder_list

def get_list_database_files(folder_name, exclusion_list=[]):
    """
    Return the list of files contained in the specified folder of the database.

    Parameters
    ----------
    folder_name : str
        Name of the folder.

    exclusion_list : list of tuples, optional (default is [])
        List of tuples containing the folder and the file to exclude.
    """
    file_exclusion_list = [
        e[1] + ".json" for e in exclusion_list if e[0] == folder_name]
    database_files_list = os.listdir(SETTINGS["path_database"] + folder_name)
    cleaned_database_files_list = filter_hidden_files(
        database_files_list, ".json")
    res = [e.replace(".json", "")
           for e in cleaned_database_files_list if not e in file_exclusion_list]
    return res

def get_database_tree():
    """
    Return the files and folders contained in the database as a tree.
    """
    tree = {}
    folders_list = get_list_database_folders()
    for folder in folders_list:
        files_list = get_list_database_files(folder)
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
            "id": int, # generated id of the question
            "answer": int
        }
    ]
    """

    # Build the path of the file
    path = SETTINGS["path_database"] + \
        database_folder + "/" + database_name + ".json"

    # Raise an error if the path does not exist
    if not os.path.exists(path):
        raise ValueError(
            f"Le fichier de questions {database_name} du dossier {database_folder} n'existe pas.")

    # Read the content of the file
    dict_database = load_json_file(
        file_path=path)

    return dict_database["list_questions"]


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

    list_questions = load_database(
        database_name=database_name,
        database_folder=database_folder
    )

    return len(list_questions)


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
                "id": int, # generated id of the question
                "answer": int
            }
        ]

    Returns
    -------
    None
    """

    # Build the path of the file
    path = SETTINGS["path_database"] + \
        database_folder + "/" + database_name + ".json"
    folder_path = SETTINGS["path_database"] + database_folder

    # Check if the folder exists
    if not os.path.exists(folder_path):
        raise ValueError(
            f"Le dossier {database_folder} n'existe pas dans la base de données.")

    # Write the content inside the file
    dict_database = {
        "file_name": database_name,
        "list_questions": content
    }

    # Save the database
    save_json_file(
        file_path=path,
        dict_to_save=dict_database
    )


def create_database_folder(folder_name):
    """
    Create a new folder in the database with the given name.

    Parameters
    ----------
    folder_name : str
        Name of the folder to create.

    Returns
    -------
    None
    """
    new_folder_path = SETTINGS["path_database"] + folder_name
    os.mkdir(new_folder_path)

### Delete folders and files of the database ###

def delete_folder(folder_name):
    """
    Delete a folder of the database and the files inside.

    Parameters
    ----------
    folder_name : str
        Name of the folder to delete.

    Returns
    -------
    None   
    """
    folder_path = SETTINGS["path_database"] + folder_name
    for file in os.listdir(folder_path):
        os.remove(folder_path + "/" + file)
    os.rmdir(folder_path)

def delete_file(folder_name, file_name):
    """
    Delete a file of the database.

    Parameters
    ----------
    folder_name : str
        Name of the folder comprising the file to delete.

    file : str
        Name of the file to delete.

    Returns
    -------
    None   
    """
    file_path = SETTINGS["path_database"] + \
        folder_name + "/" + file_name + ".json"
    os.remove(file_path)
