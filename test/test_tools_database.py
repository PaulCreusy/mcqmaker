"""
Test module of tools database
"""

###############
### Imports ###
###############

import sys
sys.path.append(".")

from mock import patch

from mcq_maker_tools.tools_database import (
    get_list_database_folders,
    get_list_database_files,
    get_database_tree,
    load_database,
    get_nb_questions,
    save_database,
    delete_file,
    create_database_folder,
    delete_folder
)

######################
### Test variables ###
######################

# Define paths
PATH_TEST_DATA_FOLDER = "test/data/"
MOCK_PATH_QUESTIONS = PATH_TEST_DATA_FOLDER + "Questions/"
MOCK_SETTINGS = {"path_database": MOCK_PATH_QUESTIONS}

# Correct structure of the database
FOLDERS_LIST = ["Grammar", "Vocabulary"]
FOLDERS_LIST_WITH_SF = ["Grammar", "Science Fiction", "Vocabulary"]
FILES_LIST_GRAMMAR = ["Conjuging", "Past and perfect"]
FILES_LIST_GRAMMAR_EXCL = ["Past and perfect"]
GRAMMAR_EXCL = [("Grammar", "Conjuging")]
FILES_LIST_VOCABULARY = ["Complete Sentences", "Farm Animals"]
TREE = {"Grammar": FILES_LIST_GRAMMAR, "Vocabulary": FILES_LIST_VOCABULARY}

# Content of the database quiz
CONJUGING_CONTENT = [
    {
        "id": 0,
        "question": "What is the correct conjugation of the verb \"to eat\" in the present tense for the pronoun \"he\"?",
        "options": [
            "eat",
            "eats",
            "eating",
            "ate"
        ],
        "answer": 0
    },
    {
        "id": 1,
        "question": "Which option correctly conjugates the verb \"to write\" in the past tense for the pronoun \"I\"?",
        "options": [
            "writing",
            "write",
            "wrote",
            "writed"
        ],
        "answer": 2
    },
    {
        "id": 2,
        "question": "Choose the correct present tense conjugation of the verb \"to swim\" for the pronoun \"they.\"",
        "options": [
            "swam",
            "swim",
            "swims",
            "swimming"
        ],
        "answer": 1
    },
    {
        "id": 3,
        "question": "What is the proper past tense conjugation of the verb \"to run\" for the pronoun \"she\"?",
        "options": [
            "run",
            "running",
            "runs",
            "ran"
        ],
        "answer": 3
    },
    {
        "id": 4,
        "question": "Select the correct conjugation of the verb \"to dance\" in the future tense for the pronoun \"we.\"",
        "options": [
            "danced",
            "dance",
            "dances",
            "will dance"
        ],
        "answer": 1
    }
]

############
### Test ###
############

### Test get list database folders ###

@patch("mcq_maker_tools.tools_database.SETTINGS", MOCK_SETTINGS)
def test_get_list_database_folders():
    assert get_list_database_folders() == FOLDERS_LIST


test_get_list_database_folders()

### Test get list database files ###

@patch("mcq_maker_tools.tools_database.SETTINGS", MOCK_SETTINGS)
def test_get_list_database_files():
    assert get_list_database_files("Vocabulary") == FILES_LIST_VOCABULARY
    assert get_list_database_files(
        "Grammar", exclusion_list=GRAMMAR_EXCL) == FILES_LIST_GRAMMAR_EXCL
    assert get_list_database_files(
        "Grammar") == FILES_LIST_GRAMMAR


test_get_list_database_files()

### Test get database tree ###

@patch("mcq_maker_tools.tools_database.SETTINGS", MOCK_SETTINGS)
def test_get_database_tree():
    assert get_database_tree() == TREE


test_get_database_tree()

### Test load database ###

@patch("mcq_maker_tools.tools_database.SETTINGS", MOCK_SETTINGS)
def test_load_database():
    assert load_database("Conjuging", "Grammar") == CONJUGING_CONTENT


test_load_database()

### Test get nb questions ###

@patch("mcq_maker_tools.tools_database.SETTINGS", MOCK_SETTINGS)
def test_get_nb_questions():
    assert get_nb_questions("Conjuging", "Grammar") == 5
    assert get_nb_questions("Complete Sentences", "Vocabulary") == 10


test_get_nb_questions()

### Test save database ###

@patch("mcq_maker_tools.tools_database.SETTINGS", MOCK_SETTINGS)
def test_save_database():
    save_database("Conjuging_test_save", "Grammar", CONJUGING_CONTENT)
    assert load_database("Conjuging_test_save", "Grammar") == CONJUGING_CONTENT


test_save_database()

### Test delete file ###

@patch("mcq_maker_tools.tools_database.SETTINGS", MOCK_SETTINGS)
def test_delete_file():
    delete_file("Grammar", "Conjuging_test_save")
    assert get_list_database_files("Grammar") == FILES_LIST_GRAMMAR


test_delete_file()

### Test create database folder ###

@patch("mcq_maker_tools.tools_database.SETTINGS", MOCK_SETTINGS)
def test_create_database_folder():
    create_database_folder("Science Fiction")
    assert get_list_database_folders() == FOLDERS_LIST_WITH_SF


test_create_database_folder()

### Test delete folder ###

@patch("mcq_maker_tools.tools_database.SETTINGS", MOCK_SETTINGS)
def test_delete_folder():
    delete_folder("Science Fiction")
    assert get_list_database_folders() == FOLDERS_LIST


test_delete_folder()
