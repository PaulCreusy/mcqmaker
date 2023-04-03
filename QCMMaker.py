# !/usr/local/bin/python3
# -*- coding: utf-8 -*-

# Format des questions dans le fichier brut.txt voir ci dessous:
"""
Titre du QCM
Question 1 : Reponse A : Reponse B : Reponse C : Reponse D
Question 2 : Reponse A : Reponse B
"""
# Le fait que le nombre de réponse ne soit pas le même pour toutes les questions n'est pas problématique
# Attention, bien respecter les espaces de part et d'autre des deux points
print("QCM Maker Version 1.1.0")
import os,sys,inspect

chemin = inspect.getsourcefile(lambda:0)
t = chemin.split("\\")
chemin = ""
for i in range(len(t)-1):
    chemin += t[i] + "\\"

#os.chdir(chemin)

cur_brut = open("brut.txt","r",-1,"utf-8")
cur_res = open("QCM.txt","w",-1,"utf-8")

print("Titre du QCM: ", end = "")
titre = input()

cur_res.write(titre + "\n\n")
cur_res.write("\n")
cur_res.write("Nom:" + " "*50 + "Classe:\n\n")
cur_res.write("Prénom:\n")
cur_res.write("\n\n")

print()
print("Numéro de la 1ere question: ")
nb = int(input())

for ligne in cur_brut:
    ligne = ligne.split(" : ")
    question = ligne[0]
    l_reponses = [" "]*(len(ligne)-1)
    for i in range(1,len(ligne)):
        l_reponses[i-1] = ligne[i]
    cur_res.write(str(nb) +". " + question + ":\n")
    for i in range(len(l_reponses)):
        cur_res.write(chr(65+i) + ") " + l_reponses[i])
        if i == len(l_reponses)-1:
            cur_res.write("\n")
        else:
            cur_res.write("   ")
    print("Question " + str(nb))
    nb += 1

cur_brut.close()
cur_res.close()

