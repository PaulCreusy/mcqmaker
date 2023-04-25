# MCQMaker

Version 4.0.0

## Installation

TU VOULAIS METTRE QUOI D'AUTRE ICI ?

Le programme peut être exécuté par la commande suivante :
```bash
python MCQMaker.py
```
Le raccourci `CTRL`+`F5` sur *VSCode* en étant dans le fichier `MCQMaker.py` peut également être utilisé pour lancer le programme.

## Utilisation

*MCQMaker* est composé de quatre menus principaux dont l'objectif détaillé est expliqué ci-dessous :
- un menu général se lançant au démarrage de l'application
- un menu de génération de QCM
- un menu de création et d'édition de bases de données
- un menu de modification des classes

![](ressources/images_readme/main_menu_french.png)

### Menu de génération de QCM

Ce menu permet de générer des QCM dans plusieurs formats différents, `txt`, `docx`, `h5p` et `xml`, à partir de configurations créées dans ce menu.

![](ressources/images_readme/mcq_menu_french.png)

#### Création d'une configuration

Afin de créer une configuration, l'utilisateur doit sélectionner un fichier de la base de données, à l'aide du menu du haut à droite. Après choisi le dossier et le fichier souhaité, l'utilisateur a la possibilité de rentrer le nombre de questions de ce fichier qu'il souhaite dans son QCM. Le nombre de questions disponibles dans le fichier est indiqué à droite de la zone de texte. Il doit ensuite ajouter la base de données en cliquant sur le bouton `+`. Ce nouveau fichier sera donc affiché dans la liste défilante juste en dessous et l'utilisateur aura la possibilité par la suite de modifier le nombre de questions des fichiers déjà choisis.

!!! tip Nombre de questions
    Le nombre total de questions contenues dans la configuration est affiché sur le menu de gauche. 


Avant de la sauvegarder, l'utilisateur doit spécifier son nom dans la zone de texte correspondante. Après l'avoir sauvegardée, il pourra la charger ultérieurement à l'aide du bouton `Charger une configuration`.

!!! info Sélection d'une classe
    Si l'utilisateur choisit d'utiliser une classe, en vue d'une génération de QCM, il est possible que le nombre total de questions disponibles dans certains fichiers, qui auraient déjà été utilisés par cette classe dans une génération de QCM précédente, soit différent. En cas de dépassement du nombre de questions disponibles, le nombre de questions sélectionnées sera modifié automatiquement pour être égal au maximum.

#### Génération d'un QCM

La génération du QCM est lancée à partir du bouton `Générer le QCM` une fois qu'une configuration a été choisie ou créée.

**Choix de la configuration**
Afin de choisir une configuration, l'utilisateur doit cliquer sur le bouton `Charger une configuration` où il aura la possibilité d'en créer une nouvelle ou d'en charger une déjà existante. Le nom de la configuration sélectionnée sera celui utilisé en tant que nom du QCM.

!!! note Création d'une nouvelle configuration
    Il n'est pas du tout nécessaire de passer par ce bouton pour créer une nouvelle configuration. L'utilisateur peut tout simplement sélectionner des fichiers et entrer un nom de configuration.

**Choix de la classe**
L'utilisateur a la possibilité de choisir une classe avant de procéder à la génération du QCM. Cela limitera les questions choisies lors de la génération du QCM en ne prenant pas celles qui ont déjà été utilisées par cette classe. De plus, si l'utilisateur le souhaite, les questions qui seront utilisées pour cette génération de QCM peuvent être sauvegardées dans la classe, afin qu'elles ne soient pas à nouveau utilisées dans un QCM suivant.

**Choix du template**
Afin de permettre la génération en `docx`, l'utilisateur doit sélectionner le template Word qu'il souhaite utiliser. Un template par défaut a été fourni, mais il est tout à fait possible pour l'utilisateur de le modifier, en particulier son style, tant que les conventions suivantes sont conservées :
- pour afficher le titre du QCM, si l'utilisateur souhaite le spécifier, la syntaxe `{NAME_MCQ}` doit être utilisée.
- pour afficher la liste des questions, les indicateurs `### LIST_QUESTIONS_START ###`, pour indiquer le début de cette liste, et `### LIST_QUESTIONS_END ###`, pour indiquer sa fin, doivent être présents.
- pour chaque question, les conventions suivantes sont utilisées :
  - `{ID_QUESTION}` pour afficher le numéro de la question
  - `{QUESTION}` pour afficher la question
  - `{LIST_OPTIONS}` pour afficher toutes les options

**Options supplémentaires**
L'utilisateur a également la possibilité de personnaliser le QCM créé notamment à l'aide des trois cases à cocher :
- `Mélanger par parties` permet de mélanger les questions au sein d'un même fichier de la base de données.
- `Mélanger toutes les questions` permet de mélanger toutes les questions du QCM, que ce soit au sein d'un même fichier de la base de données ou entre ces fichiers.
- `Stocker les données dans la classe` permet d'enregistrer dans la classe sélectionnée les questions sélectionnées pour cette génération, ce qui permet d'éviter des doublons avec le prochain QCM.

**Sauvegarde du QCM**
METTRE ICI LES DIFFERENTS FORMATS SI ON FAIT CA (METTRE LA CAPTURE D'ECRAN DE LA POPUP SI ON LA FAIT)
Le QCM généré, sous ses différents formats, est sauvegardé dans le dossier `Export` : un dossier contenant tous les formats souhaités aura alors été créé, ayant pour nom celui de la configuration joint à celui de la classe sélectionnée.

!!! warning Sauvegarde des QCM
    Il est vivement conseillé à l'utilisateur de ne pas laisser tous ses QCM dans le dossier d'export et de les sauvegarder ailleurs, car dès qu'une autre génération de QCM avec la même configuration et la même classe aura lieu, le QCM précédemment généré sera effacé au profit du nouveau.

### Menu d'édition de bases de données

Ce menu permet de créer de nouveaux fichiers dans la base de données et d'éditer les fichiers déjà existantes.

**Création d'un dossier**
L'utilisateur peut créer un dossier dans la base de données à partir de ce menu, en sélectionnant sur la première liste déroulante de choix `Nouveau` ; il pourra ensuite rentrer le nom de ce nouveau dossier dans la zone de texte correspondante, puis cliquer sur le bouton de création.

**Création d'un fichier**
L'utilisateur peut créer un fichier dans un dossier de la base de données à partir de ce menu ; pour cela, il peut sélectionner le nom du dossier souhaité, puis sélectionner `Nouveau`. Il peut ensuite spécifier le nom de ce nouveau fichier, qui ne soit pas un nom déjà pris par un fichier de ce même dossier, puis le sauvegarder avant ou après avoir inséré quelques questions dans la base de données à partir du menu du bas. Cette fonctionnalité est détaillée juste ensuite.

**Édition d'un fichier**
L'utilisateur peut éditer un fichier, que ce soit un nouveau ou un précédemment sauvegardé à l'aide de la partie inférieure de l'écran. Chaque question est affichée dans cette partie, en étant affectée à un numéro, et les choix de réponses possibles sont affichés en dessous, chacun associé à une case à cocher signifiant qu'il s'agit de la bonne réponse. L'utilisateur peut ajouter une option en cliquant sur le bouton `+` situé à la fin de la liste d'options déjà existantes.
L'utilisateur peut également supprimer une question en cliquant sur le bouton `-` situé à la fin de chaque question. 
L'utilisateur peut finalement rajouter une question en cliqyant sur le bouton `+` situé en bas de l'écran.

!!! info Numéro de la question
    Le numéro de la question est totalement arbitraire, il sert simplement à l'utilisateur de se repérer dans le fichier, notamment lors de la sauvegarde des questions si des erreurs sont détectées, mais il n'a aucune importance pour la génération du QCM.

!!! tip Suppression d'option
    Une option peut être supprimée en effaçant simplement son contenu dans la zone de texte ; la sauvegarde ne la prendra pas en compte.

!!! tip Navigation facile
    Pour faciliter l'édition de fichier dans ce menu, l'utilisateur peut naviguer entre les zones de textes, cases à cocher et boutons en appuyant sur `TAB`. La zone sélectionnée sera affichée en rose afin de permettre à l'utilisateur de se repérer. De plus, une fois sur une case à cocher ou sur un bouton, l'utilisateur pourra appuyer sur `ENTRÉE` afin de respectivement cocher ou décocher la case, ou déclencher la fonction liée au bouton.

**Détection des erreurs**
Lors de la sauvegarde d'un fichier, plusieurs vérifications sont effectuées sur le contenu rentré par l'utilisateur :
- tout d'abord, une question où rien n'a été entré dans la zone de texte intitulée "question" ne sera pas prise en compte, et donc non sauvegardée, même si des informations sont contenues dans les champs d'options.
- ensuite, un message d'erreur apparaîtra si aucune bonne réponse n'a été sélectionnée, interrompant la sauvegarde de la totalité de la base de données. L'utilisateur devra sélectionner une bonne réponse dans la question considérée puis sauvegarder à nouveau le fichier.
- finalement, une option vide ne sera pas considérée et donc non sauvegardée. S'il se trouvait qu'il s'agissait de l'unique bonne réponse à la question, le même message d'erreur que précédemment sera affiché.

!!! warning Sauvegarde du fichier en cours d'édition
    Si l'utilisateur change de fichier ou de dossier sans avoir sauvegardé au préalable le fichier qu'il était en train d'éditer, ses modifications seront perdues.

### Menu de modification des classes

Ce menu permet de gérer les classes qui seront utilisables dans le menu de génération de QCM. 

![](ressources/images_readme/class_menu_french.png)

**Classes existantes**
La partie en haut à gauche du menu permet à l'utilisateur de sélectionner une classe déjà existante. Le contenu de la classe sélectionnée sera affichée dans la partie inférieure de la fenêtre, où pour chaque fichier de la base de données, le ratio du nombre de questions utilisées par rapport au nombre total de questions sera affiché. L'utilisateur permet réinitialiser les données de cette classe en cliquant sur le bouton approprié : cela signifie que toutes les questions de tous les fichiers de la base de données seront de nouveau accessibles à la classe.

!!! warning Réinitialisation des données
    Réinitiliser les données d'une classe est une action irréversible.

**Création de classe**
La partie de droite de ce menu permet de créer une nouvelle classe, après que l'utilisateur a spécifié son nom dans la zone de texte correspondante. L'utilisateur ne pourra pas créer une classe ayant le même nom qu'une classe déjà existante.

## Première utilisation

Pour une première utilisation, il est tout d'abord conseillé à l'utilisateur de créer une base de données à partir du deuxième menu. Pour plus d'informations à ce propos, l'utilisateur peut se référer à [cette section](#menu-dédition-de-bases-de-données).

S'il souhaite fonctionner avec le principe de classes (qui permettent de mémoriser les questions déjà utilisées pour la génération d'un QCM afin d'éviter les redondances entre différents QCM), l'utilisateur peut se rendre de le troisième menu. Il peut y créer sa classe à l'aide de la partie droite du menu, comme expliqué dans [cette section](#menu-de-modification-des-classes).

Il peut ensuite procéder à la génération du QCM en se rendant dans le premier menu, dont l'utilisation est expliqué dans [cette section](#menu-de-génération-de-qcm).

## Crédits

Ce logiciel a été développé par Paul Creusy, pour la partie *backend*, et Agathe Plu pour la partie *frontend*. 
Les auteurs remercient leurs Mamans pour leur avoir demandé ce projet et l'avoir testé. 
ça te va ? ;) (dans tous les cas pour le readme sur le github, on changera ça pour mettre LUPA non ?)

## Licence

A COMPLETER