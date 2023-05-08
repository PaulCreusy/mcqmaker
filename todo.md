# To do list

## Backend

- [x] add a notice file
- [ ] add the docx export
- [ ] correct the problem with the ids of the questions in the class
- [ ] save the exports in a subfolder of Exports (with the name config_name + class_name)
- [ ] change export h5P, text format
- [ ] add error message for : isolated

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
- [ ] Mélanger toutes les questions => mélanger par parties non ? Et du coup, je devrais cocher mélanger par parties à chaque fois que mélanger toutes les questions est coché non ? OUI
- [ ] Et pour Stocker les données dans la classe, il ne faudrait pas que la case soit cochable ou cochée s'il n'y a pas de classe sélectionnée non ? OUI
- [ ] Oh et un autre truc qu'on n'a pas fait dans MCQMaker, c'est si une configuration a déjà le nom précisé par l'utilisateur, on lui met un message d'erreur ? (le problème c'est que moi je n'ai pas accès aux noms des configs qui existent déjà, du coup il faudrait que tu me les donnes. Ok, tu vas me détester encore 😅 mais j'écris le manuel d'utilisation pour me faire pardonner 😘) Ou du moins un message de warning car ça peut être voulu (édition d'une config déjà sauvegardée) et on ne mettrait ce message que quand il n'a pas chargé de config pour éviter de tout le temps le souler (là dans ce cas, c'est vraiment qu'il crée une config du même nom qu'une existante, et pas quand il l'édite) => OUI AVEC UN WARNING
- [ ] mettre la popup avec le choix des formats pour l'export CAR C'EST MIEUX COMME CA !!!!!!!!!! (quoi que tu puisses en dire)

### Database

- [x] add a delete button for each question
- [x] set an id to all questions
- [x] forbid the creation of the folder whose name is already taken

### Classes

- [x] verify that all files of the database are displayed (and not only those who have already been used)
- [x] renvoyer None à Paul quand il n'y a pas de classe sélectionnée

### Style 

- [x] progress bar style
- [x] popup style
- [x] add tooltips for the needed buttons (left right)
- [x] verify that there is no problem in the qcm menu with the " : " for English
- [x] implement the other language
- [x] init screen for all focusable buttons to set their on_release function
- [x] upscale the logo
- [x] change the icon of the main window
- [x] Ajouter une scrollbar parce que c'est leeeeeennnnnnnnntt > merci mon chéri <3

### Pour ta Maman <3

- [ ] enlever le spinner pour les templates (et du coup enlever à chaque fois qu'on l'appelle)

### Pour ma Maman <3

- [ ] faire en sorte qu'il puisse y avoir plusieurs bonnes réponses (du coup ça change pas mal de choses dans la vérification)