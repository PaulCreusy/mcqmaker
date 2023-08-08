"""Auto update script for MCQMaker
"""

# Imports
import os
import platform
import json
import toml
import urllib3
import shutil
import zipfile
from tkinter.messagebox import showerror, showinfo, askyesno

# Path of the settings
PATH_SETTINGS = "./data/settings.json"

# Path of the language folder
PATH_LANGUAGE_FOLDER = "./resources/languages/"

# Path of the version file
PATH_VERSION_FILE = "version.toml"

# Temporary zip folder path
PATH_TEMP_ZIP = "new_version.zip"

# Url of the version file on github
VERSION_FILE_URL = "https://raw.githubusercontent.com/PaulCreusy/mcqmaker/main/version.toml"

# Load the settings to extract the language
with open(PATH_SETTINGS, "r", encoding="utf-8") as file:
    SETTINGS = json.load(file)

# Extract the language used
CURRENT_LANGUAGE = SETTINGS["language"]

# Load the language dict
with open(PATH_LANGUAGE_FOLDER + CURRENT_LANGUAGE + ".json", "r", encoding="utf-8") as file:
    LANGUAGE_DICT = json.load(file)["auto_update"]

# Load the file containg the actual version number
with open(PATH_VERSION_FILE, "r", encoding="utf-8") as file:
    actual_version = toml.load(file)["version"]

# Extract the name of the os
os_name = platform.system()

# Start a popup to ask confirmation of the user
askyesno(title=LANGUAGE_DICT["confirm_update"][0],
         message=LANGUAGE_DICT["confirm_update"][1])

# Check if the os is supported for auto update
if os_name not in ("Windows", "Darwin"):
    showerror(title=LANGUAGE_DICT["error_os_not_supported"][0],
              message=LANGUAGE_DICT["error_os_not_supported"][1])
    exit()

# Download the up to date version file
http = urllib3.PoolManager()
response = http.request("GET", VERSION_FILE_URL, preload_content=False)
with open(PATH_VERSION_FILE, 'wb') as file:
    shutil.copyfileobj(response, file)

# Extract the latest version number
with open(PATH_VERSION_FILE, "r", encoding="utf-8") as file:
    toml_version_data = toml.load(file)
latest_version = toml_version_data["version"]

# Detect if the update is necessary
if actual_version == latest_version:
    showinfo(title=LANGUAGE_DICT["already_up_to_date"][0],
             message=LANGUAGE_DICT["already_up_to_date"][1])
    exit()

# Get the latest zip file corresponding to the os
if os_name == "Windows":
    download_url = toml_version_data["windows_download_link"]
elif os_name == "Darwin":
    download_url = toml_version_data["mac_download_link"]

# Download the file
http = urllib3.PoolManager()
response = http.request("GET", download_url, preload_content=False)
with open(PATH_TEMP_ZIP, 'wb') as file:
    shutil.copyfileobj(response, file)

# Unzip the folder
with zipfile.ZipFile(PATH_TEMP_ZIP, "r") as zip:
    zip.extractall()
