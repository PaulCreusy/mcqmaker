"""
Module tools of QCMMaker
"""


###############
### Imports ###
###############


### Python imports ###

import os
import sys
import platform
from typing import Literal
import json
import math
import random
import toml
import webbrowser


#################
### Constants ###
#################

platform_name = platform.system()

if platform_name == "Darwin":
    DIR_PATH = os.path.sep.join(sys.argv[0].split(os.path.sep)[:-1]) + "/"
    print(DIR_PATH)
else:
    DIR_PATH = "./"

PATH_DATA_FOLDER = DIR_PATH + "data/"
PATH_RESOURCES_FOLDER = DIR_PATH +"resources/"
PATH_SETTINGS = PATH_DATA_FOLDER + "settings.json"
PATH_LANGUAGE = PATH_RESOURCES_FOLDER + "languages/"
PATH_TEMPLATE_FOLDER = DIR_PATH +"Templates/"
PATH_CONFIG_FOLDER = PATH_DATA_FOLDER + "configuration/"
PATH_SINGLE_CHOICE_H5P_FOLDER = PATH_RESOURCES_FOLDER + "single-choice"
PATH_FILL_IN_THE_BLANKS_H5P_FOLDER = PATH_RESOURCES_FOLDER + "fill-in-the-blanks"
PATH_KIVY_FOLDER = PATH_RESOURCES_FOLDER + "kivy/"
PATH_LOGO_64 = PATH_RESOURCES_FOLDER + "logo_64.png"
PATH_LOGO = PATH_RESOURCES_FOLDER + "logo.png"
PATH_VERSION_FILE = DIR_PATH + "version.toml"

# Create the data folder if it does not exist
if not os.path.exists(PATH_DATA_FOLDER):
    os.mkdir(PATH_DATA_FOLDER)

if not os.path.exists(PATH_CONFIG_FOLDER):
    os.mkdir(PATH_CONFIG_FOLDER)

# Create default settings if they do not exist
if not os.path.exists(PATH_SETTINGS):
    SETTINGS = {
        "show_instructions": True,
        "default_template": None,
        "language": "english",
        "dict_exports": {
            "txt": True,
            "docx": False,
            "h5p": False,
            "xml": False
        },
        "path_export": DIR_PATH +"Export/",
        "path_class": DIR_PATH +"Classes/",
        "path_database": DIR_PATH +"Question Database/"
    }
    with open(PATH_SETTINGS, "w", encoding="utf-8") as file:
        json.dump(SETTINGS, file, indent=4)

    # Create the default folders if they do not exist
    for key in ("path_export", "path_class", "path_database"):
        if not os.path.exists(SETTINGS[key]):
            os.mkdir(SETTINGS[key])

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
JSON_FILETYPES = [("json", ".json")]

# MCQ import extensions
MCQ_IMPORT_EXT = [("PDF", ".pdf"), ("Word", ".docx"),
                  ("TXT", ".txt"), ("Word", ".doc")]

# Define the correspondences between languages and their names
DICT_CORR_LANGUAGES = {
    "french": "Français",
    "english": "English"
}

### Version number ###
with open(PATH_VERSION_FILE, "r", encoding="utf-8") as file:
    __version__ = toml.load(file)["version"]

#################
### Functions ###
#################

### Basics functions ###


def replace_chars_with(string, char_list, replacer):
    """
    Replace all characters contained in the list with the replacer.
    """

    for char in char_list:
        string = string.replace(char, replacer)

    return string


def remove_begin_and_end_spaces(string: str) -> str:
    """
    Remove the spaces and the end and at the beginning of a string.
    """

    while string[0] == " ":
        string = string[1:]

    while string[-1] == " ":
        string = string[:-1]

    return string


def remove_begin_and_end_char(string: str, char_list: list) -> str:
    """
    Remove the spaces and the end and at the beginning of a string.
    """

    while string[0] in char_list:
        string = string[1:]

    while string[-1] in char_list:
        string = string[:-1]

    return string


def remove_three_dots(string: str):
    while "...." in string:
        string = string.replace("....", "...")
    return string


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
        Dictionnary to save.

    Returns
    -------
    None
    """
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(dict_to_save, file, indent=4)


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


def update_settings(SETTINGS: dict, key: str, value) -> dict:
    """
    Change a value in the settings dictionnary and save it.

    Parameters
    ----------
    SETTINGS : dict
        Dict containing the settings.

    key : str
        Key of the value to change.

    value : str | bool  
        New value to set.

    Returns
    -------
    dict : Updated settings dictionnary. 
    """
    SETTINGS[key] = value
    save_json_file(PATH_SETTINGS, SETTINGS)
    return SETTINGS


### Configuration functions ###

def get_config_list():
    """
    Return the list of configuration contained in the data.

    Parameters
    ----------

    Returns
    -------
    list
        List of configuration names.
    """
    config_list = os.listdir(PATH_CONFIG_FOLDER)
    res = [e.replace(".json", "") for e in config_list]
    return res


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
    # Load the json file
    res = load_json_file(PATH_CONFIG_FOLDER + config_name + ".json")

    # Clean the files that do not exist anymore
    to_delete_list = []
    for (i, question) in enumerate(res["questions"]):
        folder_name = question["folder_name"]
        file_name = question["file_name"]
        if not os.path.exists(SETTINGS["path_database"] + folder_name + "/" + file_name + ".json"):
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
    save_json_file(PATH_CONFIG_FOLDER + config_name + ".json", config)


def set_first_letter_upper_case(string: str):
    """
    Return a string with its first letter as upper case.

    Parameters
    ----------
    string : str
        String to change.

    Returns
    -------
    str : New string with first letter in upper case.
    """
    return string[0].upper() + string[1:]


def get_current_language():
    """
    Return the name of the current language for the display.

    Returns
    -------
    str : Name of the current language.
    """
    current_language = DICT_CORR_LANGUAGES[SETTINGS["language"]]
    return set_first_letter_upper_case(current_language)


def get_list_languages():
    """
    Return the list of languages of the app.

    Returns
    -------
    list : List of available languages for the app.
    """
    return DICT_CORR_LANGUAGES.values()


def change_path(mode: Literal["export", "class", "database"], new_path):
    """
    Change a path to replace it with the new value.

    Parameters
    ----------
    mode : str
        Type of path to change.

    new_path : str
        New path of the folder.
    """
    global SETTINGS

    SETTINGS = update_settings(SETTINGS, "path_" + mode, new_path)


def compute_standard_deviation(serie):
    res = 0
    mean = sum(serie) / len(serie)
    for val in serie:
        res += (mean - val)**2 / len(serie)
    return math.sqrt(res)


def get_min_idx(value_list, restriction=None):
    if restriction is None:
        restriction = [i for i in range(len(value_list))]
    min_value = value_list[0]
    min_idx = 0
    for i, val in enumerate(value_list):
        if val < min_value and i in restriction:
            min_value = val
            min_idx = i

    return min_idx


def get_max_idx(value_list, restriction=None):
    new_value_list = [-value for value in value_list]
    return get_min_idx(new_value_list, restriction=restriction)


def get_new_question_id(existing_ids):
    """Create a new random id for a question different from the existing ids."""
    new_id = random.randint(0, 1e12)
    while new_id in existing_ids:
        new_id = random.randint(0, 1e12)
    return new_id


def open_link(instance=None, value=None):
    webbrowser.open(value)
