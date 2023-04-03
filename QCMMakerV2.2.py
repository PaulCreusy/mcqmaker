# Version 2.2.1

# -*- coding: utf-8 -*-


# Format des questions dans les fichiers .txt situés dans le dossier "Banque de questions" voir ci dessous:

"""

Question 1 : Reponse A : Reponse B : Reponse C : Reponse D ! A

Question 2 : Reponse A : Reponse B ! B

"""

# Le fait que le nombre de réponse ne soit pas le même pour toutes les questions n'est pas problématique

# Attention, bien respecter les espaces de part et d'autre des deux points

# Attention, lorsque des questions sont ajoutées à la banque, elles doivent impérativement être mises à la fin du fichier .txt

# Attention, toujours laisser une ligne vide à la fin d'un fichier de questions


import os
import sys
import inspect

from random import *

from time import sleep


chemin = inspect.getsourcefile(lambda: 0)

t = chemin.split("\\")

chemin = ""

for i in range(len(t) - 1):

    chemin += t[i] + "\\"


os.chdir(chemin)


def clean_hide(l):

    res = []

    for e in l:

        if e[0] != ".":

            res.append(e)

    return res


print("QCM Maker Version 2.2.1")

print()


l_scan = os.listdir("Banque de questions")

l_scan = clean_hide(l_scan)


l_types = []

for i in range(len(l_scan)):

    temp = clean_hide(os.listdir("Banque de questions/" + l_scan[i]))

    for e in temp:

        if e[0] != ".":

            l_types.append(l_scan[i] + "/" + e)

nb_type = len(l_types)

print(l_types)


print()

print("Numéro de la 1ere Question:")

num_quest = int(input())


plan = [[1, 2, 3] for i in range(nb_type)]

l_curs = [0] * nb_type

l_rep = []


cur_data = open("data.txt", "r", -1, "utf-8")

nom_classe = cur_data.readline()

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


print("Classe choisie:" + nom_classe)

sleep(0.5)

print("Titre du QCM:", end=" ")

titre = input()


cur_res = open("QCM.txt", "w", -1, "utf-8")

cur_res.write(titre)

cur_res.write("\n\n")

cur_res.write("Nom:" + " " * 50 + "Classe:\n\n")

cur_res.write("Prénom:\n")

cur_res.write("\n\n")


for i in range(nb_type):

    print()

    print(l_types[i].replace(".txt", ""))

    print("Nombre de questions:", end=" ")

    rep = int(input())

    plan[i] = [l_types[i], rep, []]

    l_curs[i] = open("Banque de questions/" + l_types[i], "r", -1, "utf-8")


res = ""

nb = 1

for i in range(nb_type):

    data_local = plan[i]

    # On charge toutes les lignes dans une liste
    l_ligne = [ligne for ligne in l_curs[i]]

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

        print("Erreur: plus assez de questions non utilisées dans la base pour terminer le QCM.")

        print("Souhaitez-vous continuer malgré tout? Le nombre de questions dans le QCM sera inférieur au nombre de questions demandé pour cette catégorie.")

        print(data_local[0])

        print("o/n:", end="")

        if input() == "o":

            data_local[1] = nb_indice

        else:

            exit()

    # On sélectionne aléatoirement les questions du QCM
    id_questions = sample(l_indices, data_local[1])

    save = data_local[2] + id_questions

    save = str(save).replace("[", "")

    save = save.replace(" ", "")

    save = save.replace("]", "")

    if save != "":  # bug fix 2.0.1

        data_str += data_local[0] + " : " + save + "\n"

    print()

    for j in range(nb_ligne):  # Dans cette boucle on ajoute les questions une par une

        if j in id_questions:

            ligne = l_ligne[j]

            ligne, rep = ligne.split(" @ ")

            ligne += "\n"

            l_rep.append(rep)

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

            print("Question " + str(nb))

            nb += 1

    print(data_local[0] + " terminé")

    print()

res = res.split("\n\n")

res = res[:len(res) - 1]

l_indice = [i for i in range(len(l_rep))]

shuffle(l_indice)

cur_rep = open("reponses.txt", "w", -1, "utf-8")

cur_rep.write(titre + " " + nom_classe + "\n")

for i in l_indice:

    cur_res.write(str(num_quest) + ". " + res[i] + "\n\n")

    cur_rep.write(str(num_quest) + "\t" + l_rep[i])

    num_quest += 1

for cur in l_curs:

    cur.close()

cur_res.close()

cur_rep.close()

# On le rouvre pour y écrire les nouvelles données
cur_data = open("data.txt", "w", -1, "utf-8")

cur_data.write(data_str)

cur_data.close()

print("fichiers fermés")

sleep(1)
