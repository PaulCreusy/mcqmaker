"""
Test module of tools
"""

###############
### Imports ###
###############

import sys

sys.path.append("./")

from qcm_maker_tools.tools import *

from mock import patch

######################
### Test variables ###
######################

### Paths ###

PATH_TEST_DATA = "test/data/"
PATH_TEST_JSON_FILE = PATH_TEST_DATA + "test.json"
PATH_TEST_SAVE_JSON_FILE = PATH_TEST_DATA + "test_save.json"
PATH_TEMPLATE_FOLDER = PATH_TEST_DATA + "Templates/"
PATH_CLASS_FOLDER = PATH_TEST_DATA + "Classes/"
PATH_MAIN_DATABASE = PATH_TEST_DATA + "Database/"

### Variables ###

test_json_file_dict = {
    "string": "This is a string",
    "int": 42,
    "list": [
        "A",
        "B",
        "C"
    ]
}

file_list_1 = [".ssh", "abc.txt", "toto.docx", "lupa.xlsx", "fraise",
               "Patate", "mark.txt", ".secret.txt", "settings.json", "coverage.txt"]

long_text = "This is a very very very very very very very very very very very long text."


######################
### Test functions ###
######################

### Convert letter to int ###

def test_convert_letter_to_int():
    assert convert_letter_to_int("A") == 0
    assert convert_letter_to_int("Z") == 25
    assert convert_letter_to_int("a") == 0
    assert convert_letter_to_int("z") == 25


test_convert_letter_to_int()

### Convert int to letter ###

def test_convert_int_to_letter():
    assert convert_int_to_letter(0) == "A"
    assert convert_int_to_letter(25) == "Z"


test_convert_int_to_letter()

### Load json file ###

def test_load_json_file():
    assert load_json_file(PATH_TEST_JSON_FILE) == test_json_file_dict


test_load_json_file()

### Save json file ###

def test_save_json_file():
    save_json_file(PATH_TEST_SAVE_JSON_FILE, test_json_file_dict)


test_save_json_file()

### Filter hidden files ###

def test_filter_hidden_files():
    assert filter_hidden_files(file_list_1) == ["abc.txt", "toto.docx", "lupa.xlsx", "fraise",
                                                "Patate", "mark.txt", "settings.json", "coverage.txt"]
    assert filter_hidden_files(file_list_1, ".txt") == [
        "abc.txt", "mark.txt", "coverage.txt"]
    assert filter_hidden_files(file_list_1, ".xlsx") == ["lupa.xlsx"]


test_filter_hidden_files()

### Get list templates ###
@patch("qcm_maker_tools.tools.PATH_TEMPLATE_FOLDER", PATH_TEMPLATE_FOLDER)
def test_get_list_templates():
    assert get_list_templates() == ["Template_A", "Template_B", "Template_C"]


test_get_list_templates()

### Get list classes ###

@patch("qcm_maker_tools.tools.PATH_CLASS_FOLDER", PATH_CLASS_FOLDER)
def test_get_list_classes():
    assert get_list_classes() == ["Classe_1", "Classe_2"]


test_get_list_classes()

### Get list database folders ###

@patch("qcm_maker_tools.tools.PATH_MAIN_DATABASE", PATH_MAIN_DATABASE)
def test_get_list_database_folders():
    assert get_list_database_folders(caracter_limit=1000) == [
        "Gram", "Voc"]
