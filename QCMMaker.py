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
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty

### Python imports ###

from functools import partial

### File imports ###

from qcm_maker_tools.tools_kivy import *
from qcm_maker_tools.tools import *


#################
### Main menu ###
#################


class MenuWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)


################
### QCM menu ###
################


class QCMWindow(Screen):
    def __init__(self, **kw):
        global QCMWindowInst
        self.update_screen()
        super().__init__(**kw)
        QCMWindowInst = self

    NEW_CONFIG = "Nouveau"
    CLASSES_SPINNER_DEFAULT = "Choisir la classe..."
    TEMPLATE_SPINNER_DEFAULT = SETTINGS["default_template"]
    number_questions_label = StringProperty("Nombre de questions : 0")
    showMenu = BooleanProperty(False)
    FOLDER_SPINNER_DEFAULT = "Choisir le dossier..."
    FILE_SPINNER_DEFAULT = "Choisir le fichier..."
    number_questions = StringProperty("/0")
    list_folders = ObjectProperty([])
    list_files = ObjectProperty([])
    list_classes = ObjectProperty([])
    list_templates = ObjectProperty([])

    def update_screen(self):
        self.list_classes = get_list_classes()
        self.list_templates = get_list_templates()
        self.list_folders = [self.FOLDER_SPINNER_DEFAULT] + \
            get_list_database_folders()
        self.list_files = [self.FILE_SPINNER_DEFAULT]

    def load_config(self):
        # TODO
        # Ouvrir une popup qui demande quelle configuration choisir, et qui laisse le choix avec nouveau
        popup_content = [
            ("label", {
                "text": "Veuillez choisir\nune configuration",
                "pos_hint": {"x": 0.1, "top": 0.8},
                "size_hint": (0.8, 0.15)
            }
            ),
            ("button", {
                "text": "Nouvelle configuration",
                "pos_hint": {"x": 0.1, "top": 0.45},
                "size_hint": (0.35, 0.15),
                "on_release": self.new_config
            }
            ),
            ("button", {
                "text": "Charger une\nconfiguration existante",
                "pos_hint": {"x": 0.55, "top": 0.45},
                "size_hint": (0.35, 0.15),
                "on_release": self.new_config
            }
            )
        ]

        popup = ImprovedPopup(
            title="Chargement d'une configuration",
            add_content=popup_content)
        popup.add_button(
            text="Fermer cette fenêtre",
            pos_hint={"x": 0, "top": 0.2},
            size_hint=(1, 0.15),
            on_release=popup.dismiss)

        config_name = "test"
        self.ids.config_name_input.disabled = False
        self.ids.save_config_button.disabled = False
        self.ids.template_spinner.disabled = False
        self.ids.generate_qcm_button.disabled = False
        self.ids.config_name_input.hint_text = "Nom de la configuration"
        self.showMenu = True
        self.get_config(config_name)

    def new_config(self, *args):
        self.ids.config_name_input.focus = True
        self.ids.classes_spinner.text = self.CLASSES_SPINNER_DEFAULT
        self.ids.classes_spinner.disabled = False

    def open_file_explorer(self):
        pass

    def get_config(self, config_name):
        config = load_config(config_name)
        # TODO mettre le max comme il faut pour les questions où il y a trop
        SVQCMInst.display_config(config)

    def check_errors_question(self, question):
        if question["number_questions"] > question["total_questions"]:
            # TODO message d'erreur dans popup
            print("Erreur, il y a plus de questions demandées que disponibles")
            return False
        return True

    def extract_config(self):
        config_name = self.ids.config_name_input.text
        if config_name == "":
            return
        qcm_name = config_name + "_" + self.ids.classes_spinner.text
        # PAUL sauvegarder le template dans un autre fichier pour les prochaines fois
        template = self.ids.template_spinner.text

        # Extract the configuration from the scroll view
        config = {
            "QCM_name": qcm_name,
            "class": self.ids.classes_spinner.text,
            "questions": [],
            "template": template,
            "mix_all_questions": self.ids.mix_all_questions.active,
            "mix_among_database": self.ids.mix_inside_questions.active,
            "update_class": self.ids.modify_class.active
        }
        dict_widgets = SVQCMInst.dict_widgets_config
        for key in dict_widgets:
            dict_line = dict_widgets[key]
            config_line = {
                "folder": dict_line["folder"].text,
                "file": dict_line["file"].text,
                "number_questions": int(dict_line["number_questions"].text),
                "total_questions": int(dict_line["total_questions"].text.replace("/", ""))
            }
            # Check errors in configuration regarding the number of questions
            if self.check_errors_question(config_line):
                config["questions"].append(config_line)
            else:
                return

        return config

    def save_config(self, bool_generate_QCM):
        config = self.extract_config()
        if config != None:
            config_name = self.ids.config_name_input.text
            if not bool_generate_QCM:
                # PAUL
                # Save the configuration in a json file
                # TODO création de popup pour dire que ça s'est bien sauvegardé
                print(config, config_name)
            else:
                # PAUL => est-ce qu'on sauvegarde la config quand on génère un QCM ?
                # Launch the generation of the QCM in txt and in docx
                # TODO création de popup pour afficher la progression
                print(config, config_name)
        else:
            # TODO message d'erreur dans popup
            print("Erreur, la configuration n'a pas de nom")

    def reset_tool_menu_top(self):
        self.ids.folders_spinner.text = self.FOLDER_SPINNER_DEFAULT
        self.ids.files_spinner.text = self.FILE_SPINNER_DEFAULT
        self.ids.files_spinner.disabled = True
        self.list_files = [self.FILE_SPINNER_DEFAULT]
        self.ids.number_questions_input.disabled = True
        self.ids.number_questions_input.hint_text = ""
        self.ids.number_questions_input.text = ""
        self.ids.add_button.disabled = True
        self.ids.folders_spinner.focus = True

    def update_list_files(self, spinner_folder_text):
        # Default value where to choose the folder
        if spinner_folder_text == self.FOLDER_SPINNER_DEFAULT:
            self.reset_tool_menu_top()
            return

        # Real folder selected
        self.ids.number_questions_input.disabled = True
        self.ids.number_questions_input.hint_text = ""
        self.ids.add_button.disabled = True
        self.ids.files_spinner.disabled = False
        self.ids.files_spinner.text = self.FILE_SPINNER_DEFAULT
        self.ids.files_spinner.focus = True
        # Update the list of files according to the selected folder
        self.list_files = [self.FILE_SPINNER_DEFAULT] + \
            get_list_database_files(self.ids.folders_spinner.text)

    def update_number_questions(self, folder_name, file_name):
        if file_name != self.FILE_SPINNER_DEFAULT:
            self.ids.number_questions_input.disabled = False
            self.ids.number_questions_input.text = ""
            self.ids.number_questions_input.hint_text = "Nb questions"
            self.ids.number_questions_input.focus = True
            self.ids.add_button.disabled = True
            self.number_questions = "/" + \
                str(get_nb_questions(file_name,
                    folder_name))

    def change_number_questions(self, number_questions):
        # TODO
        #number_total_questions = int(self.number_questions.replace)
        pass

    def add_database(self):
        number_questions = int(self.ids.number_questions_input.text)
        total_questions = int(str(self.number_questions).replace("/", ""))
        config_line = {
            "folder": self.ids.folders_spinner.text,
            "file": self.ids.files_spinner.text,
            "number_questions": number_questions,
            "total_questions": total_questions
        }
        if self.check_errors_question(config_line):
            SVQCMInst.add_database(
                counter_line=len(SVQCMInst.dict_widgets_config.keys()),
                config_line=config_line
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
    default_database = {}

    def display_config(self, config):
        questions = config["questions"]
        for counter_question in range(len(questions)):
            self.add_database(counter_question, questions[counter_question])

    def switch_lines_top(self, start_counter, number_switch):
        for key in self.dict_widgets_config:
            dict_line = self.dict_widgets_config[key]
            if key <= start_counter:
                y_switch = 1.1 * self.size_line * number_switch
                dict_line["folder"].y += y_switch
                dict_line["file"].y += y_switch
                dict_line["number_questions"].y += y_switch
                dict_line["total_questions"].y += y_switch

    def increase_counter_questions(self, counter_line, number_questions, bool_init=False):
        list_temp = QCMWindowInst.number_questions_label.split(" : ")
        number_total_questions = int(list_temp[1])
        number_former_questions = 0
        if not bool_init:
            number_former_questions = self.dict_widgets_config[counter_line]["former_number_questions"]
            self.dict_widgets_config[counter_line]["former_number_questions"] = number_questions
        number_total_questions += (number_questions - number_former_questions)
        QCMWindowInst.number_questions_label = list_temp[0] + " : " + str(
            number_total_questions)

    def update_number_questions(self, instance, text, counter_line):
        if text == "":
            number_questions = 0
        else:
            try:
                number_questions = int(text)
                total_questions = (
                    self.dict_widgets_config[counter_line]["total_questions"].text).replace("/", "")
                if number_questions > int(total_questions):
                    number_questions = 0
                    instance.text = ""
            except:
                number_questions = 0
                instance.text = ""
        self.increase_counter_questions(counter_line, number_questions)

    def add_database(self, counter_line, config_line):
        self.number_lines += 1
        y_pos = 1.1 * self.size_line
        folder_label = create_label_scrollview_simple(
            label_text=config_line["folder"],
            x_size=0.32,
            size_vertical=self.size_line,
            x_pos=0.05,
            y_pos=y_pos
        )
        self.add_widget(folder_label)

        file_label = create_label_scrollview_simple(
            label_text=config_line["file"],
            x_size=0.32,
            size_vertical=self.size_line,
            x_pos=0.39,
            y_pos=y_pos
        )
        self.add_widget(file_label)

        number_questions = config_line["number_questions"]
        number_questions_input = create_text_input_scrollview_simple(
            input_text=str(number_questions),
            placeholder="Nb questions",
            x_size=0.1,
            size_vertical=self.size_line,
            x_pos=0.74,
            y_pos=y_pos,
            write_tab=False,
            multiline=False
        )
        number_questions_input.bind(text=partial(
            self.update_number_questions, counter_line=counter_line))
        self.add_widget(number_questions_input)

        label_questions = create_label_scrollview_simple(
            label_text="/" + str(config_line["total_questions"]),
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
            "folder": folder_label,
            "file": file_label,
            "number_questions": number_questions_input,
            "total_questions": label_questions,
            "former_number_questions": number_questions
        }

        # Update the total number of questions
        self.increase_counter_questions(
            counter_line=counter_line,
            number_questions=number_questions,
            bool_init=True)

        # Scroll to the end of the scroll view when there are enough widgets
        if self.number_lines * self.size_line > self.parent.height:
            self.parent.scroll_y = 0

        return number_questions_input


#####################
### Database menu ###
#####################


class DatabaseWindow(Screen):
    def __init__(self, **kw):
        global DatabaseInst
        self.update_list_folders()
        super().__init__(**kw)
        DatabaseInst = self

    FOLDER_SPINNER_DEFAULT = "Choisir le dossier..."
    FILE_SPINNER_DEFAULT = "Choisir le fichier..."
    NEW_FILE = "Nouveau"
    DICT_SAVE_MESSAGES = {
        "new_folder": "Créer le dossier",
        "new_file": "Créer la nouvelle\nbase de données",
        "edit_database": "Sauvegarder la base\nde données",
        "none": ""
    }
    # Initialise the list of folders available (only second list)
    list_folders = ObjectProperty([FOLDER_SPINNER_DEFAULT, NEW_FILE])
    list_files = ObjectProperty([FILE_SPINNER_DEFAULT])
    name_database = StringProperty("")

    def update_list_folders(self):
        print(get_list_database_folders())
        self.list_folders = get_list_database_folders(15)

    def update_list_files(self, folder_name):
        # Reset the screen when the selected folder has changed
        SVDatabaseInst.reset_screen()
        self.ids.name_database_input.text = ""

        # Default value where to choose the folder
        if folder_name == self.FOLDER_SPINNER_DEFAULT:
            self.list_files = [self.FILE_SPINNER_DEFAULT]
            self.ids.files_spinner.text = self.FILE_SPINNER_DEFAULT
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
            self.ids.files_spinner.text = self.FILE_SPINNER_DEFAULT
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
        self.ids.files_spinner.text = self.FILE_SPINNER_DEFAULT
        self.ids.files_spinner.focus = True
        # Update the list of files according to the selected folder
        self.list_files = [self.FILE_SPINNER_DEFAULT,
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

        if spinner_files_text == self.FILE_SPINNER_DEFAULT:
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
                    print("ERROR IN THE QUESTION")
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

    def reset_screen(self):
        for key in self.dict_widgets_database:
            dict_line = self.dict_widgets_database[key]
            self.remove_widget(dict_line["question"])
            self.remove_widget(dict_line["add_option"])
            for counter_option in range(len(dict_line["options"])):
                self.remove_widget(dict_line["options"][counter_option][0])
                self.remove_widget(dict_line["options"][counter_option][1])
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
            number_questions = len(list_content)
            for counter_line in range(number_questions):
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
        self.add_question_button.on_press = partial(
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
            list_option = self.display_option_line(
                y_pos=(counter_option + 2) * 1.1 * self.size_line + offset,
                counter_option=number_options - counter_option,
                counter_line=counter_line
            )
            list_widgets_options.append(list_option)

        add_option_button = create_button_scrollview_simple(
            button_text="+",
            x_size=0.055,
            size_vertical=self.size_line,
            x_pos=0.5,
            y_pos=1.1 * self.size_line + offset
        )
        add_option_button.on_press = partial(self.add_option, counter_line)
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

    def display_option_line(self, y_pos, counter_option, counter_line, bool_add_option=False):
        if bool_add_option:
            y_pos = self.switch_lines_top(counter_line, 1, switch_options=True)
        text_input_option = create_text_input_scrollview_simple(
            input_text="",
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
        self.add_widget(radio_option)

        if bool_add_option:
            self.rebuild_part_screen(start_counter=counter_line)

        return [text_input_option, radio_option]

    def add_option(self, counter_line):
        self.number_lines += 1
        counter_option = len(
            self.dict_widgets_database[counter_line]["options"]) + 1
        list_option = self.display_option_line(
            y_pos=0,
            counter_option=counter_option,
            counter_line=counter_line,
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
        super().__init__(**kw)

    CLASSES_SPINNER_DEFAULT = "Choisir la classe..."
    # PAUL
    list_classes = ObjectProperty(
        [CLASSES_SPINNER_DEFAULT] + ["Classe 1", "Classe 2"])

    def update_classes(self, class_name):
        SVClassesInst.reset_screen()
        if class_name != self.CLASSES_SPINNER_DEFAULT:
            self.ids.reset_button.disabled = False
            # PAUL
            # Get the content of the class
            class_content = []
            class_content.append(
                {
                    "name_folder": "Fo1",
                    "name_file": "Fi1",
                    "used_questions": 5,
                    "total_questions": 10
                }
            )
            class_content.append(
                {
                    "name_folder": "Fo1",
                    "name_file": "Fi2",
                    "used_questions": 6,
                    "total_questions": 10
                }
            )
            class_content.append(
                {
                    "name_folder": "Fo2",
                    "name_file": "Fi2",
                    "used_questions": 4,
                    "total_questions": 12
                }
            )
            class_content.append(
                {
                    "name_folder": "Fo1",
                    "name_file": "Fi3",
                    "used_questions": 1,
                    "total_questions": 10
                }
            )
            SVClassesInst.display_classes_content(class_content)
            return
        self.ids.reset_button.disabled = True

    def reset_class(self):
        SVClassesInst.reset_screen()
        class_name = self.ids.class_selection.text
        self.ids.reset_button.disabled = True
        self.ids.class_selection.text = self.CLASSES_SPINNER_DEFAULT
        print(class_name)
        # PAUL
        # Reset the data of the class
        # TODO mettre une popup qui affiche un message comme quoi c'est bien fait

    def create_new_class(self):
        SVClassesInst.reset_screen()
        class_name = self.ids.new_class_input.text
        if class_name in self.list_classes:
            # PAUL => est-ce qu'on affiche un message d'erreur avec une popup qui dit que ce n'est pas possible ?
            print("Erreur : la classe existe déjà sous ce nom.")
            return
        elif class_name != "":
            print(class_name)
            # PAUL
            # Create the new class
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
        class_content.sort(
            key=lambda dict_content:
            (dict_content["name_folder"], dict_content["name_file"]))
        list_folders = []

        for dict_content in class_content:
            self.number_lines += 1
            y_pos = 1.1 * self.size_line

            # Get the name of the folder and do not display one twice
            label_folder_text = ""
            folder_name = dict_content["name_folder"]
            if dict_content["name_folder"] not in list_folders:
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
                label_text=dict_content["name_file"],
                x_size=0.2,
                size_vertical=self.size_line,
                x_pos=0.2625,
                y_pos=y_pos
            )

            used_questions = dict_content["used_questions"]
            total_questions = dict_content["total_questions"]
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

    def initialise_screen(self):
        if self.current == "database":
            DatabaseInst.ids.folders_spinner.focus = True
        if self.current == "qcm":
            QCMWindowInst.update_screen()


class QCMMakerApp(App):
    def build(self):
        Window.clearcolor = background_color


if __name__ == "__main__":
    Builder.load_file("data_kivy/extended_style.kv")
    QCMMakerApp().run()
