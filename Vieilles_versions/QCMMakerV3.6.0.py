# Version 3.6.0
# -*- coding: utf-8 -*-
import inspect
import os
from tkinter.scrolledtext import *
from tkinter.messagebox import *
import tkinter as tk
from random import *
import threading

version = "3.6.0"

# Format des questions dans les fichiers .txt situés dans le dossier "Banque de questions" voir ci dessous:
"""
Question 1 : Reponse A : Reponse B : Reponse C : Reponse D @ A
Question 2 : Reponse A : Reponse B @ B

"""
# Le fait que le nombre de réponse ne soit pas le même pour toutes les questions n'est pas problématique
# Attention, bien respecter les espaces de part et d'autre des deux points
# Attention, lorsque des questions sont ajoutées à la banque, elles doivent impérativement être mises à la fin du fichier .txt
# Attention, toujours laisser une ligne vide à la fin d'un fichier de questions


chemin = ""

chemin = inspect.getsourcefile(lambda: 0)
chemin = chemin.replace("\\", "/")
imax = 0
for i in range(len(chemin)):
    car = chemin[i]
    if car == "/":
        imax = i
chemin = chemin[:imax + 1]

os.chdir(chemin)


def clean_hide(l):  # Fonction pour supprimer les fichiers cachés
    res = []
    for e in l:
        if e[0] != ".":
            res.append(e)
    return res


def verification_databank():
    global compte_rendu
    nb_problem_detected = 0
    compte_rendu.set("Début de l'analyse")
    # Scan de la Banque de questions
    l_scan = os.listdir("Banque de questions")
    l_scan = clean_hide(l_scan)
    l_types = []

    for i in range(len(l_scan)):
        temp = clean_hide(os.listdir("Banque de questions/" + l_scan[i]))
        for e in temp:  # On élimine les fichiers cachés
            if e[0] != ".":
                l_types.append(l_scan[i] + "/" + e)
    nb_type = len(l_types)

    for i in range(len(l_types)):
        cur = open("Banque de questions/" + l_types[i], "r", -1, "utf-8")
        j = 1
        cond_temp = False

        for ligne in cur:
            if len(ligne.split(" : ")) != len(ligne.split(":")):
                if cond_temp == False:
                    compte_rendu.set(compte_rendu.get() + "\n\n" + l_types[i])
                    cond_temp = True
                compte_rendu.set(compte_rendu.get() + "\n" + "erreur ligne " +
                                 str(j) + ", type = :" + "\n" + ligne.replace("\n", "")[:40])
                nb_problem_detected += 1
            if len(ligne.split(" @ ")) != 2:
                if cond_temp == False:
                    compte_rendu.set(compte_rendu.get() + "\n\n" + l_types[i])
                    cond_temp = True
                compte_rendu.set(compte_rendu.get() + "\n" +
                                 "ligne " + str(j) + " type = @" + "\n" + ligne.replace("\n", "")[:40])
                nb_problem_detected += 1
            j += 1
    compte_rendu.set(compte_rendu.get() + "\n\n" + "Analyse terminée")
    compte_rendu.set(compte_rendu.get() + "\n\n" +
                     f"{nb_problem_detected} problèmes détectés")


def creation_brut(titre, num_quest, mode):
    global compte_rendu, state
    if askyesno(titre, "Créer le QCM à partir du fichier brut.txt ?", icon="question") == False:
        return
    compte_rendu.set("")
    cur_brut = open("brut.txt", "r", -1, "utf-8")
    if mode == "n":
        cur_res = open("QCM_" + titre + ".txt", "w", -1, "utf-8")
        cur_rep = open("reponses_" + titre + ".txt", "w", -1, "utf-8")
        compte_rendu.set("Titre du QCM: " + titre)
        cur_res.write(titre + "\n\n")
        cur_res.write("\n")
        cur_res.write("Nom:" + " " * 50 + "Classe:\n\n")
        cur_res.write("Prénom:\n")
        cur_res.write("\n\n")
    else:
        cur_res = open("QCM_" + titre + ".txt", "a", -1, "utf-8")
        cur_rep = open("reponses_" + titre + ".txt", "a", -1, "utf-8")

    compte_rendu.set(compte_rendu.get() +
                     "\nNuméro de la 1ère question: " + str(num_quest))

    for ligne in cur_brut:
        ligne, rep = ligne.split(" @ ")
        ligne += "\n"
        cur_rep.write(str(num_quest) + "\t" + rep.replace("\n", "") + "\n")
        ligne = ligne.split(" : ")
        question = ligne[0]
        l_reponses = [" "] * (len(ligne) - 1)
        for i in range(1, len(ligne)):
            l_reponses[i - 1] = ligne[i]
        if question.replace(" ", "") == "_" or question.replace(" ", "") == "":
            cur_res.write(str(num_quest) + ". ")
        else:
            cur_res.write(str(num_quest) + ". " + question + "\n")
        for i in range(len(l_reponses)):
            cur_res.write(chr(65 + i) + ") " + l_reponses[i])
            if i == len(l_reponses) - 1:
                cur_res.write("\n")
            else:
                cur_res.write("   ")
        compte_rendu.set(compte_rendu.get() + "\nQuestion " + str(num_quest))
        num_quest += 1

    cur_brut.close()
    cur_res.close()
    cur_rep.close()
    state.set(titre + " terminé")


def creation(fichier_data, mode, num_quest, titre, l_case_fichier):
    global state, compte_rendu
    compte_rendu.set(" " * 30)
    # fichier_data = l_classes[indice_classe[0]]
    if askyesno(titre, "Créer le QCM ?", icon="question") == False:
        return
    state.set(titre + " terminé")
    # Scan de la Banque de questions
    l_scan = os.listdir("Banque de questions")
    l_scan = clean_hide(l_scan)
    l_types = []

    for i in range(len(l_scan)):
        temp = clean_hide(os.listdir("Banque de questions/" + l_scan[i]))
        for e in temp:  # On élimine les fichiers cachés
            if e[0] != ".":
                l_types.append(l_scan[i] + "/" + e)
    nb_type = len(l_types)
    l_types = sorted(l_types)
    # print(l_types)

    plan = [[1, 2, 3] for i in range(nb_type)]
    l_curs = [0] * nb_type

    cur_data = open("Classes/" + fichier_data, "r", -1,
                    "utf-8")  # Ouverture du fichier data

    nom_classe = cur_data.readline()

    compte_rendu.set(compte_rendu.get() + "\nClasse choisie: " +
                     fichier_data.replace(".txt", ""))
    compte_rendu.set(compte_rendu.get() + "\nmode choisi: " + mode)

    if mode == "n":
        compte_rendu.set(compte_rendu.get() + "\nTitre du QCM: " + titre)
        cur_res = open("QCM_" + titre + ".txt", "w", -1, "utf-8")
        cur_res.write(titre)
        cur_res.write("\n\n")
        cur_res.write("Nom:" + " " * 50 + "Classe:\n\n")
        cur_res.write("Prénom:\n")
        cur_res.write("\n\n")
    else:
        cur_res = open("QCM_" + titre + ".txt", "a", -1, "utf-8")

    compte_rendu.set(compte_rendu.get() + "\n" +
                     "Numéro de la 1ere question: " + str(num_quest))

    for i in range(nb_type):
        compte_rendu.set(compte_rendu.get() + "\n" +
                         l_types[i].replace(".txt", ""))
        rep = int(l_case_fichier[i][2].get())
        plan[i] = [l_types[i], rep, []]
        l_curs[i] = open("Banque de questions/" + l_types[i], "r", -1, "utf-8")

    data_str = nom_classe
    # la variable dejavu liste les numéros des questions déjà utilisées dans de précédents QCM

    for ligne in cur_data:
        type, dejavu = ligne.split(" : ")
        dejavu = dejavu.split(",")
        dejavu = [int(e) for e in dejavu]
        for i in range(nb_type):
            if type == plan[i][0]:
                # On charge dans plan la liste des questions déjà utilisées
                plan[i][2] = dejavu
    cur_data.close()  # On ferme le fichier de données

    dossier_prec = plan[0][0].split("/")[0]
    num_dossier = 0
    l_rep = [[]]
    res = ""
    nb = num_quest
    for i in range(nb_type):
        data_local = plan[i]
        if data_local[0].split("/")[0] != dossier_prec:
            res += "@!@"
            l_rep.append([])
            num_dossier += 1
        dossier_prec = data_local[0].split("/")[0]
        # print(data_local)
        # On charge toutes les lignes du fichier dans une liste
        l_ligne = [ligne for ligne in l_curs[i]
                   if ligne.replace("\n", "") != ""]
        nb_ligne = len(l_ligne)
        l_indices = [j for j in range(nb_ligne)]
        for indice in l_indices:
            if indice in data_local[2]:
                l_indices[indice] = -1
        l_ind_2 = []
        for j in range(nb_ligne):
            if l_indices[j] != -1:
                l_ind_2.append(l_indices[j])
        l_indices = l_ind_2

        nb_indice = len(l_indices)
        # On évite les erreurs liées à l'utilisation de toutes les question de la base
        if data_local[1] > nb_indice:
            choix_erreur = askyesno(
                "Erreur", "Erreur: plus assez de questions non utilisées\ndans la base pour terminer le QCM. Souhaitez-vous\ncontinuer malgré tout? Le nombre de questions dans\nle QCM sera inférieur au nombre de questions\ndemandé pour cette catégorie: " + data_local[0], icon="warning")
            if choix_erreur:
                data_local[1] = nb_indice
            else:
                compte_rendu.set(compte_rendu.get() + "\n" + "Annulé")
                return
        # On sélectionne aléatoirement les questions du QCM
        id_questions = sample(l_indices, data_local[1])
        save = data_local[2] + id_questions
        # print(save)
        save = str(save).replace("[", "")
        save = save.replace(" ", "")
        save = save.replace("]", "")
        if save != "":  # bug fix 2.0.1
            data_str += data_local[0] + " : " + save + "\n"
        for j in range(nb_ligne):  # Dans cette boucle on ajoute les questions une par une
            if j in id_questions:
                ligne = l_ligne[j]
                if len(ligne.split(" @ ")) != 2:
                    compte_rendu.set(compte_rendu.get() + "\n\n" + "Erreur dans la base de questions." +
                                     "\n" + "fichier:" + data_local[0] + "\n" + "ligne:" + str(j) + "\n" + ligne)
                    ligne = ligne.replace(" @ ", "")
                    ligne = "#ERREUR# " + ligne + " @ " + "#ERREUR#"
                ligne, rep = ligne.split(" @ ")
                ligne += "\n"
                l_rep[num_dossier].append(rep)
                ligne = ligne.split(" : ")
                question = ligne[0]
                l_reponses = [" "] * (len(ligne) - 1)
                for i in range(1, len(ligne)):
                    l_reponses[i - 1] = ligne[i]
                res += question + "\n"
                for i in range(len(l_reponses)):
                    res += chr(65 + i) + ") " + l_reponses[i]
                    if i == len(l_reponses) - 1:
                        res += "\n"
                    else:
                        res += "   "
                nb += 1
        compte_rendu.set(compte_rendu.get() + "\n" +
                         data_local[0] + " terminé")
        compte_rendu.set(compte_rendu.get() + "\n" +
                         "Nombre de questions: " + str(data_local[1]))

    if mode == "n":
        cur_rep = open("reponses_" + titre + ".txt", "w", -1, "utf-8")
        cur_rep.write(titre + " " + nom_classe + "\n")
    else:
        cur_rep = open("reponses_" + titre + ".txt", "a", -1, "utf-8")

    l_res = res.split("@!@")
    # print(l_res)
    l_finale = []
    for j in range(len(l_res)):
        res = l_res[j]
        res = res.split("\n\n")
        res = res[:len(res) - 1]
        l_indice = [i for i in range(len(l_rep[j]))]
        shuffle(l_indice)

        for i in l_indice:
            temp_res = res[i] + "\n\n"
            temp_rep = "\t" + \
                l_rep[j][i].replace("\n", "") + "\n"
            l_finale.append((temp_res, temp_rep))

    if shuffle_state.get() == 1:
        shuffle(l_finale)

    for i in range(len(l_finale)):
        e = l_finale[i]
        cur_res.write(str(i + num_quest) + ". " + e[0])
        cur_rep.write(str(i + num_quest) + e[1])

    for cur in l_curs:
        cur.close()
    cur_res.close()
    cur_rep.close()
    # On le rouvre pour y écrire les nouvelles données
    cur_data = open("Classes/" + fichier_data, "w", -1, "utf-8")
    cur_data.write(data_str)
    cur_data.close()
    compte_rendu.set(compte_rendu.get() + "\n" + "Terminé")
    reset_choix()
    update(None)


# Création de la fenêtre et de son contenu
l_scan = os.listdir("Banque de questions")  # Scan de la Banque de questions
l_scan = clean_hide(l_scan)
l_types = []

for i in range(len(l_scan)):
    temp = clean_hide(os.listdir("Banque de questions/" + l_scan[i]))
    for e in temp:  # On élimine les fichiers cachés
        if e[0] != ".":
            l_types.append(l_scan[i] + "/" + e)
nb_type = len(l_types)
l_types = sorted(l_types)

main = tk.Tk()
main.title("QCM Maker Version " + version)

compte_rendu = tk.StringVar()


def supp_data(fichier, bypass):
    global compte_rendu
    if bypass == False:
        if askyesno("Demande de confirmation", "Voulez-vous vraiment supprimer les données de cette classe ?", icon="warning") == False:
            return
    cur = open("Classes/" + fichier, "w", -1, "utf-8")
    cur.write(fichier.replace(".txt", "") + "\n")
    cur.write("NoType : 0\n")
    cur.close()
    compte_rendu.set(fichier + "\nDonnées supprimées")
    if bypass == False:
        update()


supp_data("Aucune.txt", True)


def creation_classe(nom):
    global l_classes, compte_rendu, liste_classe
    if askyesno("Demande de confirmation", "Créer la classe " + nom + " ?", icon="question") == False:
        return
    nom += ".txt"
    nom = nom.replace(" ", "")
    if not(nom in l_classes):
        supp_data(nom, True)
        compte_rendu.set("Classe créée\n" + nom)
        l_classes.append(nom)
        chaine = ""
        for classe in l_classes:
            chaine += " " + classe.replace(".txt", "")
        liste_classe.set(chaine)
    else:
        compte_rendu.set("Impossible de créer la classe\nnom déjà utilisé.")


def reset_choix():
    global l_case_fichier
    for i in range(len(l_case_fichier)):
        l_case_fichier[i][2].set("0")


def update_nb_total_quest():
    global nb_total_quest
    nb_total_quest.set("Nombre total de questions: " + str(
        sum([int(l_case_fichier[i][2].get()) for i in range(len(l_case_fichier))])))


l_name_file = []
l_q_rest = []
for fichier in l_types:
    l_name_file.append(tk.StringVar())
    l_q_rest.append(tk.StringVar())


def update_quest_rest():
    global l_name_file
    d_q_rest = {}
    classe_choisie = classe_stringvar.get()
    cur_data = open("Classes/" + classe_choisie, "r", -1, "utf-8")
    cur_data.readline()
    for fichier in l_types:
        cur_scan = open("Banque de questions/" + fichier, "r", -1, "utf-8")
        nb_lignes_fich = 0
        for ligne in cur_scan:
            if ligne != "":
                nb_lignes_fich += 1
        cur_scan.close()
        d_q_rest[fichier] = nb_lignes_fich
        nom_fichier = fichier.replace(".txt", "")
    for ligne in cur_data:
        fichier, data = ligne.split(" : ")
        data = data.split(",")
        if fichier in l_types:
            d_q_rest[fichier] -= len(data)
    for i in range(len(l_types)):
        fichier = l_types[i]
        l_name_file[i].set(fichier)
        l_q_rest[i].set(" / " +
                        str(d_q_rest[fichier]))


def update(args=None):
    update_nb_total_quest()
    # update_quest_rest()


h, w = 62, 100  # Affichage logo
logo = tk.Canvas(main, width=w, height=h)
image_logo = tk.PhotoImage(file="logo_small.png")
logo.create_image(w // 2, h // 2, image=image_logo)
logo.grid(row=0, column=0, columnspan=2)

titre = tk.StringVar()  # Case pour le titre
titre.set("QCM")
case_titre = tk.Entry(main, textvariable=titre)
case_titre.grid(row=1, column=1)
case_inf_titre = tk.Label(main, text="Titre du QCM")
case_inf_titre.grid(row=1, column=0)

l_classes = os.listdir("Classes")  # Case pour choisir la classe
l_classes = clean_hide(l_classes)
case_choix_classe = tk.Label(main, text="Classe sélectionnée:")
case_choix_classe.grid(row=3, column=1)
chaine = ""
for classe in l_classes:
    chaine += " " + classe.replace(".txt", "")
classe_stringvar = tk.StringVar()
classe_stringvar.set(l_classes[0])
case_classe = tk.OptionMenu(main, classe_stringvar, *l_classes)
case_classe.grid(row=4, column=1, sticky='ew')

# Haut de colonne pour banque
# case_banque_donn = tk.Label(main, text="Nombre de questions par fichier:")
# case_banque_donn.grid(row=0, column=5, columnspan=2, sticky="ew")

update_quest_rest()

l_case_fichier = []  # Cases pour nombre de questions de chaque fichier
compt = 1
canv_quest = tk.Canvas(main, width=500, height=500,
                       scrollregion=(0, 0, 600, len(l_types) * 41))
cont_quest = tk.Frame(canv_quest)
canv_quest.grid(row=1, rowspan=8, column=5, sticky="ew")
defilY_quest = tk.Scrollbar(main, orient='vertical',
                            command=canv_quest.yview)
defilY_quest.grid(row=1, rowspan=8, column=6, sticky='ns')
canv_quest['yscrollcommand'] = defilY_quest.set
defilX_cr = tk.Scrollbar(main, orient='horizontal',
                         command=canv_quest.xview)
defilX_cr.grid(row=9, column=5, sticky='ew')
canv_quest['xscrollcommand'] = defilX_cr.set
for i in range(len(l_types)):
    fichier = l_types[i]
    nb_questions = tk.StringVar()
    nb_questions.set("0")
    l_case_fichier.append([tk.Label(cont_quest, textvariable=l_name_file[i]), tk.Entry(
        cont_quest, textvariable=nb_questions, width=6), nb_questions, tk.Label(cont_quest, textvariable=l_q_rest[i])])
    l_case_fichier[-1][0].grid(row=compt, column=0, pady=10)
    l_case_fichier[-1][1].grid(row=compt, column=1)
    l_case_fichier[-1][3].grid(row=compt, column=2)
    compt += 1
canv_quest.create_window(0, 0, anchor='nw', window=cont_quest)
case_choix_creer = tk.Label(
    main, text="Créer un nouveau QCM\nou compléter celui existant ?")
case_choix_creer.grid(row=3, column=0)
vals = ["n", "c"]  # Choix, créer ou compléter
etiqs = ['nouveau', 'compléter']
mode = tk.StringVar()
mode.set(vals[0])
for i in range(2):
    b = tk.Radiobutton(main, variable=mode, text=etiqs[i], value=vals[i])
    b.grid(row=4 + i, column=0)

# Case pour le numéro de la 1ère question
case_num_prem_quest = tk.Label(main, text="Numéro de la 1ère question:")
case_num_prem_quest.grid(row=2, column=0)
num_quest = tk.StringVar()
num_quest.set("1")
res_num_prem_quest = tk.Entry(main, textvariable=num_quest)
res_num_prem_quest.grid(row=2, column=1)

# Bouton de création du QCM
bouton_start = tk.Button(main, text="Créer le QCM", state='normal', command=lambda: creation(classe_stringvar.get(
), mode.get(), int(num_quest.get()), titre.get(), l_case_fichier))
bouton_start.grid(row=9, column=0)
state = tk.StringVar()
case_state = tk.Label(main, textvariable=state)
case_state.grid(row=8, column=1)

compte_rendu.set(" " * 30)
canv_cr = tk.Canvas(main, width=400, height=500,
                    scrollregion=(0, 0, 500, 2000))
canv_cr.grid(row=1, rowspan=8, column=5, sticky="ew")
defilY_cr = tk.Scrollbar(main, orient='vertical',
                         command=canv_cr.yview)
defilY_cr.grid(row=1, rowspan=8, column=9, sticky='nesw')
canv_cr['yscrollcommand'] = defilY_cr.set
defilX_cr = tk.Scrollbar(main, orient='horizontal',
                         command=canv_cr.xview)
defilX_cr.grid(row=9, column=8, sticky='ew')
canv_cr['xscrollcommand'] = defilX_cr.set
case_compte_rendu = tk.Message(canv_cr, textvariable=compte_rendu)

# Case de compte rendu des actions
canv_cr.create_window(0, 0, anchor="nw", window=case_compte_rendu)
canv_cr.grid(row=1, rowspan=7, column=8, sticky="ew")
case_nom_compte_rendu = tk.Label(main, text="Résumé des actions effectuées:")
case_nom_compte_rendu.grid(row=0, column=8, sticky="ew")

case_reset_data = tk.Button(main, text="Réinitialiser les données\nde la classe sélectionnée.",
                            command=lambda: supp_data(classe_stringvar.get(), False))

# Case pour reset les données d'une classe
case_reset_data.grid(row=5, column=1)

# Case pour créer une classe
nom_nouv_classe = tk.StringVar()
nom_nouv_classe.set("Nom de la nouvelle classe")
case_nom_nouv_classe = tk.Entry(main, textvariable=nom_nouv_classe)
case_nom_nouv_classe.grid(row=6, column=1)
bouton_crea_classe = tk.Button(main, text="Créer une nouvelle classe",
                               command=lambda: creation_classe(nom_nouv_classe.get()))
bouton_crea_classe.grid(row=7, column=1)

bouton_crea_brut = tk.Button(main, text="Créer le QCM à partir\ndu fichier brut",
                             command=lambda: creation_brut(titre.get(), int(num_quest.get()), mode.get()))
bouton_crea_brut.grid(row=9, column=1)  # Bouton pour lancer QCMMaker V1

# Bouton de vérification de la base de données
# case_verif_data = tk.Label(main, text="Vérification de la base de questions")
# case_verif_data.grid(row=5, column=1)
bouton_verif_data = tk.Button(
    main, text="Lancer l'analyse de\nla base de questions", command=lambda: verification_databank())
bouton_verif_data.grid(row=7, column=0)

# Case à cocher pour mélanger les questions
# case_shuffle = tk.Label(main, text="Mélanger les questions")
# case_shuffle.grid(row=5, column=0)
shuffle_state = tk.IntVar()
check_shuffle = tk.Checkbutton(
    main, text="Mélanger les questions", variable=shuffle_state)
check_shuffle.grid(row=6, column=0)

# Affichage du nombre total de questions
nb_total_quest = tk.StringVar()
nb_total_quest.set("Nombre total de questions: 0")
case_nb_total_quest = tk.Label(main, textvariable=nb_total_quest)
case_nb_total_quest.grid(row=0, column=5)

verification_databank()
main.columnconfigure(6, weight=10)

main.bind_all("<Button-1>", update)
main.mainloop()
# Fin de la création de la fenêtre
