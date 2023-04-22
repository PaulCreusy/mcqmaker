# QCMMaker

Version 4.0.0

## Installation

## Utilisation

## Crédits

## Licence

# QCMMaker

Version 4.0.0

## Installation

## Utilisation

*MCQMaker* est composé de quatre menus principaux dont l'objectif détaillé est expliqué ci-dessous :
- un menu général se lançant au démarrage de l'application METTRE PHOTO
- un menu de génération de QCM
- un menu de création et d'édition de bases de données
- un menu de modification des classes

### Menu de génération de QCM

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

!!! warning Attention quant à la sauvegarde
    Si l'utilisateur change de fichier ou de dossier avant d'avoir sauvegardé le fichier qu'il était en train d'éditer ses modifications seront perdues.

### Menu de modification des classes

Ce menu permet de gérer les classes qui seront utilisables dans le menu de génération de QCM. 
PHOTO

**Classes existantes**
La partie en haut à gauche du menu permet à l'utilisateur de sélectionner une classe déjà existante. Le contenu de la classe sélectionnée sera affichée dans la partie inférieure de la fenêtre, où pour chaque fichier de la base de données, le ratio du nombre de questions utilisées restantes par rapport au nombre total de question sera affiché. L'utilisateur permet réinitialiser les données de cette classe en cliquant sur le bouton approprié : cela signifie que toutes les questions de tous les fichiers de la base de données seront de nouveau accessibles à la classe.

!!! warning Attention quant à la réinitialisation des données
    Aucun retour en arrière n'est possible après avoir supprimé le contenu d'une classe.

**Création de classe**
La partie de droite de ce menu permet de créer une nouvelle classe, après que l'utilisateur ait spécifié son nom dans la zone de texte correspondante. L'utilisateur ne pourra pas créer de classe ayant le même nom qu'une classe déjà existante.

## Première utilisation

Pour une première utilisation, il est tout d'abord conseillé à l'utilisateur de créer une base de données à partir du deuxième menu. Pour plus d'informations à ce propos, l'utilisateur peut se référer à [cette section](#menu-dédition-de-bases-de-données).

S'il souhaite fonctionner avec le principe de classes (qui permettent de mémoriser les questions déjà utilisées pour la génération d'un QCM afin d'éviter les redondances entre différents QCM), l'utilisateur peut se rendre de le troisième menu. Il peut y créer sa classe à l'aide de la partie droite du menu, comme expliqué dans [cette section](#menu-de-modification-des-classes).

Il peut ensuite procéder à la génération du QCM en se rendant dans le premier menu, dont l'utilisation est expliqué dans [cette section](#menu-de-génération-de-qcm).

## Crédits

## Licence
