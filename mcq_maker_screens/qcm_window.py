"""
Module MCQ window of MCQMaker

Create the class for the MCQ window and build the associated kv file.

Classes
-------
QCMWindow : Screen
    Screen used for the MCQ menu.
"""

###############
### Imports ###
###############


### Python imports ###

# Import of partial
from functools import partial

# Import of file opener
from tkinter.filedialog import askopenfilename

# Import of thread
from threading import Thread

import sys

sys.path.append(".")

### Kivy imports ###

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty, NumericProperty

### Module imports ###

from mcq_maker_tools.tools import (
    JSON_FILETYPES,
    SETTINGS,
    PATH_KIVY_FOLDER,
    extract_filename_from_path,
    get_config_list,
    load_config,
    save_config,
    update_settings,
    platform_name,
    DIR_PATH
)
from mcq_maker_tools.tools_class import (
    get_list_classes,
    load_class,
    complete_and_filter_class_content
)
from mcq_maker_tools.tools_database import (
    get_list_database_files,
    get_list_database_folders,
    get_nb_questions
)
from mcq_maker_tools.tools_docx import (
    get_list_templates
)
from mcq_maker_tools.tools_enhanced_print import (
    print_error
)
from mcq_maker_tools.tools_export import (
    launch_export_QCM
)
from mcq_maker_tools.tools_kivy import (
    DICT_LANGUAGE,
    DICT_MESSAGES,
    DICT_BUTTONS,
    ImprovedPopup,
    create_standard_popup,
    LoadDialog,
    Popup
)
from mcq_maker_tools.tools_scrollview import (
    DICT_KEY_WIDGETS,
    SVLayout,
    build_scroll_view_dict_default_line
)


################
### QCM menu ###
################


class QCMWindow(Screen):
    """
    Class displaying the menu to create a QCM.
    """

    def __init__(self, **kw):
        super().__init__(**kw)
        self.scroll_view_layout = None

    TEXT_MCQ = DICT_LANGUAGE["qcm"]
    NEW_CONFIG = TEXT_MCQ["left_menu"]["new_config"]
    nb_questions_label = TEXT_MCQ["left_menu"]["number_questions_label"]
    global_questions = NumericProperty(0)
    number_total_questions = StringProperty("/0")
    list_folders = ObjectProperty([])
    list_files = ObjectProperty([])
    list_classes = ObjectProperty([])
    list_templates = ObjectProperty([])
    class_content = {}
    CONFIG_TEMP = "temp"
    bool_new_config = True
    current_template = StringProperty("")
    ratio_scrollview = 0.7

    ### Tool menu on the left ###

    def init_screen(self):
        """
        Initialise the screen of the MCQ menu.
        It attributes to all buttons the corresponding functions.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.ids.load_button.on_release = self.open_load_config_popup
        self.ids.save_config_button.on_release = self.save_config
        self.ids.generate_qcm_button.on_release = self.configure_mcq_generation
        self.ids.add_button.on_release = self.add_database
        self.update_screen()
        self.load_class_data(class_name=None)

    def update_screen(self):
        """
        Update the list of all spinners of the screen, when the screen is loaded.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.list_classes = [self.manager.CLASSES_SPINNER_DEFAULT] + \
            get_list_classes()
        self.list_templates = [self.manager.TEMPLATE_SPINNER_DEFAULT] + \
            get_list_templates()
        self.list_folders = [self.manager.FOLDER_SPINNER_DEFAULT] + \
            get_list_database_folders()
        self.list_files = [self.manager.FILE_SPINNER_DEFAULT]

        # Update the default value of the template
        if SETTINGS["default_template"] in self.list_templates:
            self.current_template = SETTINGS["default_template"]
        else:
            self.current_template = self.manager.TEMPLATE_SPINNER_DEFAULT

    def open_load_config_popup(self):
        """
        Open a popup to load a configuration.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Create the layout of the popup composed of the label
        popup_messages = self.TEXT_MCQ["load_config"]
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

        # Add the three buttons, to create a new config, load a former and close the window
        popup.add_button(
            text=popup_messages["new_config"],
            pos_hint={"x": 0.1, "y": 0.4},
            size_hint=(0.35, 0.15),
            on_release=partial(self.new_config, popup)
        )
        popup.add_button(
            text=popup_messages["choose_config"],
            pos_hint={"x": 0.55, "y": 0.4},
            size_hint=(0.35, 0.15),
            on_release=partial(self.open_file_explorer, popup)
        )
        popup.add_button(
            text=DICT_BUTTONS["close"],
            pos_hint={"x": 0.2, "y": 0.1},
            size_hint=(0.6, 0.15),
            on_release=popup.dismiss
        )

    def new_config(self, popup, *args):
        """
        Display a new configuration in the scroll view.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.bool_new_config = True
        self.ids.config_name_input.focus = True
        self.ids.config_name_input.text = ""
        self.ids.classes_spinner.text = self.manager.CLASSES_SPINNER_DEFAULT
        self.ids.classes_spinner.disabled = False
        self.global_questions = 0
        popup.dismiss()
        self.build_scroll_view({})

    def open_file_explorer(self, popup, *args):
        """
        Open the file explorer when the user has chosen to load a configuration.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.sto_popup = popup
        if platform_name == "Darwin":
            self.show_load()
        else:
            file_explorer_value = askopenfilename(
                title=self.TEXT_MCQ["load_file"],
                filetypes=JSON_FILETYPES
            )
            self.open_file_explorer_process(file_explorer_value=file_explorer_value)
        
    def dismiss_popup(self):
        self._popup.dismiss()
    
    def show_load(self):
        content = LoadDialog(load=self.open_file_explorer_process,
                             cancel=self.dismiss_popup,
                             default_path=DIR_PATH,
                             load_label=self.TEXT_MCQ["load"],
                             cancel_label=self.TEXT_MCQ["cancel"],
                             filters_list=["*.json"])
        self._popup = Popup(title=self.TEXT_MCQ["load_file"], content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
    
    def open_file_explorer_process(self,path, filename, file_explorer_value =None):

        if file_explorer_value is None:
            file_explorer_value = filename[0]
            self.dismiss_popup()

        if file_explorer_value == "":
            return
        else:
            self.get_config(extract_filename_from_path(file_explorer_value))
            self.sto_popup.dismiss()

    def get_config(self, config_name):
        """
        Get the configuration, when it has been chosen in the file explorer.
        It launches its display on the scroll view.

        Parameters
        ----------
        config_name: str
            Name of the chosen configuration

        Returns
        -------
        None
        """
        self.bool_new_config = False
        class_name = self.ids.classes_spinner.text
        # Load the configuration
        try:
            config = load_config(config_name)
        except:
            create_standard_popup(
                title_popup=DICT_MESSAGES["error_load_config"][0],
                message=DICT_MESSAGES["error_load_config"][1]
            )
            return

        if config_name != self.CONFIG_TEMP:
            # Change the name of the config in the text input
            self.ids.config_name_input.text = config_name

        # Verify that there are less questions asked than available questions
        if class_name != self.manager.CLASSES_SPINNER_DEFAULT:
            for question in config["questions"]:
                # TODO normalement on peut enlever ça avec les \n
                folder_name = question["folder_name"].replace("\n", " ")
                file_name = question["file_name"].replace("\n", " ")
                total_questions = self.class_content[
                    (folder_name, file_name)]["total_questions"] - self.class_content[
                    (folder_name, file_name)]["used_questions"]
                bool_nb_questions = question["nb_questions"] <= total_questions

                # When there are too many questions, put the max
                if not bool_nb_questions:
                    question["nb_questions"] = total_questions

        # Reset the total number of questions
        self.global_questions = 0

        # Display the configuration on the screen
        self.build_scroll_view(config=config)

    def extract_config(self, config_name, raise_warning=True):
        """
        Extract the configuration from all widgets.

        Parameters
        ----------
        None

        Returns
        -------
        config: dict
        """
        global SETTINGS

        # Check if there is configuration
        if self.scroll_view_layout is None:
            if raise_warning:
                create_standard_popup(
                    title_popup=DICT_MESSAGES["error_config"][0],
                    message=DICT_MESSAGES["error_config"][1]
                )
                print_error(DICT_MESSAGES["error_config"][1])
            raise ValueError()

        # Extract the template
        template = self.ids.template_spinner.text
        if template == self.manager.TEMPLATE_SPINNER_DEFAULT:
            template = None
        SETTINGS = update_settings(SETTINGS, "default_template", template)

        config = {
            "QCM_name": config_name,
            "questions": [],
            "template": template,
            "mix_all_questions": self.ids.mix_all_questions.active,
            "mix_among_databases": self.ids.mix_inside_questions.active,
            "update_class": self.ids.modify_class.active
        }
        # Extract the configuration from the scroll view
        list_content = self.scroll_view_layout.extract_scroll_view_content()

        # Reformat the content extracted from the scroll view to fit the config format
        for config_line in list_content:
            nb_questions = 0
            if config_line["nb_questions"] != "":
                nb_questions = int(config_line["nb_questions"])
            if nb_questions != 0:
                config_line.pop("total_questions")
                config_line["nb_questions"] = nb_questions
                config["questions"].append(config_line)
        return config

    def reload_class(self, class_name):
        """
        Load the content of the class.

        Parameters
        ----------
        class_name: str
            Name of the chosen class

        Returns
        -------
        None
        """
        if class_name == self.manager.CLASSES_SPINNER_DEFAULT:
            class_name = None
            self.ids.modify_class.active = False
        else:
            self.ids.modify_class.active = True

            temp_name = self.CONFIG_TEMP

            no_load = False
            # Save the actual configuration
            try:
                save_config(
                    config_name=temp_name,
                    config=self.extract_config(temp_name, raise_warning=False)
                )
            except ValueError:
                no_load = True

            # Load the data of the class
            self.load_class_data(class_name)

            if no_load == False:
                # Reload the configuration
                self.get_config(config_name=temp_name)

    def load_class_data(self, class_name):
        """
        Load the data of the chosen class.

        Parameters
        ----------
        class_name : str
            Name of the class

        Returns
        -------
        None
        """
        if class_name is None or class_name == self.manager.CLASSES_SPINNER_DEFAULT:
            class_name = None
            self.ids.modify_class.active = False
        else:
            # Get the content of the class
            self.ids.modify_class.active = True
        self.class_content = load_class(class_name)

    def check_mix_questions(self, mix_type):
        if mix_type == "inside":
            is_active = self.ids.mix_inside_questions.active
            if not is_active and self.ids.mix_all_questions.active:
                self.ids.mix_all_questions.active = False
        elif mix_type == "all":
            is_active = self.ids.mix_all_questions.active
            if is_active and not self.ids.mix_inside_questions.active:
                self.ids.mix_inside_questions.active = True

    def overwrite_config(self, popup, *args):
        self.bool_new_config = False
        popup.dismiss()
        self.save_config()

    def check_name_config(self):
        config_name = self.ids.config_name_input.text
        if config_name == "":
            create_standard_popup(
                message=DICT_MESSAGES["error_no_name_config"][1],
                title_popup=DICT_MESSAGES["error_no_name_config"][0],
            )
            print_error(DICT_MESSAGES["error_no_name_config"][0])
            raise ValueError()
        config = self.extract_config(config_name)
        return config, config_name

    def save_config(self):
        """
        Launch the save of the config or the generation of the MCQ, according to the given boolean.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Extract the config if it has a valid name
        try:
            config, config_name = self.check_name_config()
        except ValueError:
            return

        # Unset the focus
        self.ids.save_config_button.focus = False

        # Get the list of already used config names
        config_list = get_config_list()

        # Check the overwrite of another configuration
        if self.bool_new_config and config_name in config_list:
            # Create the popup
            popup = ImprovedPopup(
                title=DICT_MESSAGES["error_name_double_config"][0],
                add_content=[])

            # Add the label, the progress bar and the button to close the window
            popup.add_label(
                text=DICT_MESSAGES["error_name_double_config"][1],
                pos_hint={"x": 0.1, "y": 0.6},
                size_hint=(0.8, 0.15)
            )
            popup.add_button(
                text=DICT_BUTTONS["yes"],
                pos_hint={"x": 0.1, "y": 0.25},
                size_hint=(0.35, 0.15),
                on_release=partial(self.overwrite_config, popup)
            )
            popup.add_button(
                text=DICT_BUTTONS["no"],
                pos_hint={"x": 0.55, "y": 0.25},
                size_hint=(0.35, 0.15),
                on_release=popup.dismiss
            )
            return
        # Save the configuration in a json file
        save_config(
            config_name=config_name,
            config=config)
        # Display popup to confirm the success of the save
        create_standard_popup(
            message=DICT_MESSAGES["success_save_config"][1],
            title_popup=DICT_MESSAGES["success_save_config"][0],
        )

    def configure_mcq_generation(self):
        # Extract the config if it has a valid name
        try:
            config, config_name = self.check_name_config()
        except ValueError:
            return

        # Unset the focus
        self.ids.generate_qcm_button.focus = False

        popup_messages = self.TEXT_MCQ["qcm_configuration"]
        # Create the popup
        popup = ImprovedPopup(
            title=popup_messages["title_popup"],
            add_content=[])

        # Add the label, the 4 checkbox and the 2 buttons
        popup.add_label(
            text=popup_messages["label_popup"],
            pos_hint={"x": 0.1, "y": 0.7},
            size_hint=(0.8, 0.15)
        )
        # Txt checkbox
        txt_checkbox = popup.add_checkbox(
            pos_hint={"x": 0.1, "y": 0.55},
            text=popup_messages["txt"],
            size_hint_label=(0.35, 0.05)
        )
        # H5p checkbox
        h5p_checkbox = popup.add_checkbox(
            pos_hint={"x": 0.55, "y": 0.55},
            text=popup_messages["h5p"],
            size_hint_label=(0.35, 0.05)
        )
        disabled = False
        if config["template"] is None:
            disabled = True
        # Docx checkbox
        docx_checkbox = popup.add_checkbox(
            pos_hint={"x": 0.1, "y": 0.45},
            disabled=disabled,
            text=popup_messages["docx"],
            size_hint_label=(0.35, 0.05)
        )
        # Xml checkbox
        xml_checkbox = popup.add_checkbox(
            pos_hint={"x": 0.55, "y": 0.45},
            text=popup_messages["xml"],
            size_hint_label=(0.35, 0.05)
        )
        # Set the default values of the checkbox, according to the last configuration.
        dict_exports_kivy = {
            "txt": txt_checkbox,
            "docx": docx_checkbox,
            "h5p": h5p_checkbox,
            "xml": xml_checkbox
        }
        for key in dict_exports_kivy:
            if SETTINGS["dict_exports"][key]:
                dict_exports_kivy[key].ids.checkbox.active = True

        # Generation button
        popup.add_button(
            text=popup_messages["launch_generation"],
            pos_hint={"x": 0.1, "y": 0.15},
            size_hint=(0.35, 0.15),
            on_release=partial(
                self.open_popup_generation_mcq,
                config,
                popup,
                dict_exports_kivy)
        )
        # Cancel button
        popup.add_button(
            text=popup_messages["cancel"],
            pos_hint={"x": 0.55, "y": 0.15},
            size_hint=(0.35, 0.15),
            on_release=popup.dismiss
        )

    def process_dict_format(self, dict_exports_kivy):
        global SETTINGS
        dict_exports = {}
        for key in dict_exports_kivy:
            dict_exports[key] = dict_exports_kivy[key].ids.checkbox.active
        # Update the settings
        update_settings(
            SETTINGS, "dict_exports", dict_exports)
        return dict_exports

    def open_popup_generation_mcq(self, config, popup, dict_checkbox):
        popup.dismiss()
        class_name = self.ids.classes_spinner.text
        if class_name == self.manager.CLASSES_SPINNER_DEFAULT:
            class_name = None
        dict_formats = self.process_dict_format(dict_checkbox)
        popup_messages = self.TEXT_MCQ["qcm_generation"]
        # Create the popup
        popup = ImprovedPopup(
            title=popup_messages["title_popup"],
            add_content=[])

        # Add the label, the progress bar and the button to close the window
        label_popup = popup.add_label(
            text=popup_messages["label_popup"],
            pos_hint={"x": 0.1, "y": 0.7},
            size_hint=(0.8, 0.15)
        )
        progress_bar = popup.add_progress_bar(
            pos_hint={"x": 0.2, "y": 0.4},
            size_hint=(0.6, 0.15)
        )
        close_button = popup.add_button(
            text=DICT_BUTTONS["close"],
            pos_hint={"x": 0.2, "y": 0.1},
            size_hint=(0.6, 0.15),
            on_release=popup.dismiss,
            disabled=True
        )

        # Launch the generation of the QCM in txt, docx, h5p et xml
        thread = Thread(
            target=self.thread_export,
            args=(config, class_name, dict_formats, progress_bar,
                  close_button, label_popup, popup)
        )
        thread.start()

    def reset_after_generation(self, *args, **kwargs):
        self.reset_side_menu()
        self.reset_tool_menu_top()
        self.scroll_view_layout.reset_screen()

    def thread_export(self, config, class_name, dict_formats, progress_bar, close_button, label_popup, popup):
        """
        Function to control the thread of the export
        """

        # Export the QCM
        success = launch_export_QCM(
            config=config,
            class_name=class_name,
            dict_formats=dict_formats,
            progress_bar=progress_bar,
            close_button=close_button,
            label_popup=label_popup,
            popup=popup)

        # Reset screen
        if success:
            Clock.schedule_once(self.reset_after_generation)

    def reset_side_menu(self):
        """
        Reset the menu on the left.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.ids.config_name_input.text = ""
        self.ids.classes_spinner.text = self.manager.CLASSES_SPINNER_DEFAULT
        self.global_questions = 0
        self.load_class_data(class_name=None)

    ### Tool menu at the top ###

    def reset_tool_menu_top(self):
        """
        Reset the top right part of the MCQ menu.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.ids.folders_spinner.text = self.manager.FOLDER_SPINNER_DEFAULT
        self.ids.files_spinner.text = self.manager.FILE_SPINNER_DEFAULT
        self.ids.files_spinner.disabled = True
        self.list_files = [self.manager.FILE_SPINNER_DEFAULT]
        self.ids.nb_questions_input.disabled = True
        self.ids.nb_questions_input.hint_text = ""
        self.ids.nb_questions_input.text = ""
        self.number_total_questions = "/0"
        self.ids.add_button.disabled = True

    def update_list_files(self, folder_name):
        """
        Update the list of files available in the spinner when a folder has been selected.

        Parameters
        ----------
        folder_name: str
            The name of the selected folder

        Returns
        -------
        None
        """
        # Default value where to choose the folder
        if folder_name == self.manager.FOLDER_SPINNER_DEFAULT:
            self.reset_tool_menu_top()
            self.ids.folders_spinner.focus = True
            return

        # Real folder selected
        self.ids.nb_questions_input.disabled = True
        self.ids.nb_questions_input.hint_text = ""
        self.number_total_questions = "/0"
        self.ids.add_button.disabled = True
        self.ids.files_spinner.disabled = False
        self.ids.files_spinner.text = self.manager.FILE_SPINNER_DEFAULT
        self.ids.files_spinner.focus = True
        # Update the list of files according to the selected folder
        self.list_files = [self.manager.FILE_SPINNER_DEFAULT] + \
            get_list_database_files(
                self.ids.folders_spinner.text,
                exclusion_list=self.get_keys_scroll_view())

    def get_keys_scroll_view(self):
        """
        Get the list of folders and files already contained in the scroll view in order to delete them for the list of files.
        The couple (folder_name, file_name) is called "key".

        Parameters
        ----------
        None

        Returns
        -------
        list_keys: list
            The list of couples (folder_name, file_name) used in the scroll view.
        """
        list_keys = []
        if self.scroll_view_layout is not None:
            sv_content = self.scroll_view_layout.extract_scroll_view_content()
            for line in sv_content:
                list_keys.append((line["folder_name"], line["file_name"]))
        return list_keys

    def update_nb_questions_top_menu(self, folder_name, file_name):
        """
        Update the number of questions available when the file has been selected.

        Parameters
        ----------
        folder_name: str
            Name of the selected folder

        file_name: str
            Name of the selected file

        Returns
        -------
        None
        """
        if file_name != self.manager.FILE_SPINNER_DEFAULT:
            self.ids.nb_questions_input.disabled = False
            self.ids.nb_questions_input.text = ""
            self.ids.nb_questions_input.hint_text = self.TEXT_MCQ[
                "top_menu"]["hint_text_number_questions"]
            self.ids.nb_questions_input.focus = True
            self.ids.add_button.disabled = True

            folder_name = folder_name.replace("\n", " ")
            file_name = file_name.replace("\n", " ")

            # Get the number of questions available
            question_class_dict = self.class_content[(folder_name, file_name)]
            total_questions = question_class_dict["total_questions"]
            used_questions = question_class_dict["used_questions"]
            self.number_total_questions = "/" + str(
                total_questions - used_questions
            )

    def verify_nb_questions(self, instance, text, total_questions):
        """
        Check if the value entered in the text input containing the number of questions to use is correct.

        Parameters
        ----------
        instance: TextInput
            Kivy text input whose value has been changed by the user

        text: str
            The value entered in the text input

        total_questions: int
            The number of questions available

        Returns
        -------
        nb_questions: int
            The correct number of questions.
            It equals 0 when the value in the text input is not valid.
        """
        if text == "":
            nb_questions = 0
            instance.last_value = 0
        else:
            try:
                nb_questions = int(text)
                instance.last_value = nb_questions
                if nb_questions > int(total_questions) or nb_questions < 0:
                    nb_questions = 0
                    instance.last_value = 0
                    instance.text = ""
            except:
                nb_questions = 0
                instance.last_value = 0
                instance.text = ""
        return nb_questions

    def change_nb_questions(self, instance):
        """
        Change the number of questions entered in the text input of the top menu when it's incorrect.
        It disables the button to add the current line in the scroll view when it's incorrect.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        nb_questions = self.verify_nb_questions(
            instance=instance,
            text=instance.text,
            total_questions=int(self.number_total_questions.replace("/", ""))
        )
        # Enable or disable the button to add the line in the scroll view
        if nb_questions != 0:
            self.ids.add_button.disabled = False
        else:
            self.ids.add_button.disabled = True

    def add_database(self):
        """
        Add the selected database in the scroll view.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        nb_questions = int(self.ids.nb_questions_input.text)
        total_questions = int(
            str(self.number_total_questions).replace("/", ""))
        config_line = {
            "folder_name": self.ids.folders_spinner.text,
            "file_name": self.ids.files_spinner.text,
            "nb_questions": nb_questions
        }

        # Add the new line in the scroll view
        if self.scroll_view_layout is not None:
            dict_line = self.create_dict_line(
                config_line=config_line,
                total_questions=total_questions
            )
            self.scroll_view_layout.display_new_line(dict_line=dict_line)
            self.global_questions += nb_questions
        else:
            self.build_scroll_view(
                config={"questions": [config_line]})

        # Reset the top menu
        self.reset_tool_menu_top()
        self.ids.folders_spinner.focus = True

    def update_number_questions(self, total_questions, instance, text):
        last_value = instance.last_value
        nb_questions = self.verify_nb_questions(
            instance=instance,
            text=text,
            total_questions=total_questions
        )
        # Update the total number of questions
        self.global_questions += nb_questions - int(last_value)

    def create_dict_line(self, config_line, total_questions):
        """
        Create the dictionary of the line of the configuration to display in the SV.

        Parameters
        ----------
        config_line: dict
            The configuration of a specific line

        total_questions: int
            Total number of questions of the line

        Returns
        -------
        dict_line: dict
            It contains ll the specifications of the widgets in the line to display.
        """
        dict_line = {}
        dict_line["folder_name"] = {
            "text": config_line["folder_name"]
        }
        dict_line["file_name"] = {
            "text": config_line["file_name"]
        }
        nb_questions = config_line["nb_questions"]
        dict_line["nb_questions"] = {
            "text": str(nb_questions),
            "function": partial(self.update_number_questions, total_questions)
        }
        dict_line["total_questions"] = {
            "text": "/" + str(total_questions)
        }
        return dict_line

    def build_scroll_view(self, config):
        """
        Build the layout of the scroll view to display the config.

        Parameters
        ----------
        config : dict
            Configuration to display

        Returns
        -------
        None
        """
        # Create the dictionary of the default line
        self.dict_default_line = {}
        self.dict_default_line["folder_name"] = build_scroll_view_dict_default_line(
            x_size=0.32,
            x_pos=0.05
        )
        self.dict_default_line["file_name"] = build_scroll_view_dict_default_line(
            x_size=0.32,
            x_pos=0.39
        )
        self.dict_default_line["nb_questions"] = build_scroll_view_dict_default_line(
            key_widget=DICT_KEY_WIDGETS["TEXT_INPUT"],
            x_size=0.1,
            x_pos=0.74,
            other_keys={
                "multiline": False,
                "placeholder": self.TEXT_MCQ["top_menu"]["hint_text_number_questions"]
            }
        )
        self.dict_default_line["total_questions"] = build_scroll_view_dict_default_line(
            x_size=0.07,
            x_pos=0.906,
            other_keys={
                "bool_text_size": True
            }
        )

        # Build the list of content of the layout of the scroll view
        self.list_content = []

        # Build the list of content for a loaded config
        if config != {}:
            questions = config["questions"]
            class_name = self.ids.classes_spinner.text
            for counter_line in range(len(questions)):
                question = questions[counter_line]
                folder_name = question["folder_name"].replace("\n", " ")
                file_name = question["file_name"].replace("\n", " ")

                # Get the number of questions available
                if class_name != self.manager.CLASSES_SPINNER_DEFAULT:
                    dict_class_content = self.class_content[
                        (folder_name, file_name)]
                    left_questions = dict_class_content["total_questions"] - \
                        dict_class_content["used_questions"]
                else:
                    left_questions = get_nb_questions(
                        database_name=file_name,
                        database_folder=folder_name
                    )
                self.global_questions += question["nb_questions"]
                dict_line = self.create_dict_line(
                    config_line=question,
                    total_questions=left_questions
                )
                self.list_content.append(dict_line)

        # Remove the scroll view if it already exists (to avoid errors)
        if self.scroll_view_layout != None:
            self.ids.scroll_view_mcq.remove_widget(self.scroll_view_layout)
        # Build and display the layout of the scroll view
        self.scroll_view_layout = SVLayout(
            dict_default_line=self.dict_default_line,
            list_content=self.list_content,
            size_line=30,
            parent_ratio=self.ratio_scrollview)
        self.ids.scroll_view_mcq.add_widget(self.scroll_view_layout)


### Build associated kv file ###

Builder.load_file(PATH_KIVY_FOLDER + "QCMWindow.kv")
