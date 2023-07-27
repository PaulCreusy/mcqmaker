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
    StringProperty
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
    open_file
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
    list_files = ObjectProperty([])

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
        # PAUL
        print(self.ids.content_mcq.text)
        print("launch analysis")

        # TODO si l'analyse est valide
        self.ids.folders_spinner.focus = True

    def update_list_files(self, folder_name):

        # Default value where to choose the folder
        if folder_name == self.manager.FOLDER_SPINNER_DEFAULT:
            self.list_files = [self.manager.FILE_SPINNER_DEFAULT]
            self.ids.files_spinner.text = self.manager.FILE_SPINNER_DEFAULT
            self.ids.files_spinner.disabled = True
            self.ids.folders_spinner.focus = True
            return

        # Real folder selected
        self.init_screen_existing_folder(
            list_files=[self.manager.FILE_SPINNER_DEFAULT] +
            get_list_database_files(folder_name))

    def init_screen_existing_folder(self, list_files):
        self.ids.files_spinner.disabled = False
        self.ids.files_spinner.text = self.manager.FILE_SPINNER_DEFAULT
        self.ids.files_spinner.focus = True
        # Update the list of files according to the selected folder
        self.list_files = list_files

    def enable_database_transfert(self):
        # TODO mettre la condition si l'analyse est valide
        self.ids.transfert_mcq_database.disabled = False
        self.ids.transfert_mcq_database.focus = True

    def transfer_mcq_database(self):
        # PAUL
        self.manager.current = "database"
        self.manager.initialise_screen()

### Build associated kv file ###


Builder.load_file(PATH_KIVY_FOLDER + "ImportWindow.kv")
