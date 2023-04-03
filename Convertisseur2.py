# https://concours.ensea.fr/pdfs/ats/annales/
import inspect
import os

chemin = ""

chemin = inspect.getsourcefile(lambda: 0)
chemin = chemin.replace("\\", "/")
imax = 0
for i in range(len(chemin)):
    car = chemin[i]
    if car == "/":
        imax = i
chemin = chemin[:imax+1]

os.chdir(chemin)

cur = open("entree.txt", "r", encoding="utf-8")
res = open("sortie.txt", "w", encoding="utf-8")

sto = ""
for line in cur:
    line = line.replace("\n", "")
    if len(line.replace(" ", "").replace("-", "").replace("\n", "")) <= 3:
        # if sto.replace("\n", "").replace(" ", "") != "":
        #     res.write(sto + "\n")
        # sto = ""
        sto += line.replace(" ", "").replace("\n", "")
    else:
        temp = line.split(")")
        if len(temp) == 1:
            sto += line
        else:
            if ord(line[0]) > 47 and ord(line[0]) < 59:
                while (ord(line[0]) > 47 and ord(line[0]) < 59) or line[0] == ")" or line[0] == " ":
                    line = line[1:]
                if sto.replace("\n", "").replace(" ", "") != "":
                    while "  :" in sto:
                        sto = sto.replace("  :", " :")
                    while ":  " in sto:
                        sto = sto.replace(":  ", ": ")
                    res.write(sto + "\n")
                    # print("ok")
                line = line.replace(":", "")
                for i in range(97, 123):
                    line = line.replace(chr(i) + ")", " :")
                for i in range(65, 91):
                    line = line.replace(chr(i) + ")", " :")
                line = line.replace("\n", "")
                sto = line
            else:
                line = line.replace(":", "")
                for i in range(97, 123):
                    line = line.replace(chr(i) + ")", " :")
                for i in range(65, 91):
                    line = line.replace(chr(i) + ")", " :")
                line = line.replace("\n", "")
                sto += line
res.write(sto)
cur.close()
res.close()
