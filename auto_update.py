"""Auto update script for MCQMaker
"""

# Imports
import os
import sys
import shutil
import platform
import json
import toml
import urllib3
import zipfile
from tkinter.messagebox import showerror, showinfo, askyesno

# Extract the name of the os
os_name = platform.system()

if os_name == "Darwin":
    DIR_PATH = os.path.sep.join(sys.argv[0].split(os.path.sep)[:-1]) + "/"
    print(DIR_PATH)
else:
    DIR_PATH = "./"

# Path of the settings
PATH_SETTINGS = DIR_PATH + "data/settings.json"

# Path of the language folder
PATH_LANGUAGE_FOLDER = DIR_PATH + "resources/languages/"

# Path of the version file
PATH_VERSION_FILE = DIR_PATH + "version.toml"

# Temporary zip folder path
PATH_TEMP_ZIP = DIR_PATH + "new_version.zip"

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

# Start a popup to ask confirmation of the user
continue_update = askyesno(title=LANGUAGE_DICT["confirm_update"][0],
                           message=LANGUAGE_DICT["confirm_update"][1])

if continue_update is not True:
    sys.exit()

# Check if the os is supported for auto update
if os_name not in ("Windows", "Darwin", "Linux"):
    showerror(title=LANGUAGE_DICT["error_os_not_supported"][0],
              message=LANGUAGE_DICT["error_os_not_supported"][1])
    sys.exit()

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
    sys.exit()

# Get the latest zip file corresponding to the os
if os_name == "Windows":
    download_url = toml_version_data["windows_download_link"]
elif os_name == "Darwin":
    download_url = toml_version_data["mac_download_link"]
elif os_name == "Linux":
    download_url = toml_version_data["mac_download_link"]


# Download the file
http = urllib3.PoolManager()
response = http.request("GET", download_url, preload_content=False)
# with open(PATH_TEMP_ZIP, 'wb') as file:
#     shutil.copyfileobj(response, file)
with open(PATH_TEMP_ZIP, 'wb') as f:
    while True:
        chunk = response.read(1024)
        if not chunk:
            break
        f.write(chunk)

# Unzip the folder
with zipfile.ZipFile(PATH_TEMP_ZIP, "r") as zip:
    zip.extractall(DIR_PATH + "temp")

# Delete the zip file
os.remove(PATH_TEMP_ZIP)

# Define the folder and executable path
if os_name == "Windows":
    FOLDER_PATH = DIR_PATH + "temp/MCQMaker_Windows/"
    EXEC_NAME = "MCQMaker.exe"
elif os_name == "Darwin":
    FOLDER_PATH = DIR_PATH + "temp/MCQMaker_MacOS/"
    EXEC_NAME = "MCQMaker"
elif os_name == "Linux":
    FOLDER_PATH = DIR_PATH + "temp/MCQMaker_Linux/"
    EXEC_NAME = "MCQMaker"

# Remove the old resources folder
shutil.rmtree(DIR_PATH + "resources")

# Move the new resources folder
shutil.move(FOLDER_PATH + "resources", DIR_PATH + "resources")

# Remove the old executable file
os.remove(EXEC_NAME)

# Move the new executable file
shutil.move(FOLDER_PATH + EXEC_NAME, EXEC_NAME)

# Remove the temp directory
shutil.rmtree(DIR_PATH + "temp")

# Display the final popup
showinfo(title=LANGUAGE_DICT["update_completed"][0],
         message=LANGUAGE_DICT["update_completed"][1])
