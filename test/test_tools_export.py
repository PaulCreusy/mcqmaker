"""
Test module of tools export
"""

###############
### Imports ###
###############

import sys
sys.path.append(".")

from mock import patch

from mcq_maker_tools.tools_class import (
    load_class
)

from mcq_maker_tools.tools_export import (
    generate_QCM,
    create_folder_QCM,
    export_QCM_txt,
    export_QCM_docx,
    export_QCM_H5P_text_fill_blanks,
    export_QCM_H5P_text_single_choice,
    export_QCM_moodle,
    launch_export_QCM
)

######################
### Test variables ###
######################

### Mock the kivy progress bar ###

class FalseProgressBar:
    def __init__(self) -> None:
        self.value = 0


MOCK_PROGRESS_BAR = FalseProgressBar()

### Define the parameters to generate the MCQ ###

CONFIG_1 = ...

CLASS_CONTENT_1 = {
    "class_name": "Classe 1",
    "Grammar/Conjuging": [
        0,
        1
    ],
    "Vocabulary/Farm Animals": [
        2,
        4
    ]
}

RESULT_1 = ...

#############
### Tests ###
#############

# def test_generate_QCM():
#     assert generate_QCM(CONFIG_1, CLASS_CONTENT_1) == RESULT_1
