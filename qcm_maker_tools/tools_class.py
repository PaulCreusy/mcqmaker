
import sys

sys.path.append(".")

from qcm_maker_tools.tools_database import *


### Classes functions ###

def get_list_templates():
    """
    Return the list of names of the templates stored in the template folder.
    """
    template_files_list = os.listdir(PATH_TEMPLATE_FOLDER)
    cleaned_template_files_list = filter_hidden_files(
        template_files_list, ".docx")
    res = [e.replace(".docx", "") for e in cleaned_template_files_list]
    return res

def get_list_classes():
    """
    Return the list of names of the classes stored in the class folder.
    """
    classes_files_list = os.listdir(PATH_CLASS_FOLDER)
    cleaned_classes_files_list = filter_hidden_files(
        classes_files_list, ".txt")
    res = [e.replace(".txt", "") for e in cleaned_classes_files_list]
    return res

def load_class(class_name):
    """
    Return the content of the selected class.

    Parameters
    ----------
    class_name : str
        Name of the class to load.

    Returns
    -------
    dict
        Data of the class.
    """

    if class_name is None:
        return complete_and_filter_class_content({})

    class_name = clean_newlines(class_name)

    # Open the file
    file_path = PATH_CLASS_FOLDER + class_name + ".txt"
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Extract the content
    class_content = {}

    for i in range(len(lines)):

        # Read the line
        line = lines[i]
        line = line.replace("\n", "")
        if " : " not in line:
            continue

        # Extract the data
        database_path, questions = line.split(" : ")
        folder, file = database_path.split("/")
        file = file.replace(".txt", "")
        questions_list_str = questions.split(",")
        questions_list = [int(e) for e in questions_list_str]

        # Add the data to the content
        current_dict = {}
        current_dict["used_questions"] = len(questions_list)
        current_dict["total_questions"] = get_nb_questions(file, folder)
        current_dict["list_questions_used"] = questions_list
        class_content[(folder, file)] = current_dict

    return complete_and_filter_class_content(class_content)

def complete_and_filter_class_content(class_content: dict):
    """
    Complete the class content by adding all other files and delete the unexisting files.

    Parameters
    ----------
    class_content : dict
        Content of the class in a dictionnary with the keys (folder,file).

    Returns
    -------
    dict
        Filtered and completed content of the class.
    """

    # Extract the list of folders
    database_tree = get_database_tree()
    folders_list = database_tree.keys()

    # Scan the content to delete unexisting files
    for key in list(class_content.keys()):
        folder, file = key

        # Verify if folder exists
        if not folder in folders_list:
            class_content.pop((folder, file))
        else:
            files_list = database_tree[folder]

            # Verify if file exists
            if not file in files_list:
                class_content.pop((folder, file))

    # Add the missing files
    for folder in folders_list:
        files_list = database_tree[folder]
        for file in files_list:

            # If no info is in the content at the specified key, add a blank line
            if not (folder, file) in class_content:
                current_dict = {}
                current_dict["used_questions"] = 0
                current_dict["total_questions"] = get_nb_questions(
                    file, folder)
                current_dict["list_questions_used"] = []
                class_content[(folder, file)] = current_dict
    return class_content

def clean_class_content_from_empty_lines(class_content: dict):
    """
    Clean the data of the class to prepare saving by removing empty lines.
    """
    for key in list(class_content.keys()):
        current_dict = class_content[key]
        if "used_questions" in current_dict and current_dict["used_questions"] == 0:
            class_content.pop(key)
    return class_content

def save_class(class_name, class_data):
    """
    Save the given data in the selected class.

    Parameters
    ----------
    class_name : str
        Name of the class.

    class_data : list
        Data of the class.

    Returns
    -------
    None
    """

    class_data = clean_class_content_from_empty_lines(class_data)
    print(class_data)

    class_name = clean_newlines(class_name)

    # Build path of the class
    path = PATH_CLASS_FOLDER + class_name + ".txt"

    with open(path, "w", encoding="utf-8") as file:

        # Write the name of the class
        file.write(class_name + "\n")

        # Write the content of the used files one by one
        for key in class_data:
            current_dict = class_data[key]
            name_folder = key[0]
            name_file = key[1]
            file_path = name_folder + "/" + name_file + ".txt"
            list_questions_used = current_dict["list_questions_used"]
            file.write(file_path + " : " + str(list_questions_used)
                       [1:len(str(list_questions_used)) - 1] + "\n")

def reset_class(class_name):
    """
    Reset the data of the selected class

    Parameters
    ----------
    class_name : str
        Name of the selected class.

    Returns 
    -------
    None
    """
    save_class(class_name, {})