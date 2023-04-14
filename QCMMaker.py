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
from kivy.properties import ObjectProperty, StringProperty

### Python imports ###

from functools import partial
from tkinter.filedialog import askopenfilename

### File imports ###

from qcm_maker_tools.tools_kivy import *
from qcm_maker_tools.tools import *


#################
### Main menu ###
#################


class MenuWindow(Screen):
    """
    Class displaying the main menu.
    """

    def __init__(self, **kw):
        super().__init__(**kw)


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

    NEW_CONFIG = "Nouveau"
    nb_questions_label = StringProperty("Nombre de questions : 0")
    number_total_questions = StringProperty("/0")
    list_folders = ObjectProperty([])
    list_files = ObjectProperty([])
    list_classes = ObjectProperty([])
    list_templates = ObjectProperty([])
    class_content = {}
    CONFIG_TEMP = "temp"

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
        self.ids.save_config_button.on_release = partial(
            self.save_config,
            False
        )
        self.ids.generate_qcm_button.on_release = partial(
            self.save_config,
            True
        )
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
        self.list_classes = get_list_classes()
        self.list_templates = get_list_templates()
        self.list_folders = [self.manager.FOLDER_SPINNER_DEFAULT] + \
            get_list_database_folders()
        self.list_files = [self.manager.FILE_SPINNER_DEFAULT]

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
        popup_content = [
            ("label", {
                "text": "Veuillez choisir une configuration.",
                "pos_hint": {"x": 0.1, "y": 0.7},
                "size_hint": (0.8, 0.15)
            }
            )
        ]

        # Create the popup
        popup = ImprovedPopup(
            title="Chargement d'une configuration",
            add_content=popup_content)

        # Add the three buttons, to create a new config, load a former and close the window
        popup.add_button(
            text="Nouvelle\nconfiguration",
            pos_hint={"x": 0.1, "y": 0.4},
            size_hint=(0.35, 0.15),
            on_release=partial(self.new_config, popup)
        )
        popup.add_button(
            text="Choisir une\nconfiguration",
            pos_hint={"x": 0.55, "y": 0.4},
            size_hint=(0.35, 0.15),
            on_release=partial(self.open_file_explorer, popup)
        )
        popup.add_button(
            text=dict_buttons["close"],
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
        self.ids.config_name_input.focus = True
        self.ids.config_name_input.text = ""
        self.ids.classes_spinner.text = self.manager.CLASSES_SPINNER_DEFAULT
        self.ids.classes_spinner.disabled = False
        popup.dismiss()

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
            title="Sélectionnez le fichier de configuration",
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
        # Load the configuration
        config = load_config(config_name)
        class_name = self.ids.classes_spinner.text

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

        # Display the configuration on the screen
        SVQCMInst.display_config(config)

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

        # Extract the template
        template = self.ids.template_spinner.text
        if template == self.manager.TEMPLATE_SPINNER_DEFAULT:
            template = None
        else:
            SETTINGS = update_settings(SETTINGS, "default_template", template)

        # Extract the configuration from the scroll view
        config = {
            "QCM_name": config_name,
            "questions": [],
            "template": template,
            "mix_all_questions": self.ids.mix_all_questions.active,
            "mix_among_databases": self.ids.mix_inside_questions.active,
            "update_class": self.ids.modify_class.active
        }
        dict_widgets = SVQCMInst.dict_widgets_config
        for key in dict_widgets:
            dict_line = dict_widgets[key]
            nb_questions_str = dict_line["nb_questions"].text
            if nb_questions_str != "":
                nb_questions = int(nb_questions_str)
                config_line = {
                    "folder_name": dict_line["folder_name"].text,
                    "file_name": dict_line["file_name"].text,
                    "nb_questions": nb_questions
                }
                config["questions"].append(config_line)

        return config

    def reload_class(self, class_name):
        temp_name = self.CONFIG_TEMP

        # Save the actual configuration
        save_config(
            config_name=temp_name,
            config=self.extract_config(temp_name)
        )

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

    def save_config(self, bool_generate_MCQ):
        """
        Launch the save of the config or the generation of the MCQ, according to the given boolean.

        Parameters
        ----------
        bool_generate_MCQ: bool
            Boolean according to which the user wants to save the configuration or generate the MCQ.

        Returns
        -------
        None
        """
        config_name = self.ids.config_name_input.text
        if config_name == "":
            create_standard_popup(
                message=dict_messages["error_name_config"][1],
                title_popup=dict_messages["error_name_config"][0],
            )
            return
        config = self.extract_config(config_name)
        if not bool_generate_MCQ:
            # Save the configuration in a json file
            save_config(
                config_name=config_name,
                config=config)
            # Display popup to confirm the success of the save
            create_standard_popup(
                message=dict_messages["success_save_config"][1],
                title_popup=dict_messages["success_save_config"][0],
            )
        else:
            class_name = self.ids.classes_spinner.text
            if class_name == self.manager.CLASSES_SPINNER_DEFAULT:
                class_name = None
            # Launch the generation of the QCM in txt, xml and docx
            launch_export_QCM(config, class_name, None)
            # TODO création de popup pour afficher la progression

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
        self.ids.add_button.disabled = True
        self.ids.folders_spinner.focus = True

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
            return

        # Real folder selected
        self.ids.nb_questions_input.disabled = True
        self.ids.nb_questions_input.hint_text = ""
        self.ids.add_button.disabled = True
        self.ids.files_spinner.disabled = False
        self.ids.files_spinner.text = self.manager.FILE_SPINNER_DEFAULT
        self.ids.files_spinner.focus = True
        # Update the list of files according to the selected folder
        self.list_files = [self.manager.FILE_SPINNER_DEFAULT] + \
            get_list_database_files(
                self.ids.folders_spinner.text,
                exclusion_list=self.get_keys_dict_scroll_view())

    def get_keys_dict_scroll_view(self):
        list_keys = []
        dict_widgets = SVQCMInst.dict_widgets_config
        for key in dict_widgets:
            folder_name = dict_widgets[key]["folder_name"].text.replace(
                "\n", " ")
            file_name = dict_widgets[key]["file_name"].text.replace("\n", " ")
            list_keys.append((folder_name, file_name))
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
            self.ids.nb_questions_input.hint_text = "Nb questions"
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
        else:
            try:
                nb_questions = int(text)
                if nb_questions > int(total_questions):
                    nb_questions = 0
                    instance.text = ""
            except:
                nb_questions = 0
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
        SVQCMInst.add_database_scroll_view(
            counter_line=len(SVQCMInst.dict_widgets_config.keys()),
            config_line=config_line,
            total_questions=total_questions
        )
        self.reset_tool_menu_top()
        # Set focus on the folders spinner
        self.ids.folders_spinner.focus = True


class QCMScrollView(FloatLayout):
    """
    Class displaying the scrollview for the creation of the QCM.
    """

    def __init__(self, **kwargs):
        global SVQCMInst
        super().__init__(**kwargs)
        SVQCMInst = self

    number_lines = ObjectProperty(0)
    size_line = ObjectProperty(30)
    dict_widgets_config = {}
    list_widgets = []
    default_database = {}

    def reset_screen(self):
        for widget in self.list_widgets:
            self.remove_widget(widget)
        self.number_lines = 0
        self.dict_widgets_config = {}
        self.list_widgets = []
        QCMWindowInst.nb_questions_label = "Nombre de questions : 0"

    def display_config(self, config):
        self.reset_screen()
        questions = config["questions"]
        class_name = QCMWindowInst.ids.classes_spinner.text

        # Display each line of the configuration in the scrollview
        for counter_question in range(len(questions)):
            question = questions[counter_question]
            folder_name = question["folder_name"].replace("\n", " ")
            file_name = question["file_name"].replace("\n", " ")

            # Get the number of questions available
            if class_name != QCMWindowInst.manager.CLASSES_SPINNER_DEFAULT:
                dict_class_content = QCMWindowInst.class_content[
                    (folder_name, file_name)]
                left_questions = dict_class_content["total_questions"] - \
                    dict_class_content["used_questions"]
            else:
                left_questions = get_nb_questions(
                    database_name=file_name,
                    database_folder=folder_name
                )

            # Add the line into the database
            self.add_database_scroll_view(
                counter_line=counter_question,
                config_line=question,
                total_questions=left_questions
            )

    def switch_lines_top(self, start_counter, number_switch):
        for key in self.dict_widgets_config:
            dict_line = self.dict_widgets_config[key]
            if key <= start_counter:
                y_switch = 1.1 * self.size_line * number_switch
                dict_line["folder_name"].y += y_switch
                dict_line["file_name"].y += y_switch
                dict_line["nb_questions"].y += y_switch
                dict_line["total_questions"].y += y_switch

    def increase_counter_questions(self, counter_line, nb_questions, bool_init=False):
        list_temp = QCMWindowInst.nb_questions_label.split(" : ")
        number_total_questions = int(list_temp[1])
        number_former_questions = 0
        if not bool_init:
            number_former_questions = self.dict_widgets_config[counter_line]["former_nb_questions"]
            self.dict_widgets_config[counter_line]["former_nb_questions"] = nb_questions
        number_total_questions += (nb_questions - number_former_questions)
        QCMWindowInst.nb_questions_label = list_temp[0] + " : " + str(
            number_total_questions)

    def update_nb_questions(self, instance, text, counter_line):
        nb_questions = QCMWindowInst.verify_nb_questions(
            instance=instance,
            text=text,
            total_questions=(
                self.dict_widgets_config[counter_line]["total_questions"].text).replace("/", ""))
        self.increase_counter_questions(counter_line, nb_questions)

    def add_database_scroll_view(self, counter_line, config_line, total_questions):
        self.number_lines += 1
        y_pos = 1.1 * self.size_line
        folder_label = create_label_scrollview_simple(
            label_text=config_line["folder_name"],
            x_size=0.32,
            size_vertical=self.size_line,
            x_pos=0.05,
            y_pos=y_pos
        )
        self.add_widget(folder_label)

        file_label = create_label_scrollview_simple(
            label_text=config_line["file_name"],
            x_size=0.32,
            size_vertical=self.size_line,
            x_pos=0.39,
            y_pos=y_pos
        )
        self.add_widget(file_label)

        nb_questions = config_line["nb_questions"]
        nb_questions_input = create_text_input_scrollview_simple(
            input_text=str(nb_questions),
            placeholder="Nb questions",
            x_size=0.1,
            size_vertical=self.size_line,
            x_pos=0.74,
            y_pos=y_pos,
            write_tab=False,
            multiline=False
        )
        nb_questions_input.bind(text=partial(
            self.update_nb_questions, counter_line=counter_line))
        self.add_widget(nb_questions_input)

        label_questions = create_label_scrollview_simple(
            label_text="/" + str(total_questions),
            x_size=0.07,
            size_vertical=self.size_line,
            x_pos=0.906,
            y_pos=y_pos,
            bool_text_size=True
        )
        self.add_widget(label_questions)

        self.switch_lines_top(start_counter=counter_line, number_switch=1)

        # Update the dictionary of widgets for each question
        self.dict_widgets_config[counter_line] = {
            "id_line": counter_line,
            "folder_name": folder_label,
            "file_name": file_label,
            "nb_questions": nb_questions_input,
            "total_questions": label_questions,
            "former_nb_questions": nb_questions
        }
        self.list_widgets.append(folder_label)
        self.list_widgets.append(file_label)
        self.list_widgets.append(nb_questions_input)
        self.list_widgets.append(label_questions)

        # Update the total number of questions
        self.increase_counter_questions(
            counter_line=counter_line,
            nb_questions=nb_questions,
            bool_init=True)

        # Scroll to the end of the scroll view when there are enough widgets
        if self.number_lines * self.size_line > self.parent.height:
            self.parent.scroll_y = 0

        return nb_questions_input


#####################
### Database menu ###
#####################


class DatabaseWindow(Screen):
    def __init__(self, **kw):
        global DatabaseInst
        super().__init__(**kw)
        DatabaseInst = self

    NEW_FILE = "Nouveau"
    DICT_SAVE_MESSAGES = {
        "new_folder": "Créer le dossier",
        "new_file": "Créer la nouvelle\nbase de données",
        "edit_database": "Sauvegarder la base\nde données",
        "none": ""
    }
    # Initialise the list of folders available
    list_folders = ObjectProperty([])
    list_files = ObjectProperty([])
    name_database = StringProperty("")

    def init_screen(self):
        self.ids.folders_spinner.focus = True
        self.ids.save_button.on_release = self.save_database
        self.list_folders = [
            self.manager.FOLDER_SPINNER_DEFAULT,
            self.NEW_FILE] + get_list_database_folders(caracter_limit=15)
        self.list_files = [self.manager.FILE_SPINNER_DEFAULT]

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
            self.ids.name_database_input.hint_text = "Nom du nouveau dossier"
            self.ids.save_button.disabled = False
            self.ids.save_button.text = self.DICT_SAVE_MESSAGES["new_folder"]
            self.ids.name_database_input.focus = True
            return

        # Real folder selected
        self.ids.name_database_input.disabled = True
        self.ids.name_database_input.hint_text = ""
        self.ids.save_button.disabled = True
        self.ids.save_button.text = ""
        self.ids.files_spinner.disabled = False
        self.ids.files_spinner.text = self.manager.FILE_SPINNER_DEFAULT
        self.ids.files_spinner.focus = True
        # Update the list of files according to the selected folder
        self.list_files = [self.manager.FILE_SPINNER_DEFAULT,
                           self.NEW_FILE] + get_list_database_files(folder_name)

    def update_scroll_view_database(self, spinner_folder_text, spinner_files_text):
        # Reset the screen when the selected file has changed
        SVDatabaseInst.reset_screen()
        self.ids.name_database_input.text = ""

        # Create a new database
        if spinner_files_text == self.NEW_FILE:
            self.ids.name_database_input.disabled = False
            self.ids.name_database_input.hint_text = "Nom de la nouvelle base de données"
            self.ids.name_database_input.focus = True
            self.ids.save_button.disabled = False
            self.ids.save_button.text = self.DICT_SAVE_MESSAGES["new_file"]
            SVDatabaseInst.initialise_database(spinner_folder_text, "")
            return

        if spinner_files_text == self.manager.FILE_SPINNER_DEFAULT:
            self.ids.name_database_input.hint_text = ""
            self.ids.name_database_input.disabled = True
            self.ids.save_button.disabled = True
            self.ids.save_button.text = self.DICT_SAVE_MESSAGES["none"]
            self.ids.files_spinner.focus = True
            return

        # Edit a former database
        self.ids.name_database_input.disabled = True
        self.ids.name_database_input.hint_text = ""
        self.ids.save_button.disabled = False
        self.ids.save_button.text = self.DICT_SAVE_MESSAGES["edit_database"]
        SVDatabaseInst.initialise_database(
            spinner_folder_text, spinner_files_text)

    def save_database(self):
        button_text = self.ids.save_button.text
        if button_text == self.DICT_SAVE_MESSAGES["new_folder"]:
            # Create the new folder
            create_database_folder(self.ids.folders_spinner.text)
            self.update_list_folders()

        # Update the name of the database
        self.name_database = self.ids.name_database_input.text

        # Create the list of content
        content = []
        for key in SVDatabaseInst.dict_widgets_database:
            dict_line = SVDatabaseInst.dict_widgets_database[key]
            if dict_line["question"].text != "":
                dict_content = {
                    "question": dict_line["question"].text,
                    "options": [],
                    "answer": ""
                }
                list_options = dict_line["options"]
                for counter_option in range(len(list_options)):
                    option = list_options[counter_option]
                    if option[0].text != "":
                        if option[1].active:
                            dict_content["answer"] = counter_option
                        dict_content["options"].append(option[0].text)
                if dict_content["answer"] == "":
                    create_standard_popup(
                        message=dict_messages["error_selected_answer"][1] +
                        dict_content["question"],
                        title_popup=dict_messages["error_selected_answer"][0]
                    )
                    return
                content.append(dict_content)
        # PAUL
        # Save the database in the new file
        print(content)
        print(self.name_database)


class DatabaseScrollView(FloatLayout):
    """
    Class displaying the scrollview to edit the database.
    """

    def __init__(self, **kwargs):
        global SVDatabaseInst
        super().__init__(**kwargs)
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
            self.remove_widget(dict_line["question"])
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

    def initialise_database(self, folder_name, file_name):
        # Delete all widgets of the screen
        self.reset_screen()

        # Add each question
        if file_name != "":
            # PAUL
            # Get the content of the database to edit
            list_content, error_list = load_database(file_name, folder_name)
            nb_questions = len(list_content)
            for counter_line in range(nb_questions):
                dict_content = list_content[counter_line]
                self.add_question(
                    counter_line=counter_line,
                    dict_content=dict_content
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

    def add_question(self, counter_line, dict_content, bool_new_question=False):
        offset = 0
        if bool_new_question:
            offset = 1.1 * self.size_line
        number_options = len(dict_content["options"])
        number_widgets = 2 + number_options
        text_input_question = create_text_input_scrollview_simple(
            input_text=dict_content["question"],
            x_size=0.7,
            size_vertical=self.size_line,
            x_pos=0.0375,
            y_pos=number_widgets * 1.1 * self.size_line + offset,
            placeholder="Question",
            write_tab=False,
            multiline=False
        )
        self.add_widget(text_input_question)

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
            x_pos=0.5,
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
            "id_line": counter_line,
            "question": text_input_question,
            "options": list_widgets_options,
            "add_option": add_option_button
        }

        return text_input_question

    def switch_lines_top(self, start_counter, number_switch, switch_options=False):
        y_pos = 0
        for key in self.dict_widgets_database:
            dict_line = self.dict_widgets_database[key]
            if key <= start_counter:
                y_switch = 1.1 * self.size_line * number_switch
                dict_line["question"].y += y_switch
                if key != start_counter or not switch_options:
                    dict_line["add_option"].y += y_switch
                else:
                    y_pos = dict_line["add_option"].y + 1.1 * self.size_line
                for counter_option in range(len(dict_line["options"])):
                    dict_line["options"][counter_option][0].y += y_switch
                    dict_line["options"][counter_option][1].y += y_switch
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
            x_pos=0.1,
            y_pos=y_pos,
            placeholder="Option " + str(counter_option),
            write_tab=False,
            multiline=False
        )
        self.add_widget(text_input_option)

        radio_option = create_checkbox_scrollview_simple(
            x_size=0.055,
            size_vertical=self.size_line,
            x_pos=0.5,
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

    CLASSES_SPINNER_DEFAULT = "Choisir la classe..."
    # PAUL
    list_classes = ObjectProperty(
        [CLASSES_SPINNER_DEFAULT] + ["Classe 1", "Classe 2"])

    def init_screen(self):
        self.ids.new_class_button.on_release = self.create_new_class

    def update_classes(self, class_name):
        SVClassesInst.reset_screen()
        if class_name == self.manager.CLASSES_SPINNER_DEFAULT:
            self.ids.reset_button.disabled = True
            return
        self.ids.reset_button.disabled = False
        # Get the content of the class
        class_content = load_class(class_name)
        SVClassesInst.display_classes_content(class_content)

    def reset_class(self):
        SVClassesInst.reset_screen()
        class_name = self.ids.class_selection.text
        self.ids.reset_button.disabled = True
        self.ids.class_selection.text = self.manager.CLASSES_SPINNER_DEFAULT
        print(class_name)
        # PAUL
        # Reset the data of the class
        create_standard_popup(
            message=dict_messages["success_reset_class"][1],
            title_popup=dict_messages["success_reset_class"][0],
        )

    def create_new_class(self):
        SVClassesInst.reset_screen()
        class_name = self.ids.new_class_input.text
        if class_name in self.list_classes:
            create_standard_popup(
                message=dict_messages["error_create_class"][1],
                title_popup=dict_messages["error_create_class"][0]
            )
            return
        elif class_name != "":
            save_class(class_name, {})
            # Create the new class
            create_standard_popup(
                message=dict_messages["success_create_class"][1],
                title_popup=dict_messages["success_create_class"][0]
            )
        self.ids.new_class_input.text = ""


class ClassesScrollView(FloatLayout):
    """
    Class displaying the scrollview for the classes.
    """

    def __init__(self, **kwargs):
        global SVClassesInst
        super().__init__(**kwargs)
        SVClassesInst = self

    number_lines = ObjectProperty(0)
    size_line = ObjectProperty(30)
    list_widgets = []

    def reset_screen(self):
        """
        Reset the content of the scrollview by removing all widgets
        """
        for widget in self.list_widgets:
            self.remove_widget(widget)
        self.list_widgets = []
        self.number_lines = 0

    def switch_all_lines_top(self):
        y_switch = 1.1 * self.size_line
        for widget in self.list_widgets:
            widget.y += y_switch

    def display_classes_content(self, class_content):
        """
        Create the widgets for the scrollview for the corresponding class

        Parameters
        ----------
        class_content: list of dict
            List containing the information for each file of the database.
        """
        # Sort by folder name then file name
        list_keys_class_content = list(class_content.keys())
        list_keys_class_content.sort(
            key=lambda key_class_content:
            (key_class_content[0], key_class_content[1]))
        list_folders = []

        for key in list_keys_class_content:
            self.number_lines += 1
            y_pos = 1.1 * self.size_line

            # Get the name of the folder and do not display one twice
            label_folder_text = ""
            folder_name = key[0]
            if folder_name not in list_folders:
                list_folders.append(folder_name)
                label_folder_text = folder_name

            label_folder = create_label_scrollview_simple(
                label_text=label_folder_text,
                x_size=0.2,
                size_vertical=self.size_line,
                x_pos=0.0375,
                y_pos=y_pos
            )

            label_file = create_label_scrollview_simple(
                label_text=key[1],
                x_size=0.2,
                size_vertical=self.size_line,
                x_pos=0.2625,
                y_pos=y_pos
            )

            used_questions = class_content[key]["used_questions"]
            total_questions = class_content[key]["total_questions"]
            label_questions = create_label_scrollview_simple(
                label_text=str(used_questions) + "/" + str(total_questions),
                x_size=0.1,
                size_vertical=self.size_line,
                x_pos=0.5375,
                y_pos=y_pos
            )

            progress_bar = create_progress_bar_scrollview_simple(
                max_value=total_questions,
                value=used_questions,
                x_size=0.3125,
                size_vertical=self.size_line,
                x_pos=0.65,
                y_pos=y_pos
            )

            # Switch all lines to the top
            self.switch_all_lines_top()

            # Add all widgets to the list of widgets to display them later
            self.list_widgets.append(label_folder)
            self.list_widgets.append(label_file)
            self.list_widgets.append(label_questions)
            self.list_widgets.append(progress_bar)

        # Display all widgets on the screen
        for widget in self.list_widgets:
            self.add_widget(widget)


#######################
### Generic classes ###
#######################


class TabsLayout(GridLayout):
    """
    Class displaying the menu with the three tabs for each window
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos_hint = {"x": 0, "y": 0.925}
        self.size_hint = (1, 0.075)
        self.cols = 3


###############
### General ###
###############


class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.highlight_text_color = highlight_text_color
        self.button_blue_color = (
            2 * blue_color[0], 2 * blue_color[1], 2 * blue_color[2], blue_color[3])
        self.button_pink_color = (
            2 * pink_color[0], 2 * pink_color[1], 2 * pink_color[2], pink_color[3])
        self.button_disabled_color = (
            382 / 255, 382 / 255, 382 / 255, 1)
        self.color_label = color_label
        self.transition = NoTransition()

    # Global variables
    FOLDER_SPINNER_DEFAULT = "Choisir le dossier..."
    FILE_SPINNER_DEFAULT = "Choisir le fichier..."
    CLASSES_SPINNER_DEFAULT = "Choisir la classe..."
    TEMPLATE_SPINNER_DEFAULT = SETTINGS["default_template"]

    def initialise_screen(self):
        if self.current == "qcm":
            QCMWindowInst.init_screen()
        if self.current == "database":
            DatabaseInst.init_screen()
        if self.current == "classes":
            ClassesInst.init_screen()


class QCMMakerApp(App):
    """
    Main class of the application.
    """

    def build(self):
        Window.clearcolor = background_color


if __name__ == "__main__":
    Builder.load_file("data_kivy/extended_style.kv")
    QCMMakerApp().run()
