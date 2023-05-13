"""
Main script to launch QCMMaker
"""

__version__ = "4.0.1"


###############
### Imports ###
###############


### Kivy imports ###

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.uix.gridlayout import GridLayout


### Modules imports ###

from qcm_maker_tools import *
# Necessary import for the .kv
import qcm_maker_screens


######################
### Global classes ###
######################


class TabsLayout(GridLayout):
    """
    Class displaying the menu with the three tabs for each window.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos_hint = {"x": 0, "y": 0.925}
        self.size_hint = (1, 0.075)
        self.cols = 3

    # Global variables for tabs
    tabs_values = DICT_LANGUAGE["generic"]["tabs"]


###############
### General ###
###############


class WindowManager(ScreenManager):
    """
    Screen manager, which allows the navigations between the different menus.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.highlight_text_color = highlight_text_color
        self.button_blue_color = (
            2 * blue_color[0], 2 * blue_color[1], 2 * blue_color[2], blue_color[3])
        self.button_pink_color = (
            2 * pink_color[0], 2 * pink_color[1], 2 * pink_color[2], pink_color[3])
        self.button_disabled_color = (
            382 / 255, 382 / 255, 382 / 255, 1)
        self.pink_color = pink_color
        self.blue_color = blue_color
        self.color_label = color_label
        self.transition = NoTransition()

    # Global variables for spinners
    spinners_default_value = DICT_LANGUAGE["generic"]["spinners_default"]
    FOLDER_SPINNER_DEFAULT = spinners_default_value["folders"]
    FILE_SPINNER_DEFAULT = spinners_default_value["files"]
    CLASSES_SPINNER_DEFAULT = spinners_default_value["classes"]
    TEMPLATE_SPINNER_DEFAULT = spinners_default_value["templates"]

    def initialise_screen(self):
        """
        Initialise the new screen at each change

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if self.current in ["qcm", "database", "classes"]:
            self.get_screen(self.current).init_screen()


class MCQMakerApp(App):
    """
    Main class of the application.
    """

    def build(self):
        """
        Build the application.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        Window.clearcolor = background_color
        self.icon = PATH_LOGO_64


# Run the application
if __name__ == "__main__":
    Builder.load_file(PATH_KIVY_FOLDER + "extended_style.kv")
    MyApp = MCQMakerApp()
    MyApp.run()
