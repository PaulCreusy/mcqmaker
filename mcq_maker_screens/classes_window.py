"""
Module classes window of MCQMaker

Create the class for the classes window and build the associated kv file.

Classes
-------
ClassesWindow : Screen
    Screen used for the classes menu.
"""


###############
### Imports ###
###############


### Kivy imports ###

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty

### Module imports ###

from mcq_maker_tools.tools_kivy import (
    DICT_LANGUAGE,
    DICT_MESSAGES,
    PATH_KIVY_FOLDER
)
from mcq_maker_tools.tools_class import (
    get_list_classes,
    reset_class,
    load_class,
    save_class
)
from mcq_maker_tools.tools_kivy import (
    create_standard_popup
)
from mcq_maker_tools.tools_scrollview import (
    DICT_KEY_WIDGETS,
    SVLayout,
    build_scroll_view_dict_default_line
)


###############
### Process ###
###############


### Classes Window ###

class ClassesWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        # Initialise the scroll view layout to None in order to know if it exists or not
        self.scroll_view_layout = None

    list_classes = ObjectProperty([])
    TEXT_CLASSES = DICT_LANGUAGE["classes"]

    def init_screen(self):
        self.ids.new_class_button.on_release = self.create_new_class
        self.list_classes = [
            self.manager.CLASSES_SPINNER_DEFAULT] + get_list_classes()
        
        # Update the scroll view if a class has been selected
        current_class_name = self.ids.classes_spinner.text
        if current_class_name != self.manager.CLASSES_SPINNER_DEFAULT:
            class_content = load_class(class_name=current_class_name)
            self.build_scroll_view(class_content=class_content)

    def update_classes(self, class_name):
        if class_name == self.manager.CLASSES_SPINNER_DEFAULT:
            self.ids.reset_button.disabled = True
            # Reset the scroll view
            if self.scroll_view_layout != None:
                self.scroll_view_layout.reset_screen()
            return
        self.ids.reset_button.disabled = False

        # Get the content of the class
        class_content = load_class(class_name=class_name)
        self.build_scroll_view(class_content=class_content)

    def reset_class(self):
        # Remove the content of the layout of the scroll view
        self.scroll_view_layout.reset_screen()
        class_name = self.ids.classes_spinner.text
        self.ids.reset_button.disabled = True
        self.ids.classes_spinner.text = self.manager.CLASSES_SPINNER_DEFAULT
        # Reset the data of the class
        reset_class(class_name)
        create_standard_popup(
            message=DICT_MESSAGES["success_reset_class"][1],
            title_popup=DICT_MESSAGES["success_reset_class"][0],
        )

    def create_new_class(self):
        """
        Create the new class, if the name entered by the user is valid.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Remove the content of the layout of the scroll view
        if self.scroll_view_layout is not None:
            self.scroll_view_layout.reset_screen()
        class_name = self.ids.new_class_input.text
        class_name_lower = class_name.lower()
        list_classes_lower = [item.lower() for item in self.list_classes]
        # When the name is already taken
        if class_name_lower in list_classes_lower:
            create_standard_popup(
                message=DICT_MESSAGES["error_create_class"][1],
                title_popup=DICT_MESSAGES["error_create_class"][0]
            )
            return
        # Create the new class
        save_class(class_name, {})
        create_standard_popup(
            message=DICT_MESSAGES["success_create_class"][1],
            title_popup=DICT_MESSAGES["success_create_class"][0]
        )
        self.ids.new_class_input.text = ""
        self.ids.classes_spinner.text = self.manager.CLASSES_SPINNER_DEFAULT
        self.list_classes = [
            self.manager.CLASSES_SPINNER_DEFAULT] + get_list_classes()

    def build_scroll_view(self, class_content):
        # Create the dictionary of the default line
        self.dict_default_line = {}
        self.dict_default_line["label_folder"] = build_scroll_view_dict_default_line(
            x_size=0.2,
            x_pos=0.0375
        )
        self.dict_default_line["label_file"] = build_scroll_view_dict_default_line(
            x_size=0.2,
            x_pos=0.2625
        )
        self.dict_default_line["label_questions"] = build_scroll_view_dict_default_line(
            x_size=0.1,
            x_pos=0.5375
        )
        self.dict_default_line["progress_bar"] = build_scroll_view_dict_default_line(
            key_widget=DICT_KEY_WIDGETS["PROGRESS_BAR"],
            x_size=0.3125,
            x_pos=0.65
        )

        # Sort by folder name then file name
        list_keys_class_content = list(class_content.keys())
        list_keys_class_content.sort(
            key=lambda key_class_content:
            (key_class_content[0], key_class_content[1]))
        list_folders = []

        # Build the list of content of the layout of the scroll view
        self.list_content = []
        for key in list_keys_class_content:
            dict_line = {}
            # Get the name of the folder and do not display one twice
            label_folder_text = ""
            folder_name = key[0]
            if folder_name not in list_folders:
                list_folders.append(folder_name)
                label_folder_text = folder_name
            dict_line["label_folder"] = {
                "text": label_folder_text
            }
            dict_line["label_file"] = {
                "text": key[1]
            }
            used_questions = class_content[key]["used_questions"]
            total_questions = class_content[key]["total_questions"]
            dict_line["label_questions"] = {
                "text": str(used_questions) + "/" + str(total_questions)
            }
            dict_line["progress_bar"] = {
                "value": used_questions,
                "max_value": total_questions
            }
            self.list_content.append(dict_line)

        # Remove the scroll view if it already exists (to avoid errors)
        if self.scroll_view_layout != None:
            self.ids.scroll_view_classes.remove_widget(self.scroll_view_layout)
        # Build and display the layout of the scroll view
        self.scroll_view_layout = SVLayout(
            dict_default_line=self.dict_default_line,
            list_content=self.list_content,
            size_line=40)
        self.ids.scroll_view_classes.add_widget(self.scroll_view_layout)


### Build associated kv file ###

Builder.load_file(PATH_KIVY_FOLDER + "ClassesWindow.kv")
