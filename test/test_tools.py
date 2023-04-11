"""
Test module of tools
"""

###############
### Imports ###
###############

import sys

sys.path.append("./")

from qcm_maker_tools.tools import *

######################
### Test variables ###
######################

PATH_TEST_JSON_FILE = "test/data/test.json"
PATH_TEST_SAVE_JSON_FILE = "test/data/test_save.json"

test_json_file_dict = {
    "string": "This is a string",
    "int": 42,
    "list": [
        "A",
        "B",
        "C"
    ]
}

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
