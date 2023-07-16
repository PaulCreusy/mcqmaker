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
from kivy.properties import ObjectProperty, BooleanProperty

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
        print("import mcq")

    def launch_analysis(self):
        # PAUL
        print(self.ids.contains_answers.active)
        print(self.ids.content_mcq.text)
        print("launch analysis")
        # TODO => change the variable self.valid_analysis and self.mcq_data
        self.mcq_data = [{'question': 'In winter accidents happen quite .... on the roads.', 'answer': 0, 'options': [' frequently', ' quietly', 'frequent', 'sometimes']}, {'question': 'Although they are brother and sister, they ...speak to each other these days. ', 'answer': 1, 'options': [' hardy ', ' hardly ', ' strictly ', ' mainly']}, {'question': 'He goes to London every....week.', 'answer': 2, 'options': [' two', 'another', 'other', 'both']}, {'question': 'He drives.....', 'answer': 0, 'options': [' pretty fast', 'nicely fast ', 'quick ', 'enough fast']}, {'question': 'At the meeting, the manager talked....about the need for better attendance and punctuality.', 'answer': 3, 'options': ['briefing ', 'shortly ', 'shorts ', 'briefly']}, {'question': 'Hard work.....pays off.', 'answer': 1, 'options': ['advertises ', 'eventually ', 'never ', 'will sometimes']}, {'question': 'I guess he is.... 30.', 'answer': 1, 'options': ['approximatively ', 'approximately ', 'more the less ', 'an average of']}, {'question': 'With this beautiful blue sky, it is very ....to rain, isn’t it?', 'answer': 3, 'options': ['probable', 'likely', 'improbable', 'unlikely']}, {'question': 'He has just lost his contact lens but it is.... be found. How very strange!', 'answer': 3, 'options': ['somewhere', 'anywhere', 'nothing', 'nowhere']}, {'question': 'Who said we were.....?', 'answer': 2, 'options': ['whole like', 'all like', 'all alike', 'whole alike']}]

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
