"""Auto update script for MCQMaker
"""

# Imports
import os
import platform
import requests
import json
import toml
from tkinter.messagebox import showerror, showinfo, askyesno

# Path of the settings
PATH_SETTINGS = "./data/settings.json"

# Path of the language folder
PATH_LANGUAGE_FOLDER = "./resources/languages/"

# Url of the version file on github
VERSION_FILE_URL = ""

# Load the settings to extract the language
with open(PATH_SETTINGS, "r", encoding="utf-8") as file:
    SETTINGS = json.load(file)

# Extract the language used
CURRENT_LANGUAGE = SETTINGS["language"]

# Load the language dict
with open(PATH_LANGUAGE_FOLDER + CURRENT_LANGUAGE + ".json", "r", encoding="utf-8") as file:
    LANGUAGE_DICT = json.load(file)["auto_update"]

# Load the file containg the actual version number
with open("version.toml", "r", encoding="utf-8") as file:
    actual_version = toml.load(file)["version"]

# Extract the name of the os
os_name = platform.system()

# Start a popup to ask confirmation of the user
askyesno(title=LANGUAGE_DICT["confirm_update"][0],
         message=LANGUAGE_DICT["confirm_update"][1])

# Download the corresponding files depending on the os
if os_name == "Windows" or os_name == "Darwin":
    pass
else:
    showerror(title=LANGUAGE_DICT["error_os_not_supported"][0],
              message=LANGUAGE_DICT["error_os_not_supported"][1])
