"""
Module tools Kivy for the scroll views
"""

###############
### Imports ###
###############


### Kivy imports ###

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.floatlayout import FloatLayout

### Python imports ###

from functools import partial

### Module imports ###

from qcm_maker_tools.tools_enhanced_print import (
    print_error,
    print_warning
)
from qcm_maker_tools.tools_kivy import *


########################
### Global Variables ###
########################


# Key of the dictionary for each widget to store its order
ORDER_LINE = "ORDER_LINE"

# Codename to indicate to associate to the button the function to delete the current line
DELETE_LINE_FUNCTION = "DELETE_LINE_FUNCTION"

# Dictionary containing the default values for the button to add a new line at the end of the scroll view
DEFAULT_DICT_BUTTON_ADD_LINE = {
    "text": "+",
    "x_size": 0.05,
    "x_pos": 0.1,
    "size_vertical": 0.8
}

# Dictionary of the code names of each widget
DICT_KEY_WIDGETS = {
    "LABEL": "<class 'kivy.uix.label.Label'>",
    "BUTTON": "<class 'qcm_maker_tools.tools_kivy.FocusableButton'>",
    "TEXT_INPUT": "<class 'qcm_maker_tools.tools_kivy.FocusableTextInput'>",
    "CHECKBOX": "<class 'qcm_maker_tools.tools_kivy.FocusableCheckBox'>",
    "SPINNER": "<class 'qcm_maker_tools.tools_kivy.FocusableSpinner'>",
    "PROGRESS_BAR": "<class 'kivy.uix.progressbar.ProgressBar'>"
}

# Dictionary containing the default values of the attributes which are not specified in the dictionary of each widget
DICT_DEFAULT_VALUES_ATTRIBUTES = {
    "placeholder": "",
    "readonly": False,
    "multiline": True,
    "background_color": (0, 0, 0, 0),
    "function": None,
    "bool_text_size": False,
    "group": None,
    "values": [],
    "max_value": 100,
    "value": 0
}


###################
### ScrollViews ###
###################


def build_scroll_view_dict_default_line(
        key_widget=DICT_KEY_WIDGETS["LABEL"],
        text="",
        x_size=0.1,
        size_vertical=1,
        x_pos=0.1,
        number_line=1,
        total_lines=1,
        other_keys={}):
    dict_widget = {
        "key_widget": key_widget,
        "text": text,
        "x_size": x_size,
        "size_vertical": size_vertical,
        "x_pos": x_pos,
        "number_line": number_line,
        "total_lines": total_lines
    }
    for key in other_keys:
        dict_widget[key] = other_keys[key]
    return dict_widget


class SVLayout(FloatLayout):
    """
    Generic class to create the layout of a scroll view.

    Parameters
    ----------
    dict_default_line: dict of dict
        Dictionary containing the default configuration for a line.
        The keys of this dictionary are the name of the widgets to display.
        The values are dictionaries, whose keys are the name of the attributes of each widget and as values the default value of this attribute.
        This default configuration will be used when adding a new line in the scroll view, if this functionality is on.

    list_content: list of dictionaries
        This list contains the dictionaries of all widgets to display in the scroll view, for each line.
        The keys of the dictionnaries are the names of the widgets (the same as the ones contained in the dict_default_line in theory) and the values are dictionaries, detailing the attributes of each widget.
        The attributes of each widget will overide (for this line) the ones of dict_default_line. Thus, when no attribute is precised, their default value of the dict_default_line will be taken.

    size_line: int
        The size of each line in the scroll view

    dict_button_new_line: dict
        Dictionary containing the information to display the button to add a new line at the end of the scroll view.
        When set to {}, no button is created to add a new line.
    """

    def __init__(self,
                 dict_default_line={},
                 list_content=[],
                 size_line=30,
                 space_between_lines=10,
                 dict_button_new_line={},
                 **kwargs):
        super().__init__(**kwargs)

        # Global style parameters of the scroll view
        self.size_hint = (1, None)
        self.size_line = size_line
        self.number_lines = 0
        self.space_between_lines = space_between_lines
        self.height = (self.number_lines + 1) * \
            (self.size_line + self.space_between_lines)

        # Dictionary storing all widgets of the scroll view. For each subdictionary, called dict_line, it contains the key ORDER_LINE which is not a widget but just the id of the line and whose value can change when adding or deleting lines in the scroll view.
        self.dict_all_widgets = {}
        # Unique key which is incremented at each widget creation
        self.last_key_line = 0
        # Order of the line of the last widget, which is incremented at each widget creation and decremented at each widget deletion
        self.order_line = 0
        # Dictionary of a new line per default
        self.dict_default_line = dict_default_line
        # List containing the content to display by default for the scroll view
        self.list_content = list_content

        # Initialise and build the content of the scroll view layout
        bool_success = self.build_list_all_keys()
        if not bool_success:
            return
        self.build_scroll_view()

        # Button to add a new line at the end of the scroll view
        self.new_line_button = None
        if type(dict_button_new_line) != dict:
            print_error(
                "The attribute set for `dict_button_new_line` is incorrect, it must be a dictionary.")
            return
        # Add the button to add a new line in the scroll view
        if dict_button_new_line != {}:
            self.create_button_add_new_line(dict_button_new_line)

    def build_list_all_keys(self):
        """
        Build the list of keys, ie the key_widget_name, given the dict_default_line.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.list_all_keys = []
        for key_widget_name in self.dict_default_line:
            if key_widget_name != ORDER_LINE:
                self.list_all_keys.append(key_widget_name)
            else:
                print_error(
                    f"The default dictionary given as argument to the scroll view layout contains the key {ORDER_LINE} which is not allowed as a widget name. Please choose an other name for this widget.")
                return False
        return True

    def build_scroll_view(self):
        """
        Build the layout of the scroll view thanks to list_content

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        for dict_line in self.list_content:
            self.display_new_line(
                dict_line=dict_line
            )

    def reset_screen(self):
        """
        Reset the layout of the scroll view by removing all widgets.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        for key_line in self.dict_all_widgets:
            dict_line = self.dict_all_widgets[key_line]
            for key_widget_name in self.list_all_keys:
                if dict_line[key_widget_name] != None:
                    self.remove_widget(dict_line[key_widget_name])
        self.dict_all_widgets = {}
        self.number_lines = 0
        self.height = 0
        if self.new_line_button != None:
            self.remove_widget(self.new_line_button)
            self.new_line_button = None

    def extract_scroll_view_content(self):
        """
        Extract the content of the scroll view in a new list_content.

        Parameters
        ----------
        None

        Returns
        -------
        list_content: list of dict
            The content of the all the widgets.
        """
        list_content = []
        for key_line in self.dict_all_widgets:
            dict_line = self.dict_all_widgets[key_line]
            dict_line_extracted = {}
            for key_widget_name in self.list_all_keys:
                widget = dict_line[key_widget_name]
                if widget != None:
                    key_widget_kivy = str(type(widget))
                    if key_widget_kivy == DICT_KEY_WIDGETS["LABEL"]:
                        dict_line_extracted[key_widget_name] = widget.text
                    elif key_widget_kivy == DICT_KEY_WIDGETS["TEXT_INPUT"]:
                        dict_line_extracted[key_widget_name] = widget.text
                    elif key_widget_kivy == DICT_KEY_WIDGETS["SPINNER"]:
                        dict_line_extracted[key_widget_name] = widget.text
                    elif key_widget_kivy == DICT_KEY_WIDGETS["CHECKBOX"]:
                        dict_line_extracted[key_widget_name] = widget.active
                    elif key_widget_kivy == DICT_KEY_WIDGETS["PROGRESS_BAR"]:
                        dict_line_extracted[key_widget_name] = widget.value
            list_content.append(dict_line_extracted)
        return list_content

    def shift_lines_top(self, start_counter, number_shift):
        """
        Shift to the top all lines whose id is lower than start_counter from a certain amount of lines.

        Parameters
        ----------
        start_counter: int
            The id where to start the shift

        number_shift: int
            The number of lines to shift to the top

        Returns
        -------
        None
        """
        for key_line in self.dict_all_widgets:
            dict_line = self.dict_all_widgets[key_line]
            order_line = dict_line[ORDER_LINE]
            if order_line <= start_counter:
                y_shift = (self.size_line + self.space_between_lines) * \
                    number_shift
                for key in self.list_all_keys:
                    if dict_line[key] != None:
                        dict_line[key].y += y_shift

    def set_all_values_dict_line(self, dict_line):
        """
        Set the values of the dict line to the default value when they have not been associated in the list_content.

        Parameters
        ----------
        dict_line: dict of dict
            Dictionary containing the line specified in list_content

        Returns
        -------
        dict_line: dict of dict
            Dictionary containing the line with all values (completed by the default values)
        """
        for key_widget_name in dict_line:
            dict_widget = dict_line[key_widget_name]
            if key_widget_name in self.dict_default_line:
                dict_default_widget = self.dict_default_line[key_widget_name]
            else:
                print_warning(
                    f"The widget to add called {key_widget_name} of the line {str(self.order_line)} is not specified the default dictionary. It has thus not been displayed. To display it, please add it in the default dictionary.")

                if key_widget_name == ORDER_LINE:
                    print_error(
                        f"The key {ORDER_LINE} is contained in the list of content, which is not allowed as a widget name. The whole line has thus not been displayed. Please choose an other valid name for this widget.")
                    return {}

            for key_attribute in dict_default_widget:
                if key_attribute not in dict_widget:
                    dict_line[key_widget_name][key_attribute] = dict_default_widget[key_attribute]

        return dict_line

    def determine_max_number_lines(self, dict_line):
        """
        Determine the maximum number of sublines inside a line.

        Parameters
        ----------
        dict_line: dict of dict
            Dictionary containing all the widgets of a line

        Returns
        -------
        number_lines_in_line: int
            Maximum number of sublines in this line
        """
        number_lines_in_line = 1
        for key_widget_name in dict_line:
            if number_lines_in_line < dict_line[key_widget_name]["total_lines"]:
                number_lines_in_line = dict_line[key_widget_name]["total_lines"]
        return number_lines_in_line

    def display_new_line(self, dict_line, offset=0):
        """
        Display a line at the bottom of the scroll view.

        Parameters
        ----------
        dict_line: dict of dict
            Dictionary containing all the widgets of the line to display

        offset: int
            Offset used when there is the addition of a new line with the + button.
            It takes into account the position of the button.

        Returns
        -------
        None
        """

        # Initialise the dictionary of all widgets for a new line (so there is no problem for the reset of the screen with missing widgets)
        self.dict_all_widgets[self.last_key_line] = {}
        for key_widget_name in self.list_all_keys:
            self.dict_all_widgets[self.last_key_line][key_widget_name] = None
        self.dict_all_widgets[self.last_key_line][ORDER_LINE] = self.order_line

        dict_line = self.set_all_values_dict_line(dict_line=dict_line)
        if dict_line == {}:
            return
        number_lines_in_line = self.determine_max_number_lines(
            dict_line=dict_line
        )
        if self.last_key_line != 0:
            self.shift_lines_top(
                start_counter=self.last_key_line,
                number_shift=number_lines_in_line
            )

        for key_widget_name in dict_line:
            dict_widget = dict_line[key_widget_name]
            key_widget = dict_widget["key_widget"]

            # Changing some values with codenames
            if ORDER_LINE in dict_widget["text"]:
                dict_widget["text"] = dict_widget["text"].replace(
                    ORDER_LINE, str(self.order_line)
                )

            # Setting global variables for all widgets
            size_vertical = dict_widget["size_vertical"] * \
                self.size_line * dict_widget["total_lines"] + \
                self.space_between_lines * (dict_widget["total_lines"] - 1)
            y_pos = (self.size_line + self.space_between_lines) * \
                dict_widget["number_line"] + offset

            ### Create the new widget ###

            # Label widget
            if key_widget == DICT_KEY_WIDGETS["LABEL"]:
                bool_text_size = self.detect_attribute(
                    dict_widget=dict_widget,
                    key_attribute="bool_text_size"
                )
                current_widget = self.create_label_scrollview_simple(
                    label_text=dict_widget["text"],
                    x_size=dict_widget["x_size"],
                    size_vertical=size_vertical,
                    x_pos=dict_widget["x_pos"],
                    y_pos=y_pos,
                    bool_text_size=bool_text_size
                )

            # Button widget
            elif key_widget == DICT_KEY_WIDGETS["BUTTON"]:
                # Set the default values of the attributes
                function = self.detect_attribute(dict_widget, "function")
                background_color = self.detect_attribute(
                    dict_widget=dict_widget,
                    key_attribute="background_color")
                is_focusable = True
                if function == DELETE_LINE_FUNCTION:
                    is_focusable = False

                # Create the button
                current_widget = self.create_button_scrollview_simple(
                    button_text=dict_widget["text"],
                    x_size=dict_widget["x_size"],
                    size_vertical=size_vertical,
                    x_pos=dict_widget["x_pos"],
                    y_pos=y_pos,
                    is_focusable=is_focusable,
                    background_color=background_color
                )

                # Set the function
                if function != None:
                    if function == DELETE_LINE_FUNCTION:
                        # TODO mon chéri <3
                        current_widget.on_release = self.delete_line
                    else:
                        current_widget.on_release = function

            # Text input widget
            elif key_widget == DICT_KEY_WIDGETS["TEXT_INPUT"]:
                # Set the default values of the attributes
                placeholder = self.detect_attribute(dict_widget, "placeholder")
                readonly = self.detect_attribute(dict_widget, "readonly")
                multiline = self.detect_attribute(dict_widget, "multiline")
                function = self.detect_attribute(dict_widget, "function")

                # Preprocess the order line in the placeholder
                if placeholder != DICT_DEFAULT_VALUES_ATTRIBUTES["placeholder"]:
                    if ORDER_LINE in placeholder:
                        placeholder = placeholder.replace(
                            ORDER_LINE, str(self.order_line)
                        )

                # Create the text input
                current_widget = self.create_text_input_scrollview_simple(
                    input_text=dict_widget["text"],
                    x_size=dict_widget["x_size"],
                    size_vertical=size_vertical,
                    x_pos=dict_widget["x_pos"],
                    y_pos=y_pos,
                    placeholder=placeholder,
                    readonly=readonly,
                    multiline=multiline
                )
                if function != None:
                    current_widget.bind(text=function)

            elif key_widget == DICT_KEY_WIDGETS["CHECKBOX"]:
                # Set the default values of the attributes
                group = self.detect_attribute(dict_widget, "group")
                function = self.detect_attribute(dict_widget, "function")

                # Create the checkbox
                current_widget = self.create_checkbox_scrollview_simple(
                    x_size=dict_widget["x_size"],
                    size_vertical=size_vertical,
                    x_pos=dict_widget["x_pos"],
                    y_pos=y_pos,
                    group=group
                )
                if function != None:
                    current_widget.bind(active=function)

            elif key_widget == DICT_KEY_WIDGETS["SPINNER"]:
                # Set the default values of the attributes
                values = self.detect_attribute(dict_widget, "values")
                function = self.detect_attribute(dict_widget, "function")

                # Create the spinner
                current_widget = self.create_spinner_scrollview_simple(
                    text=dict_widget["text"],
                    values=values,
                    x_size=dict_widget["x_size"],
                    size_vertical=size_vertical,
                    x_pos=dict_widget["x_pos"],
                    y_pos=y_pos
                )
                if function != None:
                    current_widget.bind(text=function)

            elif key_widget == DICT_KEY_WIDGETS["PROGRESS_BAR"]:
                # Set the default values of the attributes
                max_value = self.detect_attribute(dict_widget, "max_value")
                value = self.detect_attribute(dict_widget, "value")

                # Create the progress bar
                current_widget = self.create_progress_bar_scrollview_simple(
                    max_value=max_value,
                    value=value,
                    x_size=dict_widget["x_size"],
                    size_vertical=size_vertical,
                    x_pos=dict_widget["x_pos"],
                    y_pos=y_pos
                )

            # Add the new widget
            self.dict_all_widgets[self.last_key_line][key_widget_name] = current_widget
            self.add_widget(current_widget)

        self.last_key_line += 1
        self.order_line += 1
        self.number_lines += number_lines_in_line
        self.height = (self.number_lines + 1) * \
            (self.size_line + self.space_between_lines)

    def add_new_line(self, dict_line):
        """
        Add a new line at the bottom of the scroll view.
        This function is called only with the add button.

        Parameters
        ----------
        dict_line: dict of dict
            Dictionary of all widgets to display in this new line

        Returns
        -------
        None
        """
        # Display the new line on the scroll view layout
        self.display_new_line(
            dict_line=dict_line,
            offset=self.size_line + self.space_between_lines
        )
        # Reset the dictionary to avoid deepcopy issues
        for key_widget_name in self.list_all_keys:
            dict_line[key_widget_name] = {}
        # Remove and add the widget again to change the order of the focus
        self.remove_widget(self.new_line_button)
        self.add_widget(self.new_line_button)

    def create_button_add_new_line(self, dict_button_new_line):
        """
        Create the button to allow the user to add a new line in the scroll view.

        Parameters
        ----------
        dict_button_new_line: dict
            Dictionary containing the caracteristic of the add button.

        Returns
        -------
        None
        """
        self.new_line_button = self.create_button_scrollview_simple(
            button_text=dict_button_new_line["text"],
            x_size=dict_button_new_line["x_size"],
            size_vertical=self.size_line *
            dict_button_new_line["size_vertical"],
            x_pos=dict_button_new_line["x_pos"],
            y_pos=self.size_line + self.space_between_lines,
            is_focusable=True,
            background_color=DICT_DEFAULT_VALUES_ATTRIBUTES["background_color"]
        )
        dict_line = {}
        for key_widget_name in self.list_all_keys:
            dict_line[key_widget_name] = {}
        self.new_line_button.on_release = partial(
            self.add_new_line,
            dict_line
        )
        self.add_widget(self.new_line_button)
        self.number_lines += 1
        self.height = (self.number_lines + 1) * \
            (self.size_line + self.space_between_lines)
        self.shift_lines_top(
            start_counter=self.last_key_line,
            number_shift=1
        )

    def delete_line(self):
        # TODO ce sont les order_line qui doivent changer et pas les last_key (pour last_key, tant pis s'il y a des trous en plus milieu)
        # Du coup il faudra que les Labels et les placeholder avec leur numéro soient changés ;) Pour cela, tu peux détecter le ORDER_LINE (ie le code qui montre qu'il faut remplacer) dans le self.dict_default_line
        # La valeur du décalage lors de la suppression d'une ligne c'est self.size_line*number_lines_in_line - self.space_between_lines (o*ù number_lines_in_line correspond au nombre de sous-lignes qu'il y avait dans la ligne supprimée)
        pass

    def detect_attribute(self, dict_widget, key_attribute):
        """
        Detect if an attribute is present in the dict_widget. If not return the default value.

        Parameters
        ----------
        dict_widget: dict
            Dictionary containing the caracteristic of a widget
        key_attribute: str
            Name of the attribute

        Returns
        -------
        attribute_value: str
            Value of the attribute, may it be the default or not
        """
        if key_attribute in dict_widget:
            attribute_value = dict_widget[key_attribute]
        else:
            attribute_value = DICT_DEFAULT_VALUES_ATTRIBUTES[key_attribute]
        return attribute_value

    ########################
    ### Widgets creation ###
    ########################

    def create_label_scrollview_simple(self, label_text, x_size, size_vertical, x_pos, y_pos, bool_text_size):
        """
        Create a label for a simple vertical scrollview.
        """
        label = Label(
            text=label_text,
            color=color_label,
            size_hint=(x_size, None),
            height=size_vertical,
            pos_hint={"x": x_pos},
            y=y_pos,
            shorten=False,
            text_size=(x_size * Window.size[0] * 0.95, None),
            halign="center")
        if bool_text_size:
            label.text_size = label.size
            label.halign = "left"
            label.valign = "center"
        return label

    def create_button_scrollview_simple(self, button_text, x_size, size_vertical, x_pos, y_pos, is_focusable, background_color):
        """
        Create a button for a simple vertical scrollview.
        """
        if is_focusable:
            button = FocusableButton(
                text=button_text,
                size_hint=(x_size, None),
                height=size_vertical,
                pos_hint={"x": x_pos},
                y=y_pos,
                halign="center",
                scroll_to=True)
        else:
            button = Button(
                text=button_text,
                size_hint=(x_size, None),
                height=size_vertical,
                pos_hint={"x": x_pos},
                y=y_pos,
                halign="center",
                background_color=background_color)
        return button

    def create_checkbox_scrollview_simple(sel, x_size, size_vertical, x_pos, y_pos, group):
        """
        Create a button for a simple vertical scrollview.
        """
        checkbox = FocusableCheckBox(
            size_hint=(x_size, None),
            height=size_vertical,
            pos_hint={"x": x_pos},
            y=y_pos,
            group=group, scroll_to=True)
        return checkbox

    def create_text_input_scrollview_simple(self, input_text, x_size, size_vertical, x_pos, y_pos, placeholder, readonly, multiline):
        """
        Create a text input for a simple scrollview.
        """
        text_input = FocusableTextInput(
            text=input_text,
            size_hint=(x_size, None),
            height=size_vertical,
            pos_hint={"x": x_pos},
            y=y_pos,
            selection_color=highlight_text_color,
            multiline=multiline,
            hint_text=placeholder,
            readonly=readonly,
            scroll_to=True)
        return text_input

    def create_progress_bar_scrollview_simple(self, max_value, value, x_size, size_vertical, x_pos, y_pos):
        """
        Create a progress bar for a simple scrollview.
        """
        progress_bar = ProgressBar(
            max=max_value,
            value=value,
            pos_hint={"x": x_pos},
            size_hint=(x_size, None),
            y=y_pos,
            height=size_vertical
        )
        return progress_bar

    def create_spinner_scrollview_simple(self, text, values, x_size, size_vertical, x_pos, y_pos):
        """
        Create a spinner for a simple scrollview.
        """
        spinner = FocusableSpinner(
            text=text,
            values=values,
            pos_hint={"x": x_pos},
            size_hint=(x_size, None),
            y=y_pos,
            height=size_vertical,
            scroll_to=True
        )
        return spinner
