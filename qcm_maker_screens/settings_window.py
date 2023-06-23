"""
Module settings window of MCQMaker

Create the class for the settings window and build the associated kv file.

Classes
-------
SettingsWindow : Screen
    Screen used for the settings menu.
"""


###############
### Imports ###
###############


### Python imports ###

from typing import Literal
from functools import partial

### Kivy imports ###

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty

### Module imports ###

from qcm_maker_tools.tools import (
    PATH_KIVY_FOLDER,
    DICT_LANGUAGE
)

###############
### Process ###
###############


### Settings Window ###

class SettingsWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    TEXT_SETTINGS = DICT_LANGUAGE["settings"]
    return_button_text = TEXT_SETTINGS["return_button"]
    choose_language_label = TEXT_SETTINGS["choose_language"]
    default_language = StringProperty("")
    choose_export_folder = TEXT_SETTINGS["choose_export_folder"]
    choose_class_folder = TEXT_SETTINGS["choose_class_folder"]
    choose_database_folder = TEXT_SETTINGS["choose_database_folder"]
    list_languages = ObjectProperty([])

    def init_screen(self):
        self.ids.language_spinner.focus = True
        self.list_languages = ["French", "English"] # PAUL mettre la fonction get_list_languages()
        self.default_language = "French" # PAUL get_default_language()
        self.ids.choose_export_folder_button.on_release = partial(
            self.open_file_explorer, "export"
        )
        self.ids.choose_class_folder_button.on_release = partial(
            self.open_file_explorer, "class"
        )
        self.ids.choose_database_folder_button.on_release = partial(
            self.open_file_explorer, "database"
        )

    def change_language(self):
        language = self.ids.language_spinner.text
        print(language)
        # PAUL créer une popup de confirmation pour reset l'application et changer la langue dans les settings

    def open_file_explorer(self, mode: Literal["export", "class", "database"]):
        print(mode) # PAUL


### Build associated kv file ###

Builder.load_file(PATH_KIVY_FOLDER + "SettingsWindow.kv")
