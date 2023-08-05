"""
Module import window of MCQMaker

Create the class for the import window and build the associated kv file.

Classes
-------
ImportWindow : Screen
    Screen used for the import menu.
"""


###############
### Imports ###
###############

import os

### Kivy imports ###

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import (
    ObjectProperty,
    StringProperty,
    BooleanProperty
)

from tkinter.filedialog import askopenfilename

### Module imports ###

from mcq_maker_tools.tools import (
    DICT_LANGUAGE,
    PATH_KIVY_FOLDER,
    MCQ_IMPORT_EXT
)
from mcq_maker_tools.tools_database import (
    get_list_database_files,
    get_list_database_folders
)
from mcq_maker_tools.tools_import import (
    open_pdf,
    open_docx,
    open_file,
    analyse_content,
    create_text_repr_for_mcq
)
from mcq_maker_tools.tools_kivy import (
    DICT_MESSAGES,
    create_standard_popup
)


#################
### Main menu ###
#################


class ImportWindow(Screen):
    """
    Class displaying the import menu.
    """

    TEXT_IMPORT = DICT_LANGUAGE["import"]

    # Initialise the list of folders available
    list_folders = ObjectProperty([])
    valid_analysis = BooleanProperty(True)
    mcq_data = []

    def __init__(self, **kw):
        super().__init__(**kw)

    def init_screen(self):
        # Bind functions
        self.ids.import_mcq.on_release = self.import_mcq
        self.ids.launch_analysis.on_release = self.launch_analysis
        self.ids.transfert_mcq_database.on_release = self.transfer_mcq_database

        self.list_folders = [
            self.manager.FOLDER_SPINNER_DEFAULT] + \
            get_list_database_folders()
        self.list_files = [self.manager.FILE_SPINNER_DEFAULT]

    def import_mcq(self):
        """
        Open the file explorer to allow the user to choose a file and import
        its text in the associated text input.
        """

        # Open the file explorer
        file_to_open = askopenfilename(title=self.TEXT_IMPORT["choose_import_file"],
                                       initialdir=".")

        # Extract the content of the file given its extension
        extension = os.path.splitext(file_to_open)[1]
        extension = extension.lower()

        if extension == ".pdf":
            raw_content = open_pdf(file_to_open)
        elif extension in (".docx", ".doc"):
            raw_content = open_docx(file_to_open)
        else:
            raw_content = open_file(file_to_open)

        # Set the text in the text input
        self.ids.content_mcq.text = raw_content

        # Open the popup to show completion
        create_standard_popup(DICT_MESSAGES["sucess_import_mcq"][1],
                              DICT_MESSAGES["sucess_import_mcq"][0])

    def launch_analysis(self):
        self.mcq_data = analyse_content(
            self.ids.content_mcq.text,
            has_solutions=self.ids.contains_answers.active)

        self.ids.report_analysis.text = create_text_repr_for_mcq(self.mcq_data)

        if self.valid_analysis:
            self.ids.folders_spinner.focus = True

    def update_file_name(self, folder_name):
        self.ids.file_name_input.text = ""

        # Default value where to choose the folder
        if folder_name == self.manager.FOLDER_SPINNER_DEFAULT:
            self.ids.file_name_input.disabled = True
            self.ids.folders_spinner.focus = True
            return

        # Real folder selected
        else:
            self.ids.file_name_input.disabled = False
            self.ids.file_name_input.focus = True

    def enable_database_transfert(self):
        folder_name = self.ids.folders_spinner.text
        file_name = self.ids.file_name_input.text
        # If the file name does not already exists
        if self.valid_analysis and file_name not in get_list_database_files(folder_name):
            self.ids.transfert_mcq_database.disabled = False

    def transfer_mcq_database(self):
        dict_init_database = {
            "folder_name": self.ids.folders_spinner.text,
            "file_name": self.ids.file_name_input.text,
            "mcq_data": self.mcq_data
        }
        self.manager.current = "database"
        self.manager.initialise_screen(dict_init_database=dict_init_database)

### Build associated kv file ###


Builder.load_file(PATH_KIVY_FOLDER + "ImportWindow.kv")
