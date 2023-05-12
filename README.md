# QCM Maker

*This is a temporary version of the Readme.*
*More details about the utilisation of the software can be found in the folder `Instructions`*

## Table of content

- [QCM Maker](#qcm-maker)
  - [Table of content](#table-of-content)
  - [Introduction](#introduction)
  - [Architecture of the project](#architecture-of-the-project)
  - [Installation](#installation)
    - [Creation of a virtual environnement](#creation-of-a-virtual-environnement)
    - [Installation of the necessary packages](#installation-of-the-necessary-packages)
  - [Utilisation](#utilisation)
  - [Development](#development)
    - [Data structures](#data-structures)


## Introduction

The project is a tool to generate automatically MCQs, in `txt`, `docx`, `xml` and `h5p` formats.

## Architecture of the project

The project is divided into several packages:
- `Classes`
- `data`, containing the file `settings.json` where the language of the interface is specified as well as the default template. It also contains the *json* files to get the translation of the whole interface in several languages. You may add other files, if you want to translate the interface in another language.
- `data_kivy`, containing the styling files of the interface, using the *Python* graphic librairy *Kivy*.
- `Question Database`
- `resources`
- `Templates`, containing the templates you want to use for the generation in `docx` format.
- `test`

It also contains the following modules:
- `MCQMaker.kv`, *Kivy* file containing the graphics of the interface, which is linked to the module `MCQMaker.py`.
- `MCQMaker.py`


## Installation

### Creation of a virtual environnement

If you choose to clone this repository, you might want to use a virtual environnement.

You can create one with the following command :

```bash
python -m virtualenv mcqmaker_venv
```

To start it, use the command on *Windows* : 

```bash
mcqmaker_venv\Scripts\Activate.ps1
```

Or for *MacOS* and *Linux* :

```bash
mcqmaker_venv\Scripts\activate
```

### Installation of the necessary packages

To use this software, you need several *Python* libraries specified in the `requirements.txt` file.

To install them, use the command :

```
pip install -r requirements.txt
```

## Utilisation

The use of this software is detailed in the files contained in the folder `Instructions`; the instructions manual has been translated in several languages.

## Development

### Data structures

```python
content = [
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

config = {
    "QCM_name": str,
    "questions":
        [
            {"folder_name": str, "file_name": str, "nb_questions": int},
        ],
    "template": str,
    "mix_all_questions": bool,
    "mix_among_databases": bool
}

class_data = [
    {"name_folder": str, "name_file": str,
        "used_questions": int, "total_questions": int, "list_questions_used": list}
]

QCM_data = {
    "QCM_name": str,
    "questions": [
        {"question": str, "options": list, "answer": int}
    ]
}
```