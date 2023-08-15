"""
Test module of tools export
"""

###############
### Imports ###
###############

import os
import shutil
import sys
sys.path.append(".")

from mock import patch

from mcq_maker_tools.tools_export import (
    generate_MCQ,
    create_folder_MCQ,
    export_MCQ_txt,
    export_MCQ_docx,
    export_MCQ_H5P_text_fill_blanks,
    export_MCQ_H5P_text_single_choice,
    export_MCQ_moodle,
    launch_export_MCQ
)

######################
### Test variables ###
######################

# Define the paths
PATH_TEST_DATA_FOLDER = "./test/data/"
MOCK_PATH_CLASS = PATH_TEST_DATA_FOLDER + "Classes/"
MOCK_PATH_QUESTIONS = PATH_TEST_DATA_FOLDER + "Questions/"
MOCK_PATH_EXPORT = PATH_TEST_DATA_FOLDER + "Export/"

MOCK_SETTINGS = {"path_class": MOCK_PATH_CLASS,
                 "path_database": MOCK_PATH_QUESTIONS,
                 "path_export": MOCK_PATH_EXPORT}

PATH_TEMPLATE = PATH_TEST_DATA_FOLDER + "default_template.docx"

### Mock the kivy progress bar ###

class FalseProgressBar:
    def __init__(self) -> None:
        self.value = 0


MOCK_PROGRESS_BAR = FalseProgressBar()

### Define the parameters to generate the MCQ ###

CONFIG_1 = {
    'QCM_name': 'Test',
    'questions': [{'folder_name': 'Grammar', 'file_name': 'Conjuging', 'nb_questions': 2},
                  {'folder_name': 'Vocabulary', 'file_name': 'Farm Animals', 'nb_questions': 2}],
    'template': "default_template",
    'mix_all_questions': False,
    'mix_among_databases': False,
    'update_class': False}

CLASS_CONTENT_1 = {
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

NEW_CLASS_CONTENT_1 = {
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
        "list_questions_used": [0, 1]},
    ("Vocabulary", "Complete Sentences"): {
        "used_questions": 0,
        "total_questions": 10,
        "list_questions_used": []}
}

RESULT_1 = {
    "QCM_name": "Test",
    "template": "default_template",
    "questions": [
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
            "id": 0,
            "question": "Which farm animal is known for producing wool and is often associated with the phrase \"baa baa\"?",
            "options": [
                "Cow",
                "Horse",
                "Pig",
                "Sheep"
            ],
            "answer": 3
        },
        {
            "id": 1,
            "question": "This farm animal is often used to plow fields and pull heavy loads. It has a distinctive hump on its back. What is it?",
            "options": [
                "Goat",
                "Donkey",
                "Chicken",
                "Camel"
            ],
            "answer": 3
        }
    ]
}

RESULT_1_FIB = {
    "QCM_name": "Test",
    "template": "default_template",
    "questions": [
        {
            "id": 0,
            "question": "What is the correct conjugation of the verb \"to eat\" in the present tense for the pronoun \"he\"? ... ",
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
            "question": "Which option correctly conjugates the verb \"to write\" in the past tense for the pronoun \"I\"? ... ",
            "options": [
                "writing",
                "write",
                "wrote",
                "writed"
            ],
            "answer": 2
        },
        {
            "id": 0,
            "question": "Which farm animal is known for producing wool and is often associated with the phrase \"baa baa\"? ... ",
            "options": [
                "Cow",
                "Horse",
                "Pig",
                "Sheep"
            ],
            "answer": 3
        },
        {
            "id": 1,
            "question": "This farm animal is often used to plow fields and pull heavy loads. It has a distinctive hump on its back. What is it? ... ",
            "options": [
                "Goat",
                "Donkey",
                "Chicken",
                "Camel"
            ],
            "answer": 3
        }
    ]
}

#############
### Tests ###
#############

### Test generate MCQ ###

@patch("mcq_maker_tools.tools_class.SETTINGS", MOCK_SETTINGS)
@patch("mcq_maker_tools.tools_database.SETTINGS", MOCK_SETTINGS)
def test_generate_MCQ():
    TEST_RESULT, TEST_CLASS_CONTENT = generate_MCQ(
        CONFIG_1, CLASS_CONTENT_1)
    assert TEST_RESULT == RESULT_1
    assert TEST_CLASS_CONTENT == NEW_CLASS_CONTENT_1


### Test create folder MCQ ###

@patch("mcq_maker_tools.tools_class.SETTINGS", MOCK_SETTINGS)
@patch("mcq_maker_tools.tools_database.SETTINGS", MOCK_SETTINGS)
@patch("mcq_maker_tools.tools_export.SETTINGS", MOCK_SETTINGS)
def test_create_folder_MCQ():
    create_folder_MCQ(RESULT_1)
    create_folder_MCQ(RESULT_1)
    assert sorted(os.listdir(MOCK_PATH_EXPORT)) == sorted(
        ["Test", "Test_1", "blank.txt"])
    shutil.rmtree(MOCK_PATH_EXPORT + "Test")
    shutil.rmtree(MOCK_PATH_EXPORT + "Test_1")


### Test export MCQ txt ###

@patch("mcq_maker_tools.tools_class.SETTINGS", MOCK_SETTINGS)
@patch("mcq_maker_tools.tools_database.SETTINGS", MOCK_SETTINGS)
@patch("mcq_maker_tools.tools_export.SETTINGS", MOCK_SETTINGS)
def test_export_MCQ_txt():
    export_MCQ_txt(RESULT_1, MOCK_PATH_EXPORT, MOCK_PROGRESS_BAR)
    assert sorted(os.listdir(MOCK_PATH_EXPORT)) == sorted([
        "Test.txt", "Test_solution.txt", "blank.txt"])
    os.remove(MOCK_PATH_EXPORT + "Test.txt")
    os.remove(MOCK_PATH_EXPORT + "Test_solution.txt")


### Test export MCQ docx ###

@patch("mcq_maker_tools.tools_class.SETTINGS", MOCK_SETTINGS)
@patch("mcq_maker_tools.tools_database.SETTINGS", MOCK_SETTINGS)
@patch("mcq_maker_tools.tools_export.SETTINGS", MOCK_SETTINGS)
@patch("mcq_maker_tools.tools_export.PATH_TEMPLATE_FOLDER", PATH_TEST_DATA_FOLDER)
def test_export_MCQ_docx():
    export_MCQ_docx(RESULT_1, MOCK_PATH_EXPORT, MOCK_PROGRESS_BAR)
    assert sorted(os.listdir(MOCK_PATH_EXPORT)) == sorted(
        ["Test.docx", "blank.txt"])
    os.remove(MOCK_PATH_EXPORT + "Test.docx")


### Test export MCQ xml ###

@patch("mcq_maker_tools.tools_class.SETTINGS", MOCK_SETTINGS)
@patch("mcq_maker_tools.tools_database.SETTINGS", MOCK_SETTINGS)
@patch("mcq_maker_tools.tools_export.SETTINGS", MOCK_SETTINGS)
def test_export_MCQ_moodle():
    export_MCQ_moodle(RESULT_1, MOCK_PATH_EXPORT, MOCK_PROGRESS_BAR)
    assert sorted(os.listdir(MOCK_PATH_EXPORT)) == sorted(
        ["Test.xml", "blank.txt"])
    os.remove(MOCK_PATH_EXPORT + "Test.xml")


### Test export MCQ H5P fill in the blanks ###

@patch("mcq_maker_tools.tools_class.SETTINGS", MOCK_SETTINGS)
@patch("mcq_maker_tools.tools_database.SETTINGS", MOCK_SETTINGS)
@patch("mcq_maker_tools.tools_export.SETTINGS", MOCK_SETTINGS)
def test_export_MCQ_H5P_text_fill_blanks():
    export_MCQ_H5P_text_fill_blanks(
        RESULT_1_FIB, MOCK_PATH_EXPORT, MOCK_PROGRESS_BAR)
    assert sorted(os.listdir(MOCK_PATH_EXPORT)) == sorted([
        "Test_H5P_text_fill_in_the_blanks.txt", "blank.txt"])
    os.remove(MOCK_PATH_EXPORT + "Test_H5P_text_fill_in_the_blanks.txt")


### Test export MCQ H5P single choice ###

@ patch("mcq_maker_tools.tools_class.SETTINGS", MOCK_SETTINGS)
@ patch("mcq_maker_tools.tools_database.SETTINGS", MOCK_SETTINGS)
@ patch("mcq_maker_tools.tools_export.SETTINGS", MOCK_SETTINGS)
def test_export_MCQ_H5P_text_single_choice():
    export_MCQ_H5P_text_single_choice(
        RESULT_1, MOCK_PATH_EXPORT, MOCK_PROGRESS_BAR)
    assert sorted(os.listdir(MOCK_PATH_EXPORT)) == sorted([
        "Test_H5P_text_single_choice.txt", "blank.txt"])
    os.remove(MOCK_PATH_EXPORT + "Test_H5P_text_single_choice.txt")


### Run ###
if __name__ == "__main__":
    test_generate_MCQ()
    test_create_folder_MCQ()
    test_export_MCQ_docx()
    test_export_MCQ_txt()
    test_export_MCQ_moodle()
    test_export_MCQ_H5P_text_fill_blanks()
    test_export_MCQ_H5P_text_single_choice()
