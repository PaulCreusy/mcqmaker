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


### Kivy imports ###

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty

### Module imports ###

from mcq_maker_tools.tools import (
    DICT_LANGUAGE,
    PATH_KIVY_FOLDER
)
from mcq_maker_tools.tools_database import (
    get_list_database_files,
    get_list_database_folders
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
        print("import mcq")

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
