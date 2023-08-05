"""
Test module of tools
"""

###############
### Imports ###
###############


from mcq_maker_tools.tools import (
    SETTINGS,
    convert_letter_to_int,
    convert_int_to_letter,
    load_json_file,
    save_json_file,
    filter_hidden_files,
    extract_filename_from_path,
    get_max_idx,
    get_min_idx
)


######################
### Test variables ###
######################

### Paths ###

PATH_TEST_DATA = "test/data/"
PATH_TEST_JSON_FILE = PATH_TEST_DATA + "test.json"
PATH_TEST_SAVE_JSON_FILE = PATH_TEST_DATA + "test_save.json"
PATH_TEMPLATE_FOLDER = PATH_TEST_DATA + "Templates/"
SETTINGS["path_class"] = PATH_TEST_DATA + "Classes/"
SETTINGS["path_database"] = PATH_TEST_DATA + "Database/"

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


liste_1 = [1, 5, 2, 3, 0, 3]
max_idx_1 = 1
min_idx_1 = 4

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

### Extract filename from path ###


def test_extract_filename_from_path():
    assert extract_filename_from_path(PATH_TEST_JSON_FILE) == "test"


test_extract_filename_from_path()

### Test get min idx ###


def test_get_min_idx():
    assert get_min_idx(liste_1) == min_idx_1


test_get_min_idx()

### Test get max idx ###


def test_get_max_idx():
    assert get_max_idx(liste_1) == max_idx_1


test_get_max_idx()
