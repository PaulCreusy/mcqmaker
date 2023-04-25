import sys

sys.path.append(".")

from qcm_maker_tools.tools import *

### Database functions ###

def get_list_database_folders(caracter_limit=CARACTER_LIMIT):
    """
    Return the list of the folders contained in the database.
    """
    folder_list = os.listdir(PATH_MAIN_DATABASE)
    cleaned_folder_list = filter_hidden_files(
        folder_list)
    return refactor_str_list_for_kivy(cleaned_folder_list, caracter_limit=caracter_limit)

def get_list_database_files(folder_name, caracter_limit=CARACTER_LIMIT, exclusion_list=[]):
    """
    Return the list of files contained in the specified folder of the database.
    """
    file_exclusion_list = [e[1] + ".txt" for e in exclusion_list]
    folder_name = clean_newlines(folder_name)
    database_files_list = os.listdir(PATH_MAIN_DATABASE + folder_name)
    cleaned_database_files_list = filter_hidden_files(
        database_files_list, ".txt")
    res = [e.replace(".txt", "")
           for e in cleaned_database_files_list if not e in file_exclusion_list]
    return refactor_str_list_for_kivy(res, caracter_limit=caracter_limit)

def get_database_tree():
    """
    Return the files and folders contained in the database as a tree.
    """
    tree = {}
    folders_list = get_list_database_folders(caracter_limit=NO_CARACTER_LIMIT)
    for folder in folders_list:
        files_list = get_list_database_files(
            folder, caracter_limit=NO_CARACTER_LIMIT)
        tree[folder] = files_list

    return tree

def load_database(database_name, database_folder):
    """
    Load the file of the database with the given name contained in the selected folder.

    Parameters
    ----------
    database_name : str
        Name of the database file.

    database_folder : str
        Name of the database folder.

    Returns
    -------
    list
        Content of the file under the specified form :
    [
        {
            "question": str,
            "options":
                [
                    "string1",
                    "string2"
                ],
            "answer": int
        }
    ]
    """

    # Clean the names
    database_folder = clean_newlines(database_folder)
    database_name = clean_newlines(database_name)

    # Build the path of the file
    path = PATH_MAIN_DATABASE + database_folder + "/" + database_name + ".txt"

    # Raise an error if the path does not exist
    if not os.path.exists(path):
        raise ValueError(
            f"Le fichier de questions {database_name} du dossier {database_folder} n'existe pas.")

    # Read the content of the file
    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    file_content = []
    error_list = []

    # Scan the lines to extract the content
    for line_id in range(len(lines)):

        # Extraction of the line
        line = lines[line_id]
        line = line.replace("\n", "")

        # Clean empty lines
        if line.replace(" ", "") == "":
            continue

        # Split question, solution and answers
        try:
            question_and_answers, solution = line.split(" @ ")
            question_and_answers = question_and_answers.split(" : ")
            question = question_and_answers[0]
            answers = question_and_answers[1:]
            if len(answers) == 0:
                raise ValueError
            solution = solution.replace(" ", "")
            solution_id = convert_letter_to_int(solution)
        except:
            # raise ValueError(
            #     f"Erreur détectée dans le fichier {database_name} du dossier {database_folder} à la ligne {line_id + 1}")
            error_list.append(line_id)
            solution_id = 0
            question = line
            answers = [""]

        line_dict = {}
        line_dict["question"] = question
        line_dict["answer"] = solution_id
        line_dict["options"] = answers

        file_content.append(line_dict)

    return file_content, error_list

def get_nb_questions(database_name, database_folder):
    """
    Return the number of questions contained in the specified file.

    Parameters
    ----------
    database_name : str
        Name of the database file.

    database_folder : str
        Name of the database folder.

    Returns
    -------
    int
        Number of questions of the file.
    """

    # Clean the names
    database_folder = clean_newlines(database_folder)
    database_name = clean_newlines(database_name)

    # Build the path of the file
    path = PATH_MAIN_DATABASE + database_folder + "/" + database_name + ".txt"

    # Raise an error if the path does not exist
    if not os.path.exists(path):
        # raise ValueError(
        #     f"Le fichier de questions {database_name} du dossier {database_folder} n'existe pas.")
        return None

    # Read the content of the file
    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    nb_questions = 0

    for line_id in range(len(lines)):

        # Extraction of the line
        line = lines[line_id]
        line = line.replace("\n", "")

        # Check if line not empty
        if line.replace(" ", "") != "":
            nb_questions += 1

    return nb_questions

def save_database(database_name, database_folder, content):
    """
    Save the given content of a database inside the specified file.

    Parameters
    ----------
    database_name : str
        Name of the database.

    database_folder : str
        Name of the database folder.

    content : list
        Content of the database under the following form :
        [
            {
                "question": str,
                "options":
                    [
                        "string1",
                        "string2"
                    ],
                "answer": int
            }
        ]

    Returns
    -------
    None
    """

    # Clean the names
    database_folder = clean_newlines(database_folder)
    database_name = clean_newlines(database_name)

    # Build the path of the file
    path = PATH_MAIN_DATABASE + database_folder + "/" + database_name + ".txt"
    folder_path = PATH_MAIN_DATABASE + database_folder

    # Check if the folder exists
    if not os.path.exists(folder_path):
        raise ValueError(
            f"Le dossier {database_folder} n'existe pas dans la base de données.")

    # Write the content inside the file
    with open(path, "w", encoding="utf-8") as file:
        for i in range(len(content)):
            current_dict = content[i]
            question = current_dict["question"]
            options = current_dict["options"]
            answer = current_dict["answer"]
            answer_str = convert_int_to_letter(answer)
            file.write(question)
            for option in options:
                file.write(" : " + option)
            file.write(" @ " + answer_str + "\n")

def create_database_folder(folder_name):
    """
    Create a new folder in the database with the given name.

    Parameters
    ----------
    folder_name : str
        Name of the folder to create.
    """
    folder_name = clean_newlines(folder_name)
    new_folder_path = PATH_MAIN_DATABASE + folder_name
    os.mkdir(new_folder_path)
