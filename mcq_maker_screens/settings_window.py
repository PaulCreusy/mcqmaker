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

import os
from typing import Literal
from functools import partial

# Import of file opener
from tkinter.filedialog import askdirectory

### Kivy imports ###

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty

### Module imports ###

from mcq_maker_tools.tools import (
    PATH_KIVY_FOLDER,
    PATH_SETTINGS,
    SETTINGS,
    DICT_CORR_LANGUAGES,
    __version__,
    save_json_file,
    get_current_language,
    get_list_languages,
    change_path
)
from mcq_maker_tools.tools_kivy import (
    DICT_LANGUAGE,
    DICT_MESSAGES,
    DICT_BUTTONS,
    ImprovedPopup,
    create_standard_popup
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
    default_language = StringProperty(get_current_language())
    choose_export_folder = TEXT_SETTINGS["choose_export_folder"]
    choose_class_folder = TEXT_SETTINGS["choose_class_folder"]
    choose_database_folder = TEXT_SETTINGS["choose_database_folder"]
    export_folder = StringProperty(SETTINGS["path_export"])
    class_folder = StringProperty(SETTINGS["path_class"])
    database_folder = StringProperty(SETTINGS["path_database"])
    list_languages = ObjectProperty(get_list_languages())
    version = TEXT_SETTINGS["version"] + " " + __version__
    former_language = SETTINGS["language"]
    boolean_popup_language = False

    def init_screen(self):
        """
        Init the settings menu.

        Parameters
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

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if not self.boolean_popup_language:
            language = self.ids.language_spinner.text
            for key in DICT_CORR_LANGUAGES:
                if language == DICT_CORR_LANGUAGES[key]:
                    language = key
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
                on_release=partial(self.reset_language, popup)
            )
        self.boolean_popup_language = False

    def reset_language(self, popup):
        """
        Reset the language of the spinner if the user doesn't want to change it.

        Parameters
        ----------
        popup: ImprovedPopup
            Popup of confirmation to dismiss.

        Returns
        -------
        None
        """
        popup.dismiss()
        self.boolean_popup_language = True
        self.ids.language_spinner.text = DICT_CORR_LANGUAGES[self.former_language]

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

        Parameters
        ----------
        mode: Literal["export", "class", "database"]
            String corresponding to the type of folder to choose.

        Returns
        -------
        None
        """
        current_dir = os.getcwd().replace("\\", "/")
        folder_path = askdirectory(
            title=self.TEXT_SETTINGS["choose_folder"], initialdir=current_dir)
        folder_path = folder_path.replace(current_dir, ".") + "/"
        # Change in the display
        if mode == "export":
            self.export_folder = folder_path
        elif mode == "class":
            self.class_folder = folder_path
        elif mode == "database":
            self.database_folder = folder_path
        create_standard_popup(
            DICT_MESSAGES["success_change_dir"][1],
            DICT_MESSAGES["success_change_dir"][0])
        change_path(mode, folder_path)


### Build associated kv file ###

Builder.load_file(PATH_KIVY_FOLDER + "SettingsWindow.kv")
