---
export_on_save:
    puppeteer: ["pdf"]
---
# MCQMaker

## Table of contents

- [MCQMaker](#mcqmaker)
  - [Table of contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Installation](#installation)
    - [Creation of a virtual environment](#creation-of-a-virtual-environment)
    - [Installation of the necessary packages](#installation-of-the-necessary-packages)
  - [Utilisation](#utilisation)
  - [Development](#development)
  - [Architecture of the project](#architecture-of-the-project)
    - [Data structures](#data-structures)


## Introduction

The project is a tool to generate automatically MCQs, in `txt`, `docx`, `xml` and `h5p` formats.

## Installation

### Creation of a virtual environment

If you choose to clone this repository, you might want to use a virtual environment.

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

## Architecture of the project

The project is divided into several packages:
- `Classes`, containing the `txt` files automatically generated by the software to store the data of each class.
- `coverage`
- `data`, containing the file `settings.json` where the language of the interface is specified as well as the default template and the codes caracters used for the database. It also contains the *json* files to get the translation of the whole interface in several languages. You may add other files, if you want to translate the interface in another language. It finally contains the folder `configuration` where all configurations created by the user in the application are stored.
- `Export`, corresponding to the folder where the exports of the MCQs are made, once generated.
- `Instructions`, containing the instructions manual into several languages.
- `qcm_maker_screens`, containing the *Python* modules for each *Kivy* screen. 
- `qcm_maker_tools`, containing the following *Python* tools modules:
  - `tools_class`, used to handle the interactions with classes
  - `tools_database`, used to handle the interactions with the database
  - `tools_docx`, used for the export in *docx*
  - `tools_enhanced_print`, containing several functions for colored printing
  - `tools_export`, used to handle the generation of the MCQs
  - `tools_kivy`, containing general tools classes for the librairy *Kivy*
  - `tools_scrollview`, containing the class to build scrollviews in *Kivy*
  - `tools`, containing general tool functions
- `Question Database`, where is stored the folders and the files of the database
- `resources`, containing the following folders:
  - `fill-in-the-blanks`
  - `images_documentation`, containing the images used in the instruction manuals and in the readme.
  - `kivy`, containing the styling files of the interface, using the *Python* graphic librairy *Kivy*.
  - `single-choice`
- `Templates`, containing the templates you want to use for the generation in `docx` format. By default, it contains only one template, explaining the conventions but you may add other to change style.
- `test`, containing test functions for the backend, mainly for the `tools` package.

It also contains the following files:
- `MCQMaker.kv`, *Kivy* file containing the graphics of the interface, which is linked to the module `MCQMaker.py`.
- `MCQMaker.py`, main module to launch to execute the code.
- `requirements.txt`

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