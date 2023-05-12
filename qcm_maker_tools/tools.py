"""
Module tools of QCMMaker
"""

###############
### Imports ###
###############

import json
import os
import math


#################
### Constants ###
#################

PATH_MAIN_DATABASE = "Banque de questions/"
PATH_CLASS_FOLDER = "Classes/"
PATH_DATA_FOLDER = "data/"
PATH_RESOURCES_FOLDER = "resources/"
PATH_EXPORT = "Export/"
PATH_SETTINGS = PATH_DATA_FOLDER + "settings.json"
PATH_LANGUAGE = PATH_DATA_FOLDER + "languages/"
PATH_TEMPLATE_FOLDER = "Templates/"
PATH_CONFIG_FOLDER = PATH_DATA_FOLDER + "configuration/"
PATH_SINGLE_CHOICE_H5P_FOLDER = PATH_RESOURCES_FOLDER + "single-choice"
PATH_FILL_IN_THE_BLANKS_H5P_FOLDER = PATH_RESOURCES_FOLDER + "fill-in-the-blanks"
PATH_KIVY_FOLDER = PATH_RESOURCES_FOLDER + "kivy/"
PATH_LOGO_64 = PATH_RESOURCES_FOLDER + "logo_64.png"
PATH_LOGO = PATH_RESOURCES_FOLDER + "logo.png"

# Load the settings
with open(PATH_SETTINGS, "r", encoding="utf-8") as file:
    SETTINGS = json.load(file)

# Load the language
with open(PATH_LANGUAGE + SETTINGS["language"] + ".json", "r", encoding="utf-8") as file:
    DICT_LANGUAGE = json.load(file)

# Define caracter limits
CARACTER_LIMIT = 18
NO_CARACTER_LIMIT = math.inf

# Define json filetype
json_filetypes = [("json", ".json")]


#################
### Functions ###
#################

### Basics functions ###

def remove_three_dots(string: str):
    while "...." in string:
        string = string.replace("....", "...")
    return string


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
    # Clean the name from \n used in Kivy
    config_name = clean_newlines(config_name)

    # Load the json file
    res = load_json_file(PATH_CONFIG_FOLDER + config_name + ".json")

    # Clean the files that do not exist anymore
    to_delete_list = []
    for (i, question) in enumerate(res["questions"]):
        folder_name = clean_newlines(question["folder_name"])
        file_name = clean_newlines(question["file_name"])
        if not os.path.exists(PATH_MAIN_DATABASE + folder_name + "/" + file_name + ".txt"):
            to_delete_list.append(i)
    for e in to_delete_list[::-1]:
        res["questions"].pop(e)

    return res

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
