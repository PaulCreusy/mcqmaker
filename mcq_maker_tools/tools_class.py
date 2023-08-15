"""
Module tools class of MCQMaker

Contains the functions used for class manipulation.

Functions
---------
"""

###############
### Imports ###
###############

### Python imports ###

import os
import sys

sys.path.append(".")

### Module imports ###

from mcq_maker_tools.tools import (
    SETTINGS,
    filter_hidden_files,
    load_json_file,
    save_json_file
)
from mcq_maker_tools.tools_database import (
    get_nb_questions,
    get_database_tree,
    load_database
)


#################
### Functions ###
#################

### Classes functions ###

def get_list_classes():
    """
    Return the list of names of the classes stored in the class folder.
    """
    classes_files_list = os.listdir(SETTINGS["path_class"])
    cleaned_classes_files_list = filter_hidden_files(
        classes_files_list, ".json")
    res = [e.replace(".json", "") for e in cleaned_classes_files_list]
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

    # Open the file
    file_path = SETTINGS["path_class"] + class_name + ".json"
    dict_class = load_json_file(file_path=file_path)

    # Extract the content
    class_content = {}

    for key in dict_class:
        if key != "class_name":
            questions_list = clean_unused_question_ids(dict_class[key], key)
            temp_list = key.split("/")
            current_dict = {}
            current_dict["used_questions"] = len(questions_list)
            current_dict["total_questions"] = get_nb_questions(
                temp_list[1], temp_list[0])
            current_dict["list_questions_used"] = questions_list
            class_content[(temp_list[0], temp_list[1])] = current_dict

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
    new_dict = {}
    for key in list(class_content.keys()):
        current_dict = class_content[key]
        if not ("used_questions" in current_dict and current_dict["used_questions"] == 0):
            new_dict[key] = current_dict
    return new_dict

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
    dict_class = {
        "class_name": class_name
    }

    class_data = clean_class_content_from_empty_lines(class_data)

    # Build the path of the class
    file_path = SETTINGS["path_class"] + class_name + ".json"
    for key in class_data:
        new_key = key[0] + "/" + key[1]
        dict_class[new_key] = class_data[key]["list_questions_used"]
    save_json_file(
        file_path=file_path,
        dict_to_save=dict_class
    )


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

def clean_unused_question_ids(question_list: list, folder_file: str):
    """
    Clean the unused question in the question list of a class.
    """
    folder_name, file_name = folder_file.split("/")
    database_content = load_database(file_name, folder_name)

    to_remove_list = []
    for idx in question_list:
        is_used = False
        for question_dict in database_content:
            if question_dict["id"] == idx:
                is_used = True
        if not is_used:
            to_remove_list.append(idx)

    question_list = [idx for idx in question_list if idx not in to_remove_list]

    return question_list
