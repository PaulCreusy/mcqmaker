"""
Module tools kivy of QCMMaker
"""

###############
### Imports ###
###############


from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import FocusBehavior


########################
### Global Variables ###
########################


### Kivy light theme ###

size_popup = (dp(400), dp(400))
highlight_text_color = (156 / 255, 0, 60 / 255, 0.5)
background_color = (230 / 255, 230 / 255, 230 / 255, 1)
color_label = (0, 0, 0, 1)
gray_color = (134 / 255, 122 / 255, 151 / 255, 1)
pink_color = (156 / 255, 0, 60 / 255, 1)


### Messages in popups ###

# Dictionnary of the text for the button in popups
dict_buttons = {"Normal": "Close this popup."}

key_error = "Error"
# Dictionnary of messages in popup whose values are [titre_popup_error, message_error, message_button]
dict_errors = {"Error": ["Error", "An error occured.", dict_buttons["Normal"]],
               "Generic": ["A generic popup", "This is a generic popup.", dict_buttons["Normal"]], }


#####################
### Popup windows ###
#####################


def blank_function(*args, **kwargs):
    """
    Fonction qui ne fait rien.
    """
    pass


class ImprovedPopupLayout(FloatLayout):
    """
    Class used to make the background of the popup with the pink line
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    pink_color = pink_color
    size_popup = size_popup


class ImprovedPopup(Popup):
    """
    Class used to easily create popups
    """

    def __init__(self, title="Popup", size_hint=(None, None), auto_dismiss=False, add_content=[], size=(dp(400), dp(400))):
    
        # Initialisation du layout contenant les objets du popup
        self.layout = ImprovedPopupLayout()
        # Initialisation du popup par héritage
        super().__init__(title=title, size_hint=size_hint,
                         auto_dismiss=auto_dismiss, content=self.layout, size=size)
        # Ajout du bouton de fermeture
        self.add_close_button()
        # Ajout des composants voulus
        correspondance_list = [("label", self.add_label),
                               ("textinput", self.add_text_input),
                               ("spinner", self.add_spinner),
                               ("progress_bar", self.add_progress_bar),
                               ("button", self.add_button),
                               ("widget", self.add_other_widget)]
        for instruction in add_content:
            for i in range(len(correspondance_list)):
                if instruction[0] == correspondance_list[i][0]:
                    correspondance_list[i][1](**instruction[1])
        # Ouverture du popup
        self.open()

    def add_close_button(self):
        pos_hint = {"center_x": 0.9, "center_y": 0.9}
        size_hint = (0.07, 0.07)
        close_button = Button(background_color=(
            0, 0, 0, 0), pos_hint=pos_hint, size_hint=size_hint)
        close_button.on_release = self.dismiss
        close_button_image = Image(source="ressources/close_button.png",
                                   pos_hint=pos_hint, size_hint=size_hint)
        self.layout.add_widget(close_button)
        self.layout.add_widget(close_button_image)

    def add_label(self, text="", size_hint=(0.6, 0.2), pos_hint={"x": 0.2, "top": 0.9}, halign="center", **kwargs):
        label = Label(text=text,
                      size_hint=size_hint,
                      pos_hint=pos_hint,
                      halign=halign, **kwargs)
        self.layout.add_widget(label)

    def add_text_input(self, text="", pos_hint={"x": 0.1, "top": 0.7}, size_hint=(0.8, 0.2), multiline=False, **kwargs):
        text_input = TextInput(text=text,
                               size_hint=size_hint,
                               pos_hint=pos_hint,
                               selection_color=highlight_text_color,
                               multiline=multiline, **kwargs)
        self.layout.add_widget(text_input)

    def add_spinner(self, text="Spinner", values=["Spin 1", "Spin 2"], size_hint=(0.6, 0.2), pos_hint={"x": 0.2, "top": 0.7}, halign="center", **kwargs):
        spinner = Spinner(text=text,
                          values=values,
                          size_hint=size_hint,
                          pos_hint=pos_hint,
                          halign=halign, **kwargs)
        self.layout.add_widget(spinner)

    def add_progress_bar(self, max=100, pos_hint={"center_x": 0.5, "top": 0.85}, size_hint=(0.5, 0.25), **kwargs):
        progress_bar = ProgressBar(max=max,
                                   pos_hint=pos_hint,
                                   size_hint=size_hint, **kwargs)
        # On ajoute progress_bar dans self pour pouvoir incrémenter la valeur derrière
        self.progress_bar = progress_bar
        self.layout.add_widget(progress_bar)

    def add_button(self, text="", disabled=False, size_hint=(0.8, 0.2), pos_hint={"x": 0.1, "top": 0.45}, halign="center", on_release=blank_function, **kwargs):
        button = Button(text=text,
                        size_hint=size_hint,
                        pos_hint=pos_hint,
                        halign=halign,
                        disabled=disabled, on_release=on_release, **kwargs)
        self.layout.add_widget(button)

    def add_other_widget(self, widget_class, **kwargs):
        widget = widget_class(**kwargs)
        self.layout.add_widget(widget)

    def modify_progress(self, value: int, mode: str, *args):
        if self.progress_bar is not None:
            if mode == "set":
                self.progress_bar.value = value
            elif mode == "increase":
                self.progress_bar.value += value


#######################
### Focusable items ###
#######################


class FocusableButton(FocusBehavior, Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (
            2 * gray_color[0], 2 * gray_color[1], 2 * gray_color[2], gray_color[3])
        # Window.bind(mouse_pos=self.on_mouse_pos)
        # self.children.append(ToolTip(text="hello", opacity=0)) #METTRE LA CLASSE TOOLTIP DANS EXTENDED STYLE

    def on_focus(self, instance, value, *args):
        if value:
            self.background_color = (
            2 * pink_color[0], 2 * pink_color[1], 2 * pink_color[2], pink_color[3])
        else:
            self.background_color = (
            2 * gray_color[0], 2 * gray_color[1], 2 * gray_color[2], gray_color[3])

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        key = keycode[-1]
        if key in ("spacebar", "enter"):
            self.on_press()
        return super(FocusableButton, self).keyboard_on_key_down(window, keycode, text, modifiers)
    
    # def on_mouse_pos(self, *args):
    #     if not self.get_root_window():
    #         return
    #     pos = args[1]
    #     self.children[0].pos = pos
    #     Clock.unschedule(self.display_tooltip) # cancel scheduled event since I moved the cursor
    #     self.close_tooltip() # close if it's opened
    #     if self.collide_point(*self.to_widget(*pos)):
    #         Clock.schedule_once(self.display_tooltip, 0.5)

    # def close_tooltip(self, *args):
    #     self.children[0].opacity = 0

    # def display_tooltip(self, *args):
    #     self.children[0].opacity = 1  


class FocusableCheckBox(FocusBehavior, CheckBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # METTRE ICI LES BONNES COULEURS

    def on_focus(self, instance, value, *args):
        if value:
            print("focus")
            # METTRE ICI LES BONNES COULEURS
        else:
            print("not focus")
            # METTRE ICI LES BONNES COULEURS

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        key = keycode[-1]
        if key in ("spacebar", "enter"):
            self.active = not self.active
        return super(FocusableCheckBox, self).keyboard_on_key_down(window, keycode, text, modifiers)


###################
### Scrollviews ###
###################


def create_button_scrollview_simple(button_text, x_size, size_vertical, x_pos, y_pos):
    """
    Create a button for a simple vertical scrollview.
    """
    button = FocusableButton(
        text=button_text,
        size_hint=(x_size, None),
        height=size_vertical,
        pos_hint={"x":x_pos},
        y=y_pos,
        halign="center")
    return button

def create_checkbox_scrollview_simple(x_size, size_vertical, x_pos, y_pos, group=None):
    """
    Create a button for a simple vertical scrollview.
    """
    checkbox = FocusableCheckBox(
        size_hint=(x_size, None),
        height=size_vertical,
        pos_hint={"x":x_pos},
        y=y_pos,
        group=group)
    return checkbox

def create_label_scrollview_simple(label_text, x_size, size_vertical, x_pos, y_pos, bool_text_size=False):
    """
    Create a label for a simple vertical scrollview.
    """
    label = Label(
        text=label_text,
        color=color_label,
        size_hint=(x_size, None),
        height=size_vertical,
        pos_hint={"x":x_pos},
        y=y_pos)
    if bool_text_size:
        label.text_size = label.size
        label.halign = "left"
        label.valign = "center"
    return label

def create_text_input_scrollview_simple(input_text, x_size, size_vertical, x_pos, y_pos, placeholder="", write_tab=True, readonly=False, multiline=True):
    """
    Create a text input for a simple scrollview.
    """
    text_input = TextInput(
        text=input_text,
        size_hint=(x_size, None),
        height=size_vertical,
        pos_hint={"x":x_pos},
        y=y_pos,
        selection_color=highlight_text_color,
        multiline=multiline,
        hint_text=placeholder,
        write_tab=write_tab,
        readonly=readonly)
    return text_input

def create_progress_bar_scrollview_simple(max_value, value, x_size, size_vertical, x_pos, y_pos):
    """
    Create a progress bar for a simple scrollview.
    """
    progress_bar = ProgressBar(
        max=max_value,
        value=value,
        pos_hint={"x":x_pos},
        size_hint=(x_size, None),
        y=y_pos,
        height=size_vertical
    )
    return progress_bar

def create_spinner_scrollview_simple(text, values, x_size, size_vertical, x_pos, y_pos):
    spinner = Spinner(
        text=text,
        values=values,
        pos_hint={"x":x_pos},
        size_hint=(x_size, None),
        y=y_pos,
        height=size_vertical
    )
    return spinner
