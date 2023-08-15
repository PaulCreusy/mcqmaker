"""
Test module of tools class
"""

###############
### Imports ###
###############

import os
import sys
sys.path.append(".")

from mock import patch

from mcq_maker_tools.tools_class import (
    get_list_classes,
    load_class,
    complete_and_filter_class_content,
    clean_class_content_from_empty_lines,
    save_class,
    reset_class,
    clean_unused_question_ids
)

######################
### Test variables ###
######################

# Define the paths
PATH_TEST_DATA_FOLDER = "./test/data/"
MOCK_PATH_CLASS = PATH_TEST_DATA_FOLDER + "Classes/"
MOCK_PATH_QUESTIONS = PATH_TEST_DATA_FOLDER + "Questions/"
MOCK_SETTINGS = {"path_class": MOCK_PATH_CLASS,
                 "path_database": MOCK_PATH_QUESTIONS}

# List of classes
CLASS_LIST = ["Classe 1", "Classe 2"]

# Content of classes
CLASS_CONTENT_1 = {
    ("Grammar", "Conjuging"): {
        "used_questions": 2,
        "total_questions": 5,
        "list_questions_used": [0, 1]},
    ("Grammar", "Past and perfect"): {
        "used_questions": 0,
        "total_questions": 5,
        "list_questions_used": []},
    ("Vocabulary", "Farm Animals"): {
        "used_questions": 2,
        "total_questions": 5,
        "list_questions_used": [2, 4]},
    ("Vocabulary", "Complete Sentences"): {
        "used_questions": 0,
        "total_questions": 10,
        "list_questions_used": []}
}
COMPLETED_EMPTY_CLASS = {
    ("Grammar", "Conjuging"): {
        "used_questions": 0,
        "total_questions": 5,
        "list_questions_used": []},
    ("Grammar", "Past and perfect"): {
        "used_questions": 0,
        "total_questions": 5,
        "list_questions_used": []},
    ("Vocabulary", "Farm Animals"): {
        "used_questions": 0,
        "total_questions": 5,
        "list_questions_used": []},
    ("Vocabulary", "Complete Sentences"): {
        "used_questions": 0,
        "total_questions": 10,
        "list_questions_used": []}
}
WRONG_CLASS = {("Random", "Random"): {
    "used_questions": 0,
    "total_questions": 5,
    "list_questions_used": []}}

CLEANED_CLASS_CONTENT_1 = {("Vocabulary", "Farm Animals"): {
    "used_questions": 2,
    "total_questions": 5,
    "list_questions_used": [2, 4]},
    ("Grammar", "Conjuging"): {
    "used_questions": 2,
        "total_questions": 5,
        "list_questions_used": [0, 1]}}

EXTRA_ID_LIST = [2, 4, 11012]
EXTRA_ID_FOLDER_FILE = "Vocabulary/Farm Animals"


#############
### Tests ###
#############

### Test get list classes ###

@patch("mcq_maker_tools.tools_class.SETTINGS", MOCK_SETTINGS)
def test_get_list_classes():
    assert sorted(get_list_classes()) == CLASS_LIST


test_get_list_classes()

### Test load class ###

@patch("mcq_maker_tools.tools_class.SETTINGS", MOCK_SETTINGS)
@patch("mcq_maker_tools.tools_database.SETTINGS", MOCK_SETTINGS)
def test_load_class():
    assert load_class("Classe 1") == CLASS_CONTENT_1


test_load_class()

### Test complete and filter class content ###

@patch("mcq_maker_tools.tools_class.SETTINGS", MOCK_SETTINGS)
@patch("mcq_maker_tools.tools_database.SETTINGS", MOCK_SETTINGS)
def test_complete_and_filter_class_content():
    assert complete_and_filter_class_content({}) == COMPLETED_EMPTY_CLASS
    assert complete_and_filter_class_content(
        WRONG_CLASS) == COMPLETED_EMPTY_CLASS


test_complete_and_filter_class_content()

### Test clean class content from empty lines ###

def test_clean_class_content_from_empty_lines():
    assert clean_class_content_from_empty_lines(
        CLASS_CONTENT_1) == CLEANED_CLASS_CONTENT_1


test_clean_class_content_from_empty_lines()

### Test save class ###

@patch("mcq_maker_tools.tools_class.SETTINGS", MOCK_SETTINGS)
@patch("mcq_maker_tools.tools_database.SETTINGS", MOCK_SETTINGS)
def test_save_class():
    save_class("Classe 3", CLASS_CONTENT_1)
    assert sorted(get_list_classes()) == CLASS_LIST + ["Classe 3"]


test_save_class()

### Test reset class ###

@patch("mcq_maker_tools.tools_class.SETTINGS", MOCK_SETTINGS)
@patch("mcq_maker_tools.tools_database.SETTINGS", MOCK_SETTINGS)
def test_reset_class():
    reset_class("Classe 3")
    assert load_class("Classe 3") == COMPLETED_EMPTY_CLASS


test_reset_class()
os.remove(MOCK_PATH_CLASS + "Classe 3.json")

### Test clean unused ids ###

@patch("mcq_maker_tools.tools_class.SETTINGS", MOCK_SETTINGS)
@patch("mcq_maker_tools.tools_database.SETTINGS", MOCK_SETTINGS)
def test_clean_unused_ids():
    assert clean_unused_question_ids(
        EXTRA_ID_LIST, EXTRA_ID_FOLDER_FILE) == [2, 4]


test_clean_unused_ids()
