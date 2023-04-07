###############
### Imports ###
###############


### Kivy imports ###

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, StringProperty

### Python imports ###

from functools import partial

### File imports ###

from Module.tools_kivy import *


#################
### Main menu ###
#################


class MenuWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    def change_label_popup(self, label_popup, progress_bar_popup):
        label_popup.text = "I've changed"
        progress_bar_popup.value += 10

    def open_generic_popup(self):
        ImprovedPopup(title="Title of the popup window", add_content=[
                      ("label", {"text": "Test label"})])

    def open_personalised_popup(self):
        popup_content = [("label", {"text": "Test label"}),
                         ("spinner", {"text": "EX 1", "values": ["EX 1", "EX 2"], "pos_hint":{
                          "x": 0.1, "top": 0.65}, "size_hint": (0.4, 0.1)})]

        popup = ImprovedPopup(title="This is a popup",
                              add_content=popup_content)
        popup.add_progress_bar()
        popup.add_button(text="Increase progress",
                         pos_hint={"x": 0.1, "top": 0.45}, on_release=partial(popup.modify_progress, 10, "increase"), size_hint=(0.8, 0.15))
        popup.add_button(text="Reset progress",
                         pos_hint={"x": 0.1, "top": 0.2}, on_release=partial(popup.modify_progress, 0, "set"), size_hint=(0.8, 0.15))


################
### QCM menu ###
################


class QCMWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    NEW_CONFIG = "Nouveau"
    CLASSES_SPINNER_DEFAULT = "Choisir la classe..."
    # PAUL => mettre la valeur par défaut du template précédemment utilisé
    TEMPLATE_SPINNER_DEFAULT = "T1"
    list_classes = ObjectProperty([""])
    # PAUL
    list_templates = ObjectProperty(["T1", "T2", "T3"])
    number_questions_label = StringProperty("Nombre de questions : 0")
    default_config = {
        "config_name": ""
    }

    def load_config(self):
        # TODO
        # Ouvrir une popup qui demande quelle configuration choisir, et qui laisse le choix avec nouveau
        config_name = self.NEW_CONFIG
        self.ids.config_name_input.disabled = False
        self.ids.save_config_button.disabled = False
        self.ids.template_spinner.disabled = False
        self.ids.generate_qcm_button.disabled = False
        self.ids.config_name_input.hint_text = "Nom de la configuration"
        # PAUL
        self.list_classes = [self.CLASSES_SPINNER_DEFAULT] + ["Classe 1", "Classe 2"]
        if config_name == self.NEW_CONFIG:
            self.ids.config_name_input.focus = True
            self.ids.classes_spinner.text = self.CLASSES_SPINNER_DEFAULT
            self.ids.classes_spinner.disabled = False
            SVQCMInst.display_config(self.default_config)
        else:
            self.extract_config(config_name)

    def extract_config(self, config_name):
        # TODO use the format of the config to change correctly the widgets and then display in the scrollview
        config = {
            "config_name": config_name,
            "class": "C1"
        }
        self.ids.classes_spinner.disabled = True
        self.ids.classes_spinner.text = config["class"]
        SVQCMInst.display_config(config)

    def generate_qcm(self):
        config_name = self.ids.config_name_input.text
        if config_name == "":
            # TODO message d'erreur dans popup
            print("Erreur, la configuration n'a pas de nom")
            return
        qcm_name = config_name + "_" + self.ids.classes_spinner.text
        # TODO
        # Extract the configuration from the scroll view

        # PAUL
        # Launch the generation of both qcm (txt and docx)

# TODO METTRE DANS LA SCROLLVIEW LE SPINNER POUR FILE ET FOLDER A CHAQUE FOIS

class QCMScrollView(FloatLayout):
    """
    Class displaying the scrollview for the creation of the QCM.
    """
    def __init__(self, **kwargs):
        global SVQCMInst
        super().__init__(**kwargs)
        SVQCMInst = self

    number_lines = ObjectProperty(0)
    size_line = ObjectProperty(35)
    dict_widgets_config = {}
    FOLDER_SPINNER_DEFAULT = "Choisir le dossier..."
    FILE_SPINNER_DEFAULT = "Choisir le fichier..."
    default_database = {}

    def display_config(self, config):
        for i in range(30):
            self.add_database(i, {})

        # Add the button to add a new database
        self.switch_lines_top(len(self.dict_widgets_config.keys()), 1)
        self.add_question_button = create_button_scrollview_simple(
            button_text="+",
            x_size=0.07,
            size_vertical=self.size_line,
            x_pos=0.0375,
            y_pos=1.1*self.size_line
        )
        self.add_question_button.on_press = partial(
            self.new_database,
            self.default_database
        )
        self.add_widget(self.add_question_button)
        self.number_lines += 1

    def switch_lines_top(self, start_counter, number_switch):
        for key in self.dict_widgets_config:    
            dict_line = self.dict_widgets_config[key]
            if key <= start_counter:
                y_switch = 1.1*self.size_line*number_switch
                dict_line["folder"].y += y_switch
                dict_line["file"].y += y_switch
                dict_line["number_questions"].y += y_switch
                for widget in dict_line["other_widgets"]:
                    widget.y += y_switch

    def new_database(self, dict_content):
        text_input_question = self.add_database(
            counter_line=len(self.dict_widgets_config.keys()),
            config_line={},
            bool_new_database=True
        )
        text_input_question.focus = True
        self.remove_widget(self.add_question_button)
        self.add_widget(self.add_question_button)

    def add_database(self, counter_line, config_line, bool_new_database=False):
        offset = 0
        if bool_new_database:
            offset = 1.1*self.size_line
        self.number_lines += 1
        spinner_folder = create_spinner_scrollview_simple(
            text=self.FOLDER_SPINNER_DEFAULT,
            values=[self.FOLDER_SPINNER_DEFAULT] + ["Fo1", "Fo2"], # PAUL
            x_size=0.25,
            size_vertical=self.size_line,
            x_pos=0.05,
            y_pos=1.1*self.size_line+offset
        )
        self.add_widget(spinner_folder)

        spinner_file = create_spinner_scrollview_simple(
            text=self.FILE_SPINNER_DEFAULT,
            values=[self.FILE_SPINNER_DEFAULT] + ["Fi1", "Fi2"], # PAUL
            x_size=0.25,
            size_vertical=self.size_line,
            x_pos=0.35,
            y_pos=1.1*self.size_line+offset
        )
        self.add_widget(spinner_file)

        number_questions_input = create_text_input_scrollview_simple(
            input_text="",
            placeholder="Nb questions",
            x_size=0.1,
            size_vertical=self.size_line,
            x_pos=0.65,
            y_pos=1.1*self.size_line+offset,
            write_tab=False,
            multiline=False
        )
        self.add_widget(number_questions_input)

        label_questions = create_label_scrollview_simple(
            label_text="/1", # TO CHANGE
            x_size=0.1,
            size_vertical=self.size_line,
            x_pos=0.8,
            y_pos=1.1*self.size_line+offset,
            bool_text_size=True
        )
        self.add_widget(label_questions)

        self.switch_lines_top(start_counter=counter_line, number_switch=1)
        
        # Update the dictionary of widgets for each question
        self.dict_widgets_config[counter_line] = {
            "id_line": counter_line,
            "folder": spinner_folder,
            "file": spinner_file,
            "number_questions": number_questions_input,
            "other_widgets": [label_questions]
        }

        return number_questions_input


#####################
### Database menu ###
#####################


class DatabaseWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    FOLDER_SPINNER_DEFAULT = "Choisir le dossier..."
    FILE_SPINNER_DEFAULT = "Choisir le fichier..."
    NEW_FILE = "Nouveau"
    DICT_SAVE_MESSAGES = {
        "new_folder": "Créer le dossier",
        "new_file": "Créer la nouvelle\nbase de données",
        "edit_database": "Sauvegarder la base\nde données"
    }
    # PAUL
    # Initialise the list of folders available (only second list)
    list_folders = ObjectProperty([FOLDER_SPINNER_DEFAULT, NEW_FILE] + ["Fo1", "Fo2"])
    list_files = ObjectProperty([FILE_SPINNER_DEFAULT])
    name_database = StringProperty("")

    def update_list_files(self, spinner_folder_text):
        # Reset the screen when the selected folder has changed
        SVDatabaseInst.reset_screen()
        self.ids.name_database_input.text = ""

        # Default value where to choose the folder
        if spinner_folder_text == self.FOLDER_SPINNER_DEFAULT:
            self.list_files = [self.FILE_SPINNER_DEFAULT]
            self.ids.files_spinner.text = self.FILE_SPINNER_DEFAULT
            self.ids.name_database_input.disabled = True
            self.ids.name_database_input.hint_text = ""
            self.ids.save_button.disabled = True
            self.ids.save_button.text = ""
            return
        
        # Create a new folder
        if spinner_folder_text == self.NEW_FILE:
            self.list_files = []
            self.ids.files_spinner.text = ""
            self.ids.name_database_input.disabled = False
            self.ids.name_database_input.hint_text = "Nom du nouveau dossier"
            self.ids.save_button.disabled = False
            self.ids.save_button.text = self.DICT_SAVE_MESSAGES["new_folder"]
            return

        # Real folder selected
        self.ids.name_database_input.disabled = True
        self.ids.name_database_input.hint_text = ""
        self.ids.save_button.disabled = True
        self.ids.save_button.text = ""
        self.ids.files_spinner.text = self.FILE_SPINNER_DEFAULT
        # PAUL
        # Update the list of files according to the selected folder
        self.list_files = [self.FILE_SPINNER_DEFAULT, self.NEW_FILE] + ["Fi1", "Fi2"]

    def update_scroll_view_database(self, spinner_folder_text, spinner_files_text):
        # Reset the screen when the selected file has changed
        SVDatabaseInst.reset_screen()
        self.ids.name_database_input.text = ""

        # Create a new database
        if spinner_files_text == self.NEW_FILE:
            self.ids.name_database_input.disabled = False
            self.ids.name_database_input.hint_text = "Nom de la nouvelle base de données"
            self.ids.save_button.disabled = False
            self.ids.save_button.text = self.DICT_SAVE_MESSAGES["new_file"]
            SVDatabaseInst.initialise_database(spinner_folder_text, "")

        # Edit a former database
        elif spinner_files_text not in [self.FILE_SPINNER_DEFAULT, ""]:
            self.ids.name_database_input.disabled = True
            self.ids.name_database_input.hint_text = ""
            self.ids.save_button.disabled = False
            self.ids.save_button.text = self.DICT_SAVE_MESSAGES["edit_database"]
            SVDatabaseInst.initialise_database(spinner_folder_text, spinner_files_text)

    def save_database(self):
        button_text = self.ids.save_button.text
        if button_text == self.DICT_SAVE_MESSAGES["new_folder"]:
            # PAUL
            # Create the new directory
            return

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
            dict_content = self.default_question_content
            number_questions = 5
            for counter_line in range(number_questions):
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
            y_pos=1.1*self.size_line
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
            offset = 1.1*self.size_line
        number_options = len(dict_content["options"])
        number_widgets = 2 + number_options
        text_input_question = create_text_input_scrollview_simple(
            input_text="",
            x_size=0.7,
            size_vertical=self.size_line,
            x_pos=0.0375,
            y_pos=number_widgets*1.1*self.size_line+offset,
            placeholder="Question",
            write_tab=False,
            multiline=False
        )
        self.add_widget(text_input_question)

        list_widgets_options = []
        for counter_option in range(number_options-1, -1, -1):
            list_option = self.display_option_line(
                y_pos=(counter_option+2)*1.1*self.size_line + offset,
                counter_option=number_options-counter_option,
                counter_line=counter_line
            )
            list_widgets_options.append(list_option)

        add_option_button = create_button_scrollview_simple(
            button_text="+",
            x_size=0.055,
            size_vertical=self.size_line,
            x_pos=0.5,
            y_pos=1.1*self.size_line+offset
        )
        add_option_button.on_press = partial(self.add_option, counter_line)
        self.add_widget(add_option_button)
        
        self.number_lines += number_widgets
        self.switch_lines_top(start_counter=counter_line, number_switch=number_widgets)
        
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
                y_switch = 1.1*self.size_line*number_switch
                dict_line["question"].y += y_switch
                if key != start_counter or not switch_options:
                    dict_line["add_option"].y += y_switch
                else:
                    y_pos = dict_line["add_option"].y + 1.1*self.size_line
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
            placeholder="Option "+str(counter_option),
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
        counter_option = len(self.dict_widgets_database[counter_line]["options"]) + 1
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
    list_classes = ObjectProperty([CLASSES_SPINNER_DEFAULT] + ["Classe 1", "Classe 2"])

    def update_classes(self, class_name):
        SVClassesInst.reset_screen()
        if class_name != self.CLASSES_SPINNER_DEFAULT:
            self.ids.reset_button.disabled = False
            # PAUL
            # Get the content of the class
            class_content = []
            for i in range(10):
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
                        "used_questions": 4,
                        "total_questions": 12
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

    def display_classes_content(self, class_content):
        """
        Create the widgets for the scrollview for the corresponding class
        
        Parameters
        ----------
        class_content: list of dict
            List containing the information for each file of the database.
        """
        # TODO TRIER PAR FOLDER ET SEULEMENT AFFICHER LA PREMIERE OCCURENCE
        for dict_content in class_content:
            self.number_lines += 1
            y_pos = 1.1*self.size_line*self.number_lines
            label_folder = create_label_scrollview_simple(
                label_text=dict_content["name_folder"],
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
                label_text=str(used_questions)+"/"+str(total_questions),
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
        self.pos_hint = {"x":0, "y":0.925}
        self.size_hint = (1, 0.075)
        self.cols = 3


###############
### General ###
###############


class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.highlight_text_color = highlight_text_color
        self.button_gray_color = (
            2 * blue_color[0], 2 * blue_color[1], 2 * blue_color[2], blue_color[3])
        self.button_pink_color = (
            2 * pink_color[0], 2 * pink_color[1], 2 * pink_color[2], pink_color[3])
        self.color_label = color_label
        self.transition = NoTransition()


class MainApp(App):
    def build(self):
        Window.clearcolor = background_color


if __name__ == "__main__":
    Builder.load_file("data_kivy/extended_style.kv")
    MainApp().run()
