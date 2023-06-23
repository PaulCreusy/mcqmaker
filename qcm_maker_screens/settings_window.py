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
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty

### Module imports ###

from qcm_maker_tools.tools import (
    PATH_KIVY_FOLDER,
    PATH_SETTINGS,
    SETTINGS,
    save_json_file
)
from qcm_maker_tools.tools_kivy import (
    DICT_LANGUAGE,
    DICT_MESSAGES,
    DICT_BUTTONS,
    ImprovedPopup
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
    default_language = StringProperty("French") # PAUL get_default_language()
    choose_export_folder = TEXT_SETTINGS["choose_export_folder"]
    choose_class_folder = TEXT_SETTINGS["choose_class_folder"]
    choose_database_folder = TEXT_SETTINGS["choose_database_folder"]
    list_languages = ObjectProperty(["French", "English"]) # PAUL mettre la fonction get_list_languages() => METTRE DES MAJUSCULES AU DEBUT C'EST POST-TRAITE APRES

    def init_screen(self):
        """
        Init the settings menu.

        Paramaters
        ----------
        None

        Returns
        -------
        None
        """
        self.ids.language_spinner.focus = True
        self.ids.choose_export_folder_button.on_release = partial(
            self.open_file_explorer, "export"
        )
        self.ids.choose_class_folder_button.on_release = partial(
            self.open_file_explorer, "class"
        )
        self.ids.choose_database_folder_button.on_release = partial(
            self.open_file_explorer, "database"
        )

    def open_confirmation_popup(self):
        """
        Open a popup of confirmation for the change of language.

        Paramaters
        ----------
        None

        Returns
        -------
        None
        """
        language = self.ids.language_spinner.text
        language = language.lower()
        # Create the popup
        popup = ImprovedPopup(
            title=DICT_MESSAGES["change_language"][0],
            add_content=[])

        # Add the label, the progress bar and the button to close the window
        popup.add_label(
            text=DICT_MESSAGES["change_language"][1],
            pos_hint={"x": 0.1, "y": 0.6},
            size_hint=(0.8, 0.15)
        )
        popup.add_button(
            text=DICT_BUTTONS["yes"],
            pos_hint={"x": 0.1, "y": 0.25},
            size_hint=(0.35, 0.15),
            on_release=partial(self.change_language, language, popup)
        )
        popup.add_button(
            text=DICT_BUTTONS["no"],
            pos_hint={"x": 0.55, "y": 0.25},
            size_hint=(0.35, 0.15),
            on_release=popup.dismiss
        )

    def change_language(self, language, popup):
        """
        Change the language of the application in the settings.
        It closes the window at the end of the operation.

        Parameters
        ----------
        language: str
            New language of the application.

        popup: ImprovedPopup
            Popup of confirmation to dismiss.

        Returns
        -------
        None
        """
        popup.dismiss()
        SETTINGS["language"] = language
        save_json_file(
            file_path=PATH_SETTINGS,
            dict_to_save=SETTINGS
        )
        Window.close()

    def open_file_explorer(self, mode: Literal["export", "class", "database"]):
        """
        Open the file explorer to choose the folder.

        Paramaters
        ----------
        mode: Literal["export", "class", "database"]
            String corresponding to the type of folder to choose.

        Returns
        -------
        None
        """
        print(mode) # PAUL


### Build associated kv file ###

Builder.load_file(PATH_KIVY_FOLDER + "SettingsWindow.kv")
