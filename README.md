# QCM Maker

## Introduction

The project is a tool to generate automatically MCQs, in *txt* and *docx* formats, given templates provided by the user. 

## Architecture of the project

The project is divided into several packages:
- `data`, containing the file `settings.json` where the language of the interface is specified as well as the default template. It also contains two *json* files, `english.json` and `french.json`, containing the translation of the whole interface in both languages. The user may add other files, if he wants to translate the interface in another language.
- `data_kivy`, containing the styling files of the interface, using the *Python* graphic librairy *Kivy*.
- `Database`
- `module`

It also contains the following modules:
- `qcm_maker.kv`, *Kivy* file containing the graphics of the interface, which is linked to the module `qcm_maker.py`.
- `qcm_maker.py`


## Installation

## Utilisation

After having executed the module `qcm_maker.py`, the following window is displayed METTRE IMAGE. The user may then choose between three menus, thanks to the three buttons on the top of the screen:
- `Create a MCQ`
- `Edit the database`
- `Modify classes`

### Create a MCQ

The main goal of this window is to generate a MCQ in *txt* and *docx* format 

### Edit the database

### Modify classes

In this menu, the user may handle the data of each class and create new ones.

On the left part, the user may select a class among those contained in the folder IL Y A UN FOLDER? 
The button `Reset data of the class` allows the user to reset the questions used by a class, after having selected it. It means, that for a future MCQ generation, the corresponding class will have access the questions of the whole database.

After having selected a class, the number of left questions for each file of the database is displayed in the scroll view on the bottom of the screen.

For the creation of a new class, the user may enter its name and click on the button `Create the new class`.