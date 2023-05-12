from kivy.uix.screenmanager import Screen
from qcm_maker_tools.tools import DICT_LANGUAGE, PATH_LOGO_64
from qcm_maker_tools.tools_kivy import ImprovedPopup, Image, DICT_BUTTONS

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
