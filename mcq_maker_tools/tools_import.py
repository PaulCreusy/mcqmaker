"""
Module tools for the import functions of QCMMaker
"""

###############
### Imports ###
###############

### Library imports ###

import PyPDF2
from docx import Document

### Module imports ###

from mcq_maker_tools.tools import (
    convert_letter_to_int,
    remove_begin_and_end_spaces,
    remove_begin_and_end_char,
    replace_chars_with,
    compute_standard_deviation,
    get_min_idx,
    get_max_idx
)

#################
### Constants ###
#################

DETECTED_SPECIAL_CHARS = ["/", ".", ":", ")", "|", "@"]
DETECTED_SPECIAL_CHARS_SOL = ["/", ":", "|", "@"]
CHAR_TO_REMOVE = ["•"]
NUMBERS_LIST = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

#################
### Functions ###
#################

### Open functions ###


def open_pdf(filepath: str) -> str:
    """
    Open a PDF file and return its content as a string.

    Parameters
    ----------
    filepath : str
        Path of the pdf to open.

    Returns
    -------
    str : Text contained in the pdf.
    """

    # Open the pdf file
    pdf = open(filepath, "rb")

    # Extract the text page by page
    pdfread = PyPDF2.PdfReader(pdf)
    res = ""
    for x in range(len(pdfread.pages)):
        pageobj = pdfread.pages[x]
        text = pageobj.extract_text()
        res += text

    # Close the pdf file
    pdf.close()

    # Clean unwanted characters
    res = replace_chars_with(res, char_list=CHAR_TO_REMOVE, replacer="")

    return res


def open_docx(filepath: str) -> str:
    """
    Open a word file and return its content as a string.

    Parameters
    ----------
    filepath : str
        Path of the word to open.

    Returns
    -------
    str : Text contained in the word.
    """

    # Create the document
    document = Document(filepath)

    # Extract the text
    res = ""
    for paragraph in document.paragraphs:
        res += paragraph.text + "\n"

    return res


def open_file(filepath: str) -> str:
    """
    Open a file and return its content as a string.

    Parameters
    ----------
    filepath : str
        Path of the file to open.

    Returns
    -------
    str : Text contained in the file.
    """

    # Open the file
    file = open(filepath, "r")

    # Read the lines
    lines = file.readlines()

    # Close the file
    file.close()

    # Extract the text
    res = ""
    for line in lines:
        res += line

    return res

### Import functions ###


def import_old_format(lines: list, correct_answer_separator: str, question_answers_separator: str):
    """
    Load the file of the database with the given name contained in the selected folder.

    Parameters
    ----------
    raw_content : str
        Raw content of the file in a string.

    correct_answer_separator : str
        Separator used for the correct answer.

    question_answer_separator : str
        Separator used for question and answers.

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
            # TODO mettre "id": generated_id
        }
    ]
    """

    file_content = []
    error_list = []
    current_id = 0

    # Scan the lines to extract the content
    for line_id, line in enumerate(lines):

        # Clean empty lines
        if line.replace(" ", "") == "":
            continue

        # Split question, solution and answers
        try:
            # Separate question, answers and solution
            question_and_answers, solution = line.split(
                correct_answer_separator)
            question_and_answers = question_and_answers.split(
                question_answers_separator)
            question = question_and_answers[0]
            answers = question_and_answers[1:]

            # Raise error if no answer is detected
            if len(answers) == 0:
                raise ValueError

            # Clean the unwanted spaces
            question = remove_begin_and_end_spaces(question)
            answers = [remove_begin_and_end_spaces(
                answer) for answer in answers]
            solution = solution.replace(" ", "")

            # Convert the solution to obtain an id
            solution_id = convert_letter_to_int(solution)
        except:
            error_list.append(line_id)
            solution_id = 0
            question = line
            answers = [""]

        line_dict = {}
        line_dict["question"] = question
        line_dict["answer"] = solution_id
        line_dict["options"] = answers
        line_dict["id"] = current_id

        current_id += 1

        file_content.append(line_dict)

    return file_content, error_list

### Analysis functions ###


def convert_to_simple_repr(string: str):
    """Convert a string to a very simple representation to ease the analysis."""
    for i in range(97, 123):
        string = string.replace(chr(i), "a")
    for i in range(65, 91):
        string = string.replace(chr(i), "A")
    for i in range(48, 58):
        string = string.replace(chr(i), "1")
    return string


def remove_num(string: str):
    """Remove the numerotation inside a string."""
    string = remove_begin_and_end_spaces(string)
    for char in DETECTED_SPECIAL_CHARS:
        if char in string:
            str_split = string.split(char, 1)
            if len(str_split[0]) < 3:
                return remove_begin_and_end_spaces(str_split[1])
    return string


def analyse_num_type(num: str):
    """Analyse the type of numerotation present in a numerotation."""
    num = num.replace(" ", "")
    num_type_list = []
    for char in num:
        ord_char = ord(char)
        if 47 < ord_char < 58:
            num_type_list.append("number")
        elif 64 < ord_char < 91:
            num_type_list.append("upper")
        elif 96 < ord_char < 123:
            num_type_list.append("lower")
        else:
            return False

    for num_type in num_type_list:
        if num_type != num_type_list[0]:
            return False

    return num_type_list[0]


def get_num_type(string):
    """Get the type of numerotation present in a string."""
    string = remove_begin_and_end_spaces(string)
    for char in DETECTED_SPECIAL_CHARS:
        if char in string:
            str_split = string.split(char, 1)
            if len(str_split[0]) < 3:
                return analyse_num_type(str_split[0])
    return False


def search_answer_id_in_line(line: str):
    """Search for one single character matching the current numerotation."""
    line_simple_repr = convert_to_simple_repr(line)
    expected_borders = DETECTED_SPECIAL_CHARS + ["", " ", "\n"]
    for i in range(len(line)):
        if line[i - 1:i] in expected_borders and line[i + 1:i + 2] in expected_borders:
            if line_simple_repr[i] == "a":
                return convert_letter_to_int(
                    line[i].upper())
            if line_simple_repr[i] == "1":
                return int(line[i]) - 1
            if line_simple_repr[i] == "A":
                return convert_letter_to_int(
                    line[i])
    return None


def make_multiline_analyse(lines, has_solutions):
    """Treat the case where questions and options are split on several lines."""

    # Initialise the output
    res = []

    current_line_type = "question"
    current_question_id = -1
    number_type_answer = None

    for line in lines:

        # Remove spaces at the end and the beginning of the line
        line = remove_begin_and_end_spaces(line)

        if number_type_answer is None and current_line_type == "options":
            number_type_answer = get_num_type(line)

        if current_line_type == "options" and get_num_type(line) == number_type_answer:
            res[-1]["options"].append(remove_num(line))
        elif current_line_type == "question" or not has_solutions:
            # If the line is a question, add it to the dict
            line = remove_num(line)
            current_question_id += 1
            res.append({
                "question": line, "options": [], "answer": None, "id": current_question_id})
            current_line_type = "options"
        else:
            # In this case, it is a solution
            line = remove_begin_and_end_char(
                line, DETECTED_SPECIAL_CHARS + [" "])
            if line[-1] in NUMBERS_LIST:
                res[-1]["answer"] = int(
                    line[-1]) - 1
            else:
                res[-1]["answer"] = search_answer_id_in_line(line)
            current_line_type = "question"

    return res


def make_single_lines_with_num_analyse(lines):
    """Treat the single lines with num case"""

    # Determine the character used for numerotation
    char_used_dict = {}
    for line in lines:
        if remove_begin_and_end_char(line, [" ", "\n"]) == "":
            continue
        simple_line = replace_chars_with(line, DETECTED_SPECIAL_CHARS, "¤")
        simple_line = convert_to_simple_repr(simple_line)
        for i in range(len(line) - 3):
            if simple_line[i: i + 3] in (" A¤", " 1¤", " a¤"):
                char = line[i + 2]
                if char in char_used_dict:
                    char_used_dict[char] += 1
                else:
                    char_used_dict[char] = 1

    # Extract the best character
    max_count = 0
    best_char = ""
    for char in char_used_dict:
        count = char_used_dict[char]
        if count > max_count:
            best_char = char
            max_count = count

    res = []
    current_question_id = 0

    # Analyse line by line to extract the questions and answers
    for line in lines:
        prec_i = 0
        if remove_begin_and_end_char(line, [" ", "\n"]) == "":
            continue
        simple_line = replace_chars_with(line, DETECTED_SPECIAL_CHARS, "¤")
        simple_line = convert_to_simple_repr(simple_line)
        dict_line = {}
        for i in range(len(line) - 3):
            if simple_line[i: i + 3] in (" A¤", " 1¤", " a¤"):
                char = line[i + 2]
                if char == best_char:
                    chunk = line[prec_i:i]
                    chunk = remove_num(chunk)
                    chunk = remove_begin_and_end_spaces(chunk)

                    # If it is the question
                    if prec_i == 0:
                        dict_line["question"] = chunk
                        dict_line["options"] = []
                        dict_line["answer"] = None
                        dict_line["id"] = current_question_id
                    else:
                        dict_line["options"].append(chunk)
                    prec_i = i + 1
        chunk = line[prec_i:len(line)]
        chunk = remove_num(chunk)
        chunk = remove_begin_and_end_spaces(chunk)
        dict_line["options"].append(chunk)
        if dict_line != {}:
            res.append(dict_line)
            current_question_id += 1

    return res


def count_char_occurences_on_lines(lines, char_list):
    """"""
    history = []
    for line in lines:
        if remove_begin_and_end_char(line, [" ", "\n"]) == "":
            continue
        line_scan = []
        for char in char_list:
            line_scan.append(len(line.split(char)) - 1)
        history.append(line_scan)
    return history


def make_single_lines_with_sep_analyse(lines, has_solutions):
    """Treat the single lines with separators."""

    # Determine the character used for question and answer separation
    # Find characters with number of occurences between 2 and 10 each time
    # Score based on max mean, threshold std 0.5 and if no one, min std
    history = count_char_occurences_on_lines(lines, DETECTED_SPECIAL_CHARS)

    if len(history) == 0:
        return {}

    mean_list = [sum([history[j][i] for j in range(len(history))]) /
                 len(history[0]) for i in range(len(DETECTED_SPECIAL_CHARS))]
    std_list = [compute_standard_deviation([history[j][i] for j in range(len(history))])
                for i in range(len(DETECTED_SPECIAL_CHARS))]

    kept_list = [i for i in range(
        len(std_list)) if std_list[i] < 0.5 and mean_list[i] >= 1.5]

    if len(kept_list) > 0:
        best_idx = get_max_idx(mean_list, restriction=kept_list)
    else:
        kept_list = [i for i in range(
            len(std_list)) if mean_list[i] >= 1.5]
        if len(kept_list) == 0:
            return {}
        best_idx = get_min_idx(std_list, restriction=kept_list)

    best_char_options = DETECTED_SPECIAL_CHARS[best_idx]

    if has_solutions:
        # Determine the character used for answer and solution separation
        history = count_char_occurences_on_lines(
            lines, DETECTED_SPECIAL_CHARS_SOL)

        # Compute mean and standard deviation
        mean_list = [sum([history[j][i] for j in range(len(history))]) /
                     len(history[0]) for i in range(len(history[0]))]
        dist_list = [abs(1 - mean_list[i]) for i in range(len(mean_list))]

        # Keep the best result
        best_char_sol_id = get_min_idx(dist_list)
        best_char_sol = DETECTED_SPECIAL_CHARS_SOL[best_char_sol_id]
    else:
        best_char_sol = "###"

    # Launch the analyse with the old import function
    return import_old_format(lines,
                             correct_answer_separator=best_char_sol,
                             question_answers_separator=best_char_options)[0]


def analyse_content(raw_content: str, has_solutions=False):
    """
    Analyse the content of a file to extract the questions and answers.
    """

    # Remove tabulations
    raw_content = raw_content.replace("\t", " ")

    # Clean blank lines and spaces at the end and the beginning of the content
    raw_content = remove_begin_and_end_char(raw_content, [" ", "\n"])

    # Clean blank lines
    raw_content = raw_content.replace("\n\n", "\n")

    # Detect whether we have one question with its answers per line or not
    # Two types of single line, with separator or with numbers
    lines = raw_content.split("\n")
    nb_single_lines_with_sep_detected = 0
    nb_single_lines_with_num_detected = 0
    for line in lines:
        line = remove_begin_and_end_spaces(line)
        line = replace_chars_with(line, DETECTED_SPECIAL_CHARS, "¤")
        line = convert_to_simple_repr(line)
        if len(line.split(" A¤")) > 1 or len(line.split(" 1¤")) > 1 or len(line.split(" a¤")) > 1:
            nb_single_lines_with_num_detected += 1
        elif len(line.split(" ¤ ")) > 2:
            nb_single_lines_with_sep_detected += 1

    # Set the mode of reading
    nb_lines = len(lines)
    if nb_single_lines_with_num_detected > 0.8 * nb_lines:
        mode = "single_lines_with_num"
    elif nb_single_lines_with_sep_detected > 0.8 * nb_lines:
        mode = "single_lines_with_sep"
    else:
        mode = "multi_lines"

    # Add the info if solutions are provided
    if has_solutions:
        mode += "_with_sol"

    # Return because unknown format
    if mode == "single_lines_with_num_with_sol":
        return {}

    if "multi_lines" in mode:
        return make_multiline_analyse(lines, has_solutions)
    elif mode == "single_lines_with_num":
        return make_single_lines_with_num_analyse(lines)
    else:
        return make_single_lines_with_sep_analyse(lines, has_solutions)
