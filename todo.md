# To do list

## General

- [x] add a notice file
- [ ] create the executable in the *zip* file
- [ ] take the pictures in English for the instruction_manual
- [ ] german version of the instruction manual
- [ ] correct the small problems in German with the `\n`

## Backend

- [x] add the docx export
- [x] save the exports in a subfolder of Exports (with the name config_name + class_name)
- [x] change text export
- [x] add error message for isolated :
- [x] set the progress bar evolution

## Kivy interface

### Main menu

- [x] add the logo
- [x] add the popup for credits

### QCM

- [x] create the top bar to add widgets
- [x] remake the scroll view and widden the labels for the folders and the files
- [x] exclude the file which has already been used in the scroll view
- [x] put a condition to scroll to if there are not enough items
- [x] delete the databases where there is no questions
- [ ] put a popup warning the user that some questions have been deleted
- [x] mix_all => mix_inside
- [x] store data in class available only if there is a class selected
- [x] put a warning popup with a yes/no choice when the user wants to create (not save after edit) a configuration whose name is already taken
- [x] put the popup with the format of exports
- [x] forbid to put negative numbers in the number of questions
- [x] correct the bug when there is no scroll view layout and that the extraction is launched with a error popup and exception

### Database

- [x] add a delete button for each question
- [x] set an id to all questions
- [x] forbid the creation of the folder whose name is already taken

### Classes

- [x] verify that all files of the database are displayed (and not only those who have already been used)
- [x] send None to Paul when there is no class selected

### Style 

- [x] progress bar style
- [x] popup style
- [x] add tooltips for the needed buttons (left right)
- [x] implement the other language
- [x] init screen for all focusable buttons to set their on_release function
- [x] upscale the logo
- [x] change the icon of the main window
- [x] add a scrollbar for the scroll views
- [x] add the class of labelled checkbox
- [x] integrate the general class of the scroll view layout
- [x] change disable style for checkbox

## Documentation

- [ ] complete the readme
- [x] complete the user guide

## Bug fix

- [x] fix bug reset screen in Thread, change to schedule in qcm creation