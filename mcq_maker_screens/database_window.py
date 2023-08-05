"""
Module database window of MCQMaker

Create the class for the database window and build the associated kv file.

Classes
-------
DatabaseWindow : Screen
    Screen used for the database menu.
DatabaseScrollView : ScrollView
    ScrollView contained inside the menu.
"""


###############
### Imports ###
###############


### Python imports ###

from functools import partial

### Kivy imports ###

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, StringProperty

### Modules imports ###

from mcq_maker_tools.tools import (
    DICT_LANGUAGE,
    PATH_KIVY_FOLDER,
    PATH_RESOURCES_FOLDER
)
from mcq_maker_tools.tools_database import (
    get_list_database_files,
    get_list_database_folders,
    create_database_folder,
    save_database,
    load_database,
    delete_folder,
    delete_file
)
from mcq_maker_tools.tools_kivy import (
    DICT_MESSAGES,
    DICT_BUTTONS,
    create_standard_popup,
    create_button_scrollview_simple,
    create_label_scrollview_simple,
    create_button_scrollview_simple_no_focus,
    create_text_input_scrollview_simple,
    create_checkbox_scrollview_simple,
    ImprovedPopup
)


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

    def init_screen(self, dict_init_database=None):
        self.ids.save_button.on_release = self.save_database
        self.list_folders = [
            self.manager.FOLDER_SPINNER_DEFAULT,
            self.NEW_FILE] + \
            get_list_database_folders()
        if dict_init_database is None:
            self.ids.folders_spinner.focus = True
            if self.ids.folders_spinner.text == self.manager.FOLDER_SPINNER_DEFAULT:
                self.list_files = [self.manager.FILE_SPINNER_DEFAULT]
        else:
            self.ids.folders_spinner.text = dict_init_database["folder_name"]
            self.ids.files_spinner.text = self.NEW_FILE
            self.ids.name_database_input.text = dict_init_database["file_name"]
            self.ids.save_button.focus = True
            SVDatabaseInst.initialise_database(
                list_content=dict_init_database["mcq_data"])

    def partial_reset_after_creation(self):
        # Update the list of files according to the selected folder
        self.list_files = [self.manager.FILE_SPINNER_DEFAULT, self.NEW_FILE] + \
            get_list_database_files(
                folder_name=self.ids.folders_spinner.text)
        self.ids.files_spinner.text = self.name_database
        self.ids.name_database_input.disabled = True
        self.ids.name_database_input.hint_text = ""
        self.ids.save_button.text = self.DICT_SAVE_MESSAGES["edit_database"]

    def reset_screen_default_folder(self):
        self.list_files = [self.manager.FILE_SPINNER_DEFAULT]
        self.ids.files_spinner.text = self.manager.FILE_SPINNER_DEFAULT
        self.ids.files_spinner.disabled = True
        self.ids.name_database_input.disabled = True
        self.ids.name_database_input.hint_text = ""
        self.ids.save_button.disabled = True
        self.ids.save_button.text = self.DICT_SAVE_MESSAGES["none"]
        self.ids.delete_button.disabled = True
        self.ids.delete_image.source = "resources/trash_disabled_logo.png"
        self.ids.folders_spinner.focus = True

    def update_list_files(self, folder_name):
        # Reset the screen when the selected folder has changed
        SVDatabaseInst.reset_screen()
        self.ids.name_database_input.text = ""

        # Default value where to choose the folder
        if folder_name == self.manager.FOLDER_SPINNER_DEFAULT:
            self.reset_screen_default_folder()
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
            self.ids.delete_button.disabled = True
            self.ids.delete_image.source = "resources/trash_disabled_logo.png"
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
        self.ids.delete_button.disabled = False
        self.ids.delete_image.source = "resources/trash_logo.png"
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
            self.name_database = ""
            self.ids.name_database_input.disabled = False
            self.ids.name_database_input.hint_text = self.DICT_INPUT_MESSAGES["new_file"]
            self.ids.name_database_input.text = ""
            self.ids.name_database_input.focus = True
            self.ids.save_button.disabled = False
            self.ids.save_button.text = self.DICT_SAVE_MESSAGES["new_file"]
            self.ids.delete_button.disabled = True
            self.ids.delete_image.source = "resources/trash_disabled_logo.png"
            SVDatabaseInst.initialise_database()
            return

        if spinner_files_text == self.manager.FILE_SPINNER_DEFAULT:
            self.name_database = self.manager.FILE_SPINNER_DEFAULT
            self.ids.name_database_input.hint_text = ""
            self.ids.name_database_input.disabled = True
            self.ids.name_database_input.text = ""
            self.ids.save_button.disabled = True
            self.ids.save_button.text = self.DICT_SAVE_MESSAGES["none"]
            self.ids.files_spinner.focus = True
            self.ids.delete_button.disabled = False
            self.ids.delete_image.source = "resources/trash_logo.png"
            return

        # Edit a former database
        self.ids.name_database_input.disabled = True
        self.ids.name_database_input.hint_text = ""
        self.ids.save_button.disabled = False
        self.ids.save_button.text = self.DICT_SAVE_MESSAGES["edit_database"]
        self.ids.delete_button.disabled = False
        self.ids.delete_image.source = "resources/trash_logo.png"
        self.name_database = spinner_files_text
        list_content = load_database(spinner_files_text, spinner_folder_text)
        SVDatabaseInst.initialise_database(list_content=list_content)

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
                # Delete the empty options to avoid the shift of indices
                list_options = [
                    option for option in list_options if option[0].text != ""]
                # Get the options in the right order (so they are always display in the same order in the scroll view)
                for counter_option in range(len(list_options) - 1, -1, -1):
                    option = list_options[counter_option]
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

    def open_delete_popup_confirmation(self):
        """
        Open a popup of confirmation when deleting a file.

        Paramaters
        ----------
        None

        Returns
        -------
        None
        """
        message_code = "delete_folder"
        if self.ids.files_spinner.text != self.manager.FILE_SPINNER_DEFAULT:
            message_code = "delete_file"
        # Create the popup
        popup = ImprovedPopup(
            title=DICT_MESSAGES[message_code][0],
            add_content=[])

        # Add the label and both buttons
        popup.add_label(
            text=DICT_MESSAGES[message_code][1],
            pos_hint={"x": 0.1, "y": 0.6},
            size_hint=(0.8, 0.15)
        )
        popup.add_button(
            text=DICT_BUTTONS["yes"],
            pos_hint={"x": 0.1, "y": 0.25},
            size_hint=(0.35, 0.15),
            on_release=partial(self.delete_file, message_code, popup)
        )
        popup.add_button(
            text=DICT_BUTTONS["no"],
            pos_hint={"x": 0.55, "y": 0.25},
            size_hint=(0.35, 0.15),
            on_release=popup.dismiss
        )

    def delete_file(self, type_delete, popup):
        """
        Delete the folder or the file of the database.

        Parameters
        ----------
        type_delete : Literal["delete_file", "delete_folder"]
            Whether it is a folder or a file to delete

        popup : ImprovedPopup
            Popup of confirmation to dismiss

        Returns
        -------
        None
        """
        popup.dismiss()
        if type_delete == "delete_file":
            code_message = "success_delete_file"
            delete_file(
                folder_name=self.ids.folders_spinner.text,
                file_name=self.ids.files_spinner.text)
            self.init_screen_existing_folder(
                list_files=[
                    self.manager.FILE_SPINNER_DEFAULT, self.NEW_FILE] +
                get_list_database_files(self.ids.folders_spinner.text))
        elif type_delete == "delete_folder":
            code_message = "success_delete_folder"
            delete_folder(folder_name=self.ids.folders_spinner.text)
            self.ids.folders_spinner.text = self.manager.FOLDER_SPINNER_DEFAULT
            self.reset_screen_default_folder()
        create_standard_popup(
            message=DICT_MESSAGES[code_message][1],
            title_popup=DICT_MESSAGES[code_message][0]
        )


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
            self.remove_widget(dict_line["delete_image"])
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

    def initialise_database(self, list_content=[]):
        # Delete all widgets of the screen
        self.reset_screen()

        # Add each question
        if list_content != []:
            nb_questions = len(list_content)
            for counter_line in range(nb_questions):
                print(list_content)
                print(counter_line)
                print(list_content[counter_line])
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
            button_text=DatabaseInst.TEXT_DATABASE["add_question"],
            x_size=0.7,
            size_vertical=self.size_line,
            x_pos=0.1,
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

    def delete_question(self, *args, question_id=0, **kwargs):

        # Recover the widgets of the question
        temp_dict_widgets = self.dict_widgets_database[question_id]

        # Remove them
        for key in list(temp_dict_widgets.keys()):
            if key != "options":
                # Remove the focus to avoid errors
                try:
                    if temp_dict_widgets[key].focus:
                        temp_dict_widgets[key].focus = False
                except:
                    pass
                self.remove_widget(temp_dict_widgets[key])
            else:
                number_widgets = 2 + len(temp_dict_widgets["options"])
                for list_option_widgets in temp_dict_widgets["options"]:
                    for option_widget in list_option_widgets:
                        if option_widget.focus:
                            option_widget.focus = False
                        self.remove_widget(option_widget)

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

        delete_image = Image(
            source=PATH_RESOURCES_FOLDER+"trash_logo.png",
            pos_hint={"x": 0.85},
            size_hint=(None, None),
            allow_strech=True,
            height=self.size_line,
            width=self.size_line,
            y=number_widgets * 1.1 * self.size_line + offset
        )
        self.add_widget(delete_image)
        delete_function = partial(
            self.delete_question, question_id=counter_line)
        self.delete_function_dict[counter_line] = delete_function
        delete_button = create_button_scrollview_simple_no_focus(
            button_text="",
            x_size=0.05,
            size_vertical=self.size_line,
            x_pos=0.85,
            y_pos=number_widgets * 1.1 * self.size_line + offset,
            background_color=(0, 0, 0, 0),
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
            button_text=DatabaseInst.TEXT_DATABASE["add_option"],
            x_size=0.4,
            size_vertical=self.size_line,
            x_pos=0.1625,
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
            "delete": delete_button,
            "delete_image": delete_image
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
                dict_line["delete_image"].y += y_switch
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
                dict_line["delete_image"].y -= y_switch
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


### Build associated kv file ###

Builder.load_file(PATH_KIVY_FOLDER + "DatabaseWindow.kv")
