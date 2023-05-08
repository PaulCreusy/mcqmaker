"""
Main script to launch QCMMaker
"""

__version__ = "4.0.0"


###############
### Imports ###
###############


### Kivy imports ###

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty

### Python imports ###

from functools import partial
from tkinter.filedialog import askopenfilename
from threading import Thread

### Modules imports ###

from qcm_maker_tools import *


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


################
### QCM menu ###
################


class QCMWindow(Screen):
    """
    Class displaying the menu to create a QCM.
    """

    def __init__(self, **kw):
        global QCMWindowInst
        super().__init__(**kw)
        QCMWindowInst = self
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
        file_explorer_value = askopenfilename(
            title=self.TEXT_MCQ["load_file"],
            filetypes=json_filetypes
        )
        if file_explorer_value == "":
            return
        else:
            self.get_config(extract_filename_from_path(file_explorer_value))
            popup.dismiss()

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
        config = load_config(config_name)

        if config_name != self.CONFIG_TEMP:
            # Change the name of the config in the text input
            self.ids.config_name_input.text = config_name

        # Verify that there are less questions asked than available questions
        if class_name != self.manager.CLASSES_SPINNER_DEFAULT:
            for question in config["questions"]:
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

    def extract_config(self, config_name):
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

        temp_name = self.CONFIG_TEMP

        # Save the actual configuration
        try:
            save_config(
                config_name=temp_name,
                config=self.extract_config(temp_name)
            )
        except ValueError:
            return

        # Load the data of the class
        self.load_class_data(class_name)

        # Reload the configuration
        self.get_config(config_name=temp_name)

    def load_class_data(self, class_name):
        """
        Load the data of the chosen class.

        Parameters
        ----------
        class_name: str
            Name of the class

        Returns
        -------
        None
        """
        if class_name == self.manager.CLASSES_SPINNER_DEFAULT:
            class_name = None
        # Get the content of the class
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

        # PAUL j'ai besoin de ta liste de noms de configs <3
        # Check the overwrite of another configuration
        if self.bool_new_config and config_name in ["test"]:
            # Create the popup
            popup = ImprovedPopup(
                title=DICT_MESSAGES["error_name_double_config"][0],
                add_content=[])

            # Add the label, the progress bar and the button to close the window
            popup.add_label(
                text=DICT_MESSAGES["error_name_double_config"][1],
                pos_hint={"x": 0.1, "y": 0.7},
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
            print(key)
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
        SETTINGS["dict_exports"] = dict_exports
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
            self.reset_side_menu()
            self.reset_tool_menu_top()
            self.scroll_view_layout.reset_screen()

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

    def update_nb_questions(self, folder_name, file_name):
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
        config: dict
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
                    dict_class_content = QCMWindowInst.class_content[
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
            size_line=30)
        self.ids.scroll_view_mcq.add_widget(self.scroll_view_layout)


#####################
### Database menu ###
#####################


class DatabaseWindow(Screen):
    def __init__(self, **kw):
        global DatabaseInst
        super().__init__(**kw)
        DatabaseInst = self

    TEXT_DATABASE = DICT_LANGUAGE["database"]
    NEW_FILE = TEXT_DATABASE["new_file"]
    DICT_SAVE_MESSAGES = TEXT_DATABASE["dict_save_messages"]
    DICT_INPUT_MESSAGES = TEXT_DATABASE["dict_input_messages"]

    # Initialise the list of folders available
    list_folders = ObjectProperty([])
    list_files = ObjectProperty([])
    name_database = StringProperty("")

    def init_screen(self):
        self.ids.folders_spinner.focus = True
        self.ids.save_button.on_release = self.save_database
        self.list_folders = [
            self.manager.FOLDER_SPINNER_DEFAULT,
            self.NEW_FILE] + \
            get_list_database_folders(caracter_limit=15)
        self.list_files = [self.manager.FILE_SPINNER_DEFAULT]

    def partial_reset_after_creation(self):
        # Update the list of files according to the selected folder
        self.list_files = [self.manager.FILE_SPINNER_DEFAULT, self.NEW_FILE] + \
            get_list_database_files(
                folder_name=self.ids.folders_spinner.text)
        self.ids.files_spinner.text = self.name_database
        self.ids.name_database_input.disabled = True
        self.ids.name_database_input.hint_text = ""
        self.ids.save_button.text = self.DICT_SAVE_MESSAGES["edit_database"]

    def update_list_files(self, folder_name):
        # Reset the screen when the selected folder has changed
        SVDatabaseInst.reset_screen()
        self.ids.name_database_input.text = ""

        # Default value where to choose the folder
        if folder_name == self.manager.FOLDER_SPINNER_DEFAULT:
            self.list_files = [self.manager.FILE_SPINNER_DEFAULT]
            self.ids.files_spinner.text = self.manager.FILE_SPINNER_DEFAULT
            self.ids.files_spinner.disabled = True
            self.ids.name_database_input.disabled = True
            self.ids.name_database_input.hint_text = ""
            self.ids.save_button.disabled = True
            self.ids.save_button.text = self.DICT_SAVE_MESSAGES["none"]
            self.ids.folders_spinner.focus = True
            return

        # Create a new folder
        if folder_name == self.NEW_FILE:
            self.list_files = []
            self.ids.files_spinner.text = self.manager.FILE_SPINNER_DEFAULT
            self.ids.files_spinner.disabled = True
            self.ids.name_database_input.disabled = False
            self.ids.name_database_input.hint_text = self.DICT_INPUT_MESSAGES["new_folder"]
            self.ids.save_button.disabled = False
            self.ids.save_button.text = self.DICT_SAVE_MESSAGES["new_folder"]
            self.ids.name_database_input.focus = True
            return

        # Real folder selected
        self.init_screen_existing_folder(
            list_files=[
                self.manager.FILE_SPINNER_DEFAULT, self.NEW_FILE] +
            get_list_database_files(folder_name))

    def init_screen_existing_folder(self, list_files):
        self.ids.name_database_input.disabled = True
        self.ids.name_database_input.hint_text = ""
        self.ids.save_button.disabled = True
        self.ids.save_button.text = ""
        self.ids.files_spinner.disabled = False
        self.ids.files_spinner.text = self.manager.FILE_SPINNER_DEFAULT
        self.ids.files_spinner.focus = True
        # Update the list of files according to the selected folder
        self.list_files = list_files

    def update_scroll_view_database(self, spinner_folder_text, spinner_files_text):
        # If the name of the configuration has not changed, do nothing
        if spinner_files_text == self.name_database:
            return

        # Reset the screen when the selected file has changed
        SVDatabaseInst.reset_screen()

        # Create a new database
        if spinner_files_text == self.NEW_FILE:
            self.ids.name_database_input.disabled = False
            self.ids.name_database_input.hint_text = self.DICT_INPUT_MESSAGES["new_file"]
            self.ids.name_database_input.text = ""
            self.ids.name_database_input.focus = True
            self.ids.save_button.disabled = False
            self.ids.save_button.text = self.DICT_SAVE_MESSAGES["new_file"]
            SVDatabaseInst.initialise_database(spinner_folder_text, "")
            return

        if spinner_files_text == self.manager.FILE_SPINNER_DEFAULT:
            self.ids.name_database_input.hint_text = ""
            self.ids.name_database_input.disabled = True
            self.ids.name_database_input.text = ""
            self.ids.save_button.disabled = True
            self.ids.save_button.text = self.DICT_SAVE_MESSAGES["none"]
            self.ids.files_spinner.focus = True
            return

        # Edit a former database
        self.ids.name_database_input.disabled = True
        self.ids.name_database_input.hint_text = ""
        self.ids.save_button.disabled = False
        self.ids.save_button.text = self.DICT_SAVE_MESSAGES["edit_database"]
        self.name_database = spinner_files_text
        SVDatabaseInst.initialise_database(
            spinner_folder_text, spinner_files_text)

    def save_database(self):
        button_text = self.ids.save_button.text
        if button_text == self.DICT_SAVE_MESSAGES["new_folder"]:
            name_folder = self.ids.name_database_input.text
            name_folder_lower = name_folder.lower()
            list_folders_lower = [item.lower()
                                  for item in self.ids.folders_spinner.values]
            if name_folder_lower not in list_folders_lower:
                # Create the new folder
                create_database_folder(name_folder)
                self.ids.folders_spinner.values.append(name_folder)
                self.ids.folders_spinner.text = name_folder
                self.init_screen_existing_folder(
                    list_files=[
                        self.manager.FILE_SPINNER_DEFAULT, self.NEW_FILE])
            else:
                # Create an error popup if the name is already taken
                create_standard_popup(
                    message=DICT_MESSAGES["error_name_double_folder"][1],
                    title_popup=DICT_MESSAGES["error_name_double_folder"][0]
                )
            return

        if button_text == self.DICT_SAVE_MESSAGES["new_file"]:
            # Update the name of the database
            self.name_database = self.ids.name_database_input.text

            if self.name_database == "":
                create_standard_popup(
                    message=DICT_MESSAGES["error_no_name_database"][1],
                    title_popup=DICT_MESSAGES["error_no_name_database"][0]
                )
                return

            name_database_lower = self.name_database.lower()
            list_files_lower = [item.lower() for item in self.list_files]
            if name_database_lower in list_files_lower:
                create_standard_popup(
                    message=DICT_MESSAGES["error_name_double_database"][1],
                    title_popup=DICT_MESSAGES["error_name_double_database"][0]
                )
                return

        # Create the list of content
        content = []
        for key in SVDatabaseInst.dict_widgets_database:
            dict_line = SVDatabaseInst.dict_widgets_database[key]
            if dict_line["question"].text != "":
                dict_content = {
                    "id_line": dict_line["id_line"].text,
                    "question": dict_line["question"].text,
                    "options": [],
                    "answer": ""
                }
                list_options = dict_line["options"]
                # Get the options in the right order (so they are always display in the same order in the scroll view)
                for counter_option in range(len(list_options) - 1, -1, -1):
                    option = list_options[counter_option]
                    if option[0].text != "":
                        if option[1].active:
                            dict_content["answer"] = len(
                                list_options) - 1 - counter_option
                        dict_content["options"].append(option[0].text)
                if dict_content["answer"] == "":
                    create_standard_popup(
                        message=DICT_MESSAGES["error_selected_answer"][1] +
                        dict_content["id_line"] + ".",
                        title_popup=DICT_MESSAGES["error_selected_answer"][0]
                    )
                    return
                content.append(dict_content)

        # Save the database in the new file
        save_database(
            database_name=self.name_database,
            database_folder=self.ids.folders_spinner.text,
            content=content
        )

        create_standard_popup(
            message=self.DICT_SAVE_MESSAGES["save_succeed_text"],
            title_popup=self.DICT_SAVE_MESSAGES["save_succeed_title"]
        )

        # Reset partially the screenwhen creating a new database
        if button_text == self.DICT_SAVE_MESSAGES["new_file"]:
            self.partial_reset_after_creation()


class DatabaseScrollView(FloatLayout):
    """
    Class displaying the scrollview to edit the database.
    """

    def __init__(self, **kwargs):
        global SVDatabaseInst
        super().__init__(**kwargs)
        self.delete_function_dict = {}
        SVDatabaseInst = self

    number_lines = ObjectProperty(0)
    size_line = ObjectProperty(40)
    dict_widgets_database = {}
    default_question_content = {
        "question": "",
        "options": ["", ""],
        "answer": None
    }
    add_question_button = None

    def reset_screen(self):
        # Remove all widgets
        for key in self.dict_widgets_database:
            dict_line = self.dict_widgets_database[key]
            self.remove_widget(dict_line["id_line"])
            self.remove_widget(dict_line["question"])
            self.remove_widget(dict_line["delete"])
            self.remove_widget(dict_line["add_option"])
            for counter_option in range(len(dict_line["options"])):
                self.remove_widget(dict_line["options"][counter_option][0])
                self.remove_widget(dict_line["options"][counter_option][1])
        # Remove the button to add a new question
        if self.add_question_button != None:
            self.remove_widget(self.add_question_button)
            self.add_question_button = None
        self.number_lines = 0
        self.dict_widgets_database = {}
        self.delete_function_dict = {}

    def initialise_database(self, folder_name, file_name):
        # Delete all widgets of the screen
        self.reset_screen()

        # Add each question
        if file_name != "":
            # Get the content of the database to edit
            list_content, error_list = load_database(file_name, folder_name)
            nb_questions = len(list_content)
            for counter_line in range(nb_questions):
                dict_content = list_content[counter_line]
                self.add_question(
                    counter_line=counter_line,
                    dict_content=dict_content
                )
            if len(error_list) > 0:
                error_string = str(error_list.pop(0) + 1)
                for e in error_list:
                    error_string += ", " + str(e + 1)
                create_standard_popup(
                    message=DICT_MESSAGES["error_load_db"][1] + error_string,
                    title_popup=DICT_MESSAGES["error_load_db"][0]
                )
        else:
            self.add_question(
                counter_line=0,
                dict_content=self.default_question_content
            )

        # Add the button to add new questions
        self.switch_lines_top(len(self.dict_widgets_database.keys()), 1)
        self.add_question_button = create_button_scrollview_simple(
            button_text="+",
            x_size=0.055,
            size_vertical=self.size_line,
            x_pos=0.0375,
            y_pos=1.1 * self.size_line
        )
        self.add_question_button.on_release = partial(
            self.new_question,
            self.default_question_content
        )
        self.add_widget(self.add_question_button)
        self.number_lines += 1

    def new_question(self, dict_content):
        text_input_question = self.add_question(
            counter_line=len(self.dict_widgets_database.keys()),
            dict_content=dict_content,
            bool_new_question=True
        )
        text_input_question.focus = True
        self.remove_widget(self.add_question_button)
        self.add_widget(self.add_question_button)

    def picolo(self, *args, **kwargs):
        print("picolo")

    def delete_question(self, *args, question_id=0, **kwargs):

        # Recover the widgets of the question
        temp_dict_widgets = self.dict_widgets_database[question_id]

        # Remove them
        for key in list(temp_dict_widgets.keys()):
            if key != "options":
                self.remove_widget(temp_dict_widgets[key])
            else:
                number_widgets = 2 + len(temp_dict_widgets["options"])
                for el in temp_dict_widgets["options"]:
                    for e in el:
                        self.remove_widget(e)

        # Pop the dict out of the widgets database

        for i in list(self.dict_widgets_database.keys()):
            if i > question_id:
                self.dict_widgets_database[i -
                                           1] = self.dict_widgets_database[i]
                self.delete_function_dict[i - 1] = self.delete_function_dict[i]
                self.dict_widgets_database.pop(i)
                self.delete_function_dict.pop(i)
            elif i == question_id:
                self.dict_widgets_database.pop(i)
                self.delete_function_dict.pop(i)

        for i in self.dict_widgets_database:
            current_dict_widgets = self.dict_widgets_database[i]
            # print(current_dict_widgets, i)
            current_dict_widgets["id_line"].text = str(i + 1) + "."
            current_dict_widgets["delete"].unbind(
                on_press=self.delete_function_dict[i])
            new_delete_function = partial(
                self.delete_question, question_id=i)
            self.delete_function_dict[i] = new_delete_function
            current_dict_widgets["delete"].bind(
                on_press=self.delete_function_dict[i])

        self.switch_lines_bottom(start_counter=question_id,
                                 number_switch=number_widgets)
        self.number_lines -= number_widgets

    def add_question(self, counter_line, dict_content, bool_new_question=False):
        offset = 0
        if bool_new_question:
            offset = 1.1 * self.size_line
        number_options = len(dict_content["options"])
        number_widgets = 2 + number_options

        label_id = create_label_scrollview_simple(
            label_text=str(counter_line + 1) + ".",
            x_size=0.05,
            size_vertical=self.size_line,
            x_pos=0.0375,
            y_pos=number_widgets * 1.1 * self.size_line + offset
        )
        self.add_widget(label_id)

        text_input_question = create_text_input_scrollview_simple(
            input_text=dict_content["question"],
            x_size=0.7,
            size_vertical=self.size_line,
            x_pos=0.1,
            y_pos=number_widgets * 1.1 * self.size_line + offset,
            placeholder=DatabaseInst.TEXT_DATABASE["placeholder_question"],
            write_tab=False,
            multiline=False
        )
        self.add_widget(text_input_question)

        delete_function = partial(
            self.delete_question, question_id=counter_line)
        self.delete_function_dict[counter_line] = delete_function
        delete_button = create_button_scrollview_simple_no_focus(
            button_text="-",
            x_size=0.05,
            size_vertical=self.size_line,
            x_pos=0.85,
            y_pos=number_widgets * 1.1 * self.size_line + offset,
            background_color=DatabaseInst.manager.button_blue_color,
            on_press=self.delete_function_dict[counter_line]
        )
        self.add_widget(delete_button)

        list_widgets_options = []
        for counter_option in range(number_options - 1, -1, -1):
            bool_is_correct = False
            if dict_content["answer"] != None and int(dict_content["answer"]) == counter_option:
                bool_is_correct = True
            list_option = self.display_option_line(
                y_pos=(counter_option + 2) * 1.1 * self.size_line + offset,
                counter_option=number_options - counter_option,
                counter_line=counter_line,
                option=dict_content["options"][counter_option],
                bool_is_correct=bool_is_correct
            )
            list_widgets_options.append(list_option)

        add_option_button = create_button_scrollview_simple(
            button_text="+",
            x_size=0.055,
            size_vertical=self.size_line,
            x_pos=0.5625,
            y_pos=1.1 * self.size_line + offset
        )
        add_option_button.on_release = partial(
            self.add_option, counter_line, "")
        self.add_widget(add_option_button)

        self.number_lines += number_widgets
        self.switch_lines_top(start_counter=counter_line,
                              number_switch=number_widgets)

        # Update the dictionary of widgets for each question
        self.dict_widgets_database[counter_line] = {
            "id_line": label_id,
            "question": text_input_question,
            "options": list_widgets_options,
            "add_option": add_option_button,
            "delete": delete_button
        }

        return text_input_question

    def switch_lines_top(self, start_counter, number_switch, switch_options=False):
        y_pos = 0
        for key in self.dict_widgets_database:
            dict_line = self.dict_widgets_database[key]
            if key <= start_counter:
                y_switch = 1.1 * self.size_line * number_switch
                dict_line["id_line"].y += y_switch
                dict_line["question"].y += y_switch
                dict_line["delete"].y += y_switch
                if key != start_counter or not switch_options:
                    dict_line["add_option"].y += y_switch
                else:
                    y_pos = dict_line["add_option"].y + 1.1 * self.size_line
                for counter_option in range(len(dict_line["options"])):
                    dict_line["options"][counter_option][0].y += y_switch
                    dict_line["options"][counter_option][1].y += y_switch
        return y_pos

    def switch_lines_bottom(self, start_counter, number_switch, switch_options=False):
        y_pos = 0
        for key in self.dict_widgets_database:
            dict_line = self.dict_widgets_database[key]
            if key < start_counter:
                y_switch = 1.1 * self.size_line * number_switch
                dict_line["id_line"].y -= y_switch
                dict_line["question"].y -= y_switch
                dict_line["delete"].y -= y_switch
                if key != start_counter or not switch_options:
                    dict_line["add_option"].y -= y_switch
                else:
                    y_pos = dict_line["add_option"].y + 1.1 * self.size_line
                for counter_option in range(len(dict_line["options"])):
                    dict_line["options"][counter_option][0].y -= y_switch
                    dict_line["options"][counter_option][1].y -= y_switch
        return y_pos

    def rebuild_part_screen(self, start_counter):
        for key in self.dict_widgets_database:
            dict_line = self.dict_widgets_database[key]
            if key > start_counter:
                text_input = dict_line["question"]
                self.remove_widget(text_input)
                self.add_widget(text_input)
                for counter_option in range(len(dict_line["options"])):
                    option_input = dict_line["options"][counter_option][0]
                    option_checkbox = dict_line["options"][counter_option][1]
                    self.remove_widget(option_input)
                    self.add_widget(option_input)
                    self.remove_widget(option_checkbox)
                    self.add_widget(option_checkbox)
                add_option_button = dict_line["add_option"]
                self.remove_widget(add_option_button)
                self.add_widget(add_option_button)
            if key == start_counter:
                add_option_button = dict_line["add_option"]
                self.remove_widget(add_option_button)
                self.add_widget(add_option_button)

    def display_option_line(self, y_pos, counter_option, counter_line, option, bool_is_correct=False, bool_add_option=False):
        if bool_add_option:
            y_pos = self.switch_lines_top(counter_line, 1, switch_options=True)
        text_input_option = create_text_input_scrollview_simple(
            input_text=option,
            x_size=0.4,
            size_vertical=self.size_line,
            x_pos=0.1625,
            y_pos=y_pos,
            placeholder=DatabaseInst.TEXT_DATABASE["placeholder_option"] + str(
                counter_option),
            write_tab=False,
            multiline=False
        )
        self.add_widget(text_input_option)

        radio_option = create_checkbox_scrollview_simple(
            x_size=0.055,
            size_vertical=self.size_line,
            x_pos=0.5625,
            y_pos=y_pos,
            group=str(counter_line)
        )
        if bool_is_correct:
            radio_option.active = True
        self.add_widget(radio_option)

        if bool_add_option:
            self.rebuild_part_screen(start_counter=counter_line)

        return [text_input_option, radio_option]

    def add_option(self, counter_line, option):
        self.number_lines += 1
        counter_option = len(
            self.dict_widgets_database[counter_line]["options"]) + 1
        list_option = self.display_option_line(
            y_pos=0,
            counter_option=counter_option,
            counter_line=counter_line,
            option=option,
            bool_add_option=True
        )
        self.dict_widgets_database[counter_line]["options"].append(list_option)

        # Set the focus on the right element and rearrange the order of elements
        list_option[0].focus = True
        self.remove_widget(self.add_question_button)
        self.add_widget(self.add_question_button)


####################
### Classes menu ###
####################


class ClassesWindow(Screen):
    def __init__(self, **kw):
        global ClassesInst
        super().__init__(**kw)
        ClassesInst = self
        # Initialise the scroll view layout to None in order to know if it exists or not
        self.scroll_view_layout = None

    list_classes = ObjectProperty([])
    TEXT_CLASSES = DICT_LANGUAGE["classes"]

    def init_screen(self):
        self.ids.new_class_button.on_release = self.create_new_class
        self.list_classes = [
            self.manager.CLASSES_SPINNER_DEFAULT] + get_list_classes()

    def update_classes(self, class_name):
        if class_name == self.manager.CLASSES_SPINNER_DEFAULT:
            self.ids.reset_button.disabled = True
            return
        self.ids.reset_button.disabled = False
        # Get the content of the class
        class_content = load_class(class_name)
        self.build_scroll_view(class_content)

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
        caracter_limit = 20

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
                "text": cut_text_with_newlines(
                    string=label_folder_text,
                    caracter_limit=caracter_limit)
            }
            dict_line["label_file"] = {
                "text": cut_text_with_newlines(
                    string=key[1],
                    caracter_limit=caracter_limit)
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
        if self.current == "qcm":
            QCMWindowInst.init_screen()
        if self.current == "database":
            DatabaseInst.init_screen()
        if self.current == "classes":
            ClassesInst.init_screen()


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
    MCQMakerApp().run()