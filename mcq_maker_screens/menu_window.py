"""
Module menu window of MCQMaker

Create the class for the menu window and build the associated kv file.

Classes
-------
MenuWindow : Screen
    Screen used for the main menu.
"""


###############
### Imports ###
###############

### Python imports ###

import os
from functools import partial

### Kivy imports ###

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock

### Module imports ###

from mcq_maker_tools.tools import (
    DICT_LANGUAGE,
    PATH_LOGO_64,
    PATH_KIVY_FOLDER,
    SETTINGS,
    update_settings
)
from mcq_maker_tools.tools_kivy import (
    DICT_BUTTONS,
    DICT_MESSAGES,
    ImprovedPopup,
    Image
)


#################
### Main menu ###
#################


class MenuWindow(Screen):
    """
    Class displaying the main menu.
    """

    TEXT_MENU = DICT_LANGUAGE["menu"]

    def __init__(self, **kw):
        super().__init__(**kw)

        # Show the popup to indicate the location of the instructions
        if SETTINGS["show_instructions"]:
            Clock.schedule_once(self.create_instruction_popup)
        else:
            Clock.schedule_once(self.verify_and_warn_missing_folders)

    def verify_and_warn_missing_folders(self, *args):
        folder_to_check = ("path_export", "path_class", "path_database")
        missing_folders_text = "\n\n"

        # Check if the folders exist
        for folder in folder_to_check:
            if not os.path.exists(SETTINGS[folder]):
                missing_folders_text += f"- {self.TEXT_MENU[folder]} : {SETTINGS[folder]}\n"

        if missing_folders_text != "\n\n":
            # Create a folder to warn the user
            popup = ImprovedPopup(
                title=DICT_MESSAGES["missing_folders"][0],
                add_content=[])

            # Add the list of missing folders
            popup.add_label(
                text=DICT_MESSAGES["missing_folders"][1] +
                missing_folders_text,
                pos_hint={"x": 0.1, "y": 0.2},
                size_hint=(0.8, 0.75)
            )

            # Add the close button
            popup.add_button(
                text=DICT_BUTTONS["close"],
                pos_hint={"x": 0.2, "y": 0.1},
                size_hint=(0.6, 0.15),
                on_release=popup.dismiss
            )

    def create_instruction_popup(self, *args):
        """
        Create the popup to indicate where are located the user guides.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        # Create the popup
        popup = ImprovedPopup(
            title=DICT_MESSAGES["instruction_information"][0],
            add_content=[])

        # Add the label and both buttons
        popup.add_label(
            text=DICT_MESSAGES["instruction_information"][1],
            pos_hint={"x": 0.1, "y": 0.7},
            size_hint=(0.8, 0.15)
        )
        checkbox = popup.add_checkbox(
            text=DICT_MESSAGES["instruction_information"][2],
            pos_hint={"x": 0.2, "y": 0.5},
            size_hint_label=(0.8, 0.05)
        )
        popup.add_button(
            text=DICT_BUTTONS["close"],
            pos_hint={"x": 0.2, "y": 0.25},
            size_hint=(0.6, 0.15),
            on_release=partial(
                self.save_user_choice_instructions, popup, checkbox)
        )
        Clock.schedule_once(self.verify_and_warn_missing_folders)

    def save_user_choice_instructions(self, popup, popup_checkbox):
        """
        Save the choice of the user to show again the popup for instructions.

        Parameters
        ----------
        popup : ImprovedPopup
            Previous popup to close.

        popup_checkbox : LabelledCheckbox
            Checkbox indicating if the user wants to see this popup again or not.

        Returns
        -------
        None
        """

        global SETTINGS
        popup.dismiss()
        SETTINGS = update_settings(
            SETTINGS, "show_instructions", not popup_checkbox.ids.checkbox.active)

    def display_credits(self):
        """
        Display the credits in a popup.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        # Create the layout of the popup composed of the label
        popup_messages = self.TEXT_MENU["credits_popup"]
        popup_content = [
            ("label", {
                "text": popup_messages["label_popup"],
                "pos_hint": {"x": 0.1, "y": 0.7},
                "size_hint": (0.8, 0.15)
            }
            )
        ]

        # Create the popup
        popup = ImprovedPopup(
            title=popup_messages["title_popup"],
            add_content=popup_content)

        # Add the logo
        popup.add_other_widget(
            Image,
            source=PATH_LOGO_64,
            pos_hint={"x": 0.2, "y": 0.3},
            size_hint=(0.6, 0.35)
        )

        # Add the close button
        popup.add_button(
            text=DICT_BUTTONS["close"],
            pos_hint={"x": 0.2, "y": 0.1},
            size_hint=(0.6, 0.15),
            on_release=popup.dismiss
        )


### Build associated kv file ###

Builder.load_file(PATH_KIVY_FOLDER + "MenuWindow.kv")
