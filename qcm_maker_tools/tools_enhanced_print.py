"""
Module used to enhance the print and write functions of Python by adding colors and formatting.
"""


###############
### Imports ###
###############


### Python imports ###

from colorama import Fore


#################
### Constants ###
#################


PRINT_DEBUG = True
MODE_TEST = False
MODE_OPENAI = False


#######################
### Print functions ###
#######################


def print_error(*args, **kwargs):
    print("[" + Fore.RED + "Error      " + Fore.RESET + "] ", *args, **kwargs)

def print_warning(*args, **kwargs):
    print("[" + Fore.YELLOW + "Warning    " + Fore.RESET + "] ", *args, **kwargs)

def print_done(*args, **kwargs):
    print("[" + Fore.GREEN + "Done       " + Fore.RESET + "] ", *args, **kwargs)

def print_info(*args, **kwargs):
    print("[" + Fore.BLUE + "Information" + Fore.RESET + "] ", *args, **kwargs)

def print_result(*args, **kwargs):
    if "sep" not in kwargs:
        kwargs["sep"] = ""
    print("[" + Fore.CYAN + "Result     " + Fore.RESET + "]\n", *args,
          "\n[" + Fore.CYAN + "End        " + Fore.RESET + "]", **kwargs)

def print_start(*args, **kwargs):
    print("[" + Fore.GREEN + "Starting   " + Fore.RESET + "] ", *args, **kwargs)

def print_debug(*args, **kwargs):
    if PRINT_DEBUG:
        print("[" + Fore.LIGHTMAGENTA_EX +
              "Debug        " + Fore.RESET + "] ", *args, **kwargs)


#######################
### Write functions ###
#######################


def write_result(cur, text):
    cur.write("[" + Fore.CYAN + "Result     " + Fore.RESET + "]\n")
    cur.write(text)
    cur.write("\n[" + Fore.CYAN + "End        " + Fore.RESET + "]\n")

def write_start(cur, text):
    cur.write("[" + Fore.GREEN + "Starting   " + Fore.RESET + "] " + text + "\n")

def write_done(cur, text):
    cur.write("[" + Fore.GREEN + "Done       " + Fore.RESET + "] " + text + "\n")

def write_info(cur, text):
    cur.write("[" + Fore.BLUE + "Information" + Fore.RESET + "] " + text + "\n")

def write_warning(cur, text):
    cur.write("[" + Fore.YELLOW + "Warning    " + Fore.RESET + "] " + text + "\n")

def write_line(cur):
    cur.write("\n")
