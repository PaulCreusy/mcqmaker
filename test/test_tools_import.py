"""
Test module of tools import
"""

###############
### Imports ###
###############

from mcq_maker_tools.tools import (
    remove_begin_and_end_char
)

from mcq_maker_tools.tools_import import (
    open_docx,
    open_file,
    open_pdf,
    import_old_format,
    convert_to_simple_repr,
    remove_num,
    analyse_num_type,
    get_num_type,
    make_multiline_analyse,
    make_single_lines_with_num_analyse,
    make_single_lines_with_sep_analyse,
    analyse_content
)

######################
### Test variables ###
######################

# Path of the folder with files for open tests
PATH_IMPORT_FOLDER = "test/data/Import/"

### Test variables for open functions ###

PATH_DOCX_FILE_1 = PATH_IMPORT_FOLDER + "test_1.docx"
PATH_PDF_FILE_1 = PATH_IMPORT_FOLDER + "test_1.pdf"
PATH_TXT_FILE_1 = PATH_IMPORT_FOLDER + "test_1.txt"
CONTENT_FILE_1 = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
Nullam eget erat a diam scelerisque tincidunt. 
Aliquam sit amet felis at ante fringilla aliquam eu vitae est. 
Mauris a orci lobortis, suscipit nulla vitae, convallis sem. 
Nullam tincidunt purus in velit sodales commodo. 
Aenean maximus massa vel velit pulvinar, eu ultrices massa vestibulum."""

PATH_DOCX_FILE_2 = PATH_IMPORT_FOLDER + "test_2.docx"
PATH_PDF_FILE_2 = PATH_IMPORT_FOLDER + "test_2.pdf"
PATH_TXT_FILE_2 = PATH_IMPORT_FOLDER + "test_2.txt"
CONTENT_FILE_2 = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris ultrices, nibh ut feugiat auctor, libero mi scelerisque lacus, id iaculis lorem leo non elit. Fusce a risus accumsan arcu vestibulum vehicula. Donec auctor varius arcu, blandit pulvinar est scelerisque varius. Curabitur ante purus, tempor molestie tellus id, imperdiet tempus nibh. Maecenas quam arcu, egestas a ex at, vestibulum placerat neque. Nulla dignissim, urna sed consequat consectetur, lectus sem sagittis leo, ut ornare eros sem sed tortor. Phasellus ac augue lorem. In ac mi tempor, egestas elit nec, consequat odio. Etiam tellus risus, rhoncus nec nunc ac, laoreet pretium est. Etiam placerat tincidunt ipsum eu dictum. Suspendisse vel efficitur elit. Praesent hendrerit lectus vel magna ornare, in rhoncus ipsum finibus. Proin eu nulla faucibus nunc dignissim facilisis. 

Sed a dui urna. Sed in luctus nisl, eget tincidunt quam. Quisque eget sapien eu neque efficitur iaculis at non nulla. Ut mollis arcu in ex vestibulum tincidunt. Proin mollis maximus dui et commodo. Aliquam a lorem in augue congue posuere. Vestibulum dui diam, cursus nec lectus nec, gravida finibus diam. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam nec feugiat ex. Nullam tempor quam et mauris placerat dictum."""
CONTENT_FILE_2_PDF = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris ultrices, nibh ut feugiat auctor, 
libero mi scelerisque lacus, id iaculis lorem leo non elit. Fusce a risus accumsan arcu vestibulum 
vehicula. Donec auctor varius arcu, blandit pulvinar est scelerisque varius. Curabitur ante purus, 
tempor molestie tellus id, imperdiet tempus nibh. Maecenas quam arcu, egestas a ex at, vestibulum 
placerat neque. Nulla dignissim, urna sed consequat consectetur, lectus sem sagittis leo, ut ornare 
eros sem sed tortor. Phasellus ac augue lorem. In ac mi tempor, egestas elit nec, consequat odio. 
Etiam tellus risus, rhoncus nec nunc ac, laoreet pretium est. Etiam placerat tincidunt ipsum eu 
dictum. Suspendisse vel efficitur elit. Praesent hendrerit lectus vel magna ornare, in rhoncus ipsum 
finibus. Proin eu nulla faucibus nunc dignissim facilisis. 
Sed a dui urna. Sed in luctus nisl, eget tincidunt quam. Quisque eget sapien eu neque efficitur 
iaculis at non nulla. Ut mollis arcu in ex vestibulum tincidunt. Proin mollis maximus dui et 
commodo. Aliquam a lorem in augue congue posuere. Vestibulum dui diam, cursus nec lectus nec, 
gravida finibus diam. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere 
cubilia curae; Etiam nec feugiat ex. Nullam tempor quam et mauris placerat dictum."""

### Test variables for convert and num functions ###

TEST_TEXT_1 = "My name is SamSam and I'm 5 years old."
TEST_TEXT_REPR_1 = "Aa aaaa aa AaaAaa aaa A'a 1 aaaaa aaa."

TEST_NUM_1 = "2. What region is Lille located in?"
TEST_NUM_REPR_1 = "1. Aaaa aaaaaa aa Aaaaa aaaaaaa aa?"
TEST_NUM_1_REM_NUM = "What region is Lille located in?"


TEST_NUM_2 = "3/ Which famous art museum can be found in Lille?"
TEST_NUM_2_REM_NUM = "Which famous art museum can be found in Lille?"

TEST_NUM_3 = "   a) Germany"
TEST_NUM_3_REM_NUM = "Germany"

NUM_TYPE_1 = "a"
NUM_TYPE_2 = "2"
NUM_TYPE_3 = "AB"
NUM_TYPE_4 = "1A"

### Test variables for import old format ###

PATH_OLD_IMPORT = PATH_IMPORT_FOLDER + "test_old_format.txt"

ANSWER_LIST = ["Reponse 1", "Reponse 2", "Reponse 3", "Reponse 4"]
OLD_IMPORT_FILE_CONTENT = [
    {
        "question": "Q_S1",
        "options": ANSWER_LIST,
        "answer": 0,
        "id": 0
    },
    {
        "question": "Q_S2",
        "options": ANSWER_LIST,
        "answer": 1,
        "id": 1
    },
    {
        "question": "Q_S3",
        "options": ANSWER_LIST,
        "answer": 2,
        "id": 2
    },
    {
        "question": "Q_S4",
        "options": ANSWER_LIST,
        "answer": 3,
        "id": 3
    }
]


#############
### Tests ###
#############

### Test open docx ###


def test_open_docx():
    assert remove_begin_and_end_char(open_docx(PATH_DOCX_FILE_1), [" ", "\n"]) \
        == CONTENT_FILE_1
    assert remove_begin_and_end_char(open_docx(PATH_DOCX_FILE_2), [" ", "\n"]) \
        == CONTENT_FILE_2


test_open_docx()

### Test open pdf ###


def test_open_pdf():
    assert remove_begin_and_end_char(open_pdf(PATH_PDF_FILE_1), [" ", "\n"]) \
        == CONTENT_FILE_1
    assert remove_begin_and_end_char(open_pdf(PATH_PDF_FILE_2), [" ", "\n"]) \
        == CONTENT_FILE_2_PDF


test_open_pdf()

### Test open file ###


def test_open_file():
    assert remove_begin_and_end_char(open_file(PATH_TXT_FILE_1), [" ", "\n"]) \
        == CONTENT_FILE_1
    assert remove_begin_and_end_char(open_file(PATH_TXT_FILE_2), [" ", "\n"]) \
        == CONTENT_FILE_2


test_open_file()

### Test convert to simple repr ###


def test_convert_to_simple_repr():
    assert convert_to_simple_repr(TEST_TEXT_1) == TEST_TEXT_REPR_1
    assert convert_to_simple_repr(TEST_NUM_1) == TEST_NUM_REPR_1


test_convert_to_simple_repr()

### Test remove num ###


def test_remove_num():
    assert remove_num(TEST_NUM_1) == TEST_NUM_1_REM_NUM
    assert remove_num(TEST_NUM_2) == TEST_NUM_2_REM_NUM
    assert remove_num(TEST_NUM_3) == TEST_NUM_3_REM_NUM


test_remove_num()

### Test analyse num type ###


def test_analyse_num_type():
    assert analyse_num_type(NUM_TYPE_1) == "lower"
    assert analyse_num_type(NUM_TYPE_2) == "number"
    assert analyse_num_type(NUM_TYPE_3) == "upper"
    assert analyse_num_type(NUM_TYPE_4) == False


test_analyse_num_type()

### Test get num type ###


def test_get_num_type():
    assert get_num_type(TEST_NUM_1) == "number"
    assert get_num_type(TEST_NUM_2) == "number"
    assert get_num_type(TEST_NUM_3) == "lower"


test_get_num_type()

### Test import old format ###


def test_import_old_format():
    assert import_old_format(open_file(PATH_OLD_IMPORT).split("\n"), correct_answer_separator="@", question_answers_separator=":")[0] \
        == OLD_IMPORT_FILE_CONTENT


test_import_old_format()
