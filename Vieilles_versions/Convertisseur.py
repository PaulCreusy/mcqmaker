import inspect
import os
import PyPDF2

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

l_files = os.listdir("./Convertisseur")

for file in l_files:
    pdf = open("./Convertisseur/" + file, "rb")
    res = open("./Sortie/" + file.replace(".pdf", ".txt"), "w")
    pdfread = PyPDF2.PdfFileReader(pdf)
    temp = ""
    for x in range(pdfread.numPages):
        pageobj = pdfread.getPage(x)
        text = pageobj.extractText()
        temp += text
        # res.write(text)
    pdf.close()
    l_lignes = temp.split("\n")
    l_questions = []
    temp = ""
    for ligne in l_lignes:
        if len(ligne.replace("\n", "").replace(" ", "")) > 0 and ord(ligne[0].replace("\n", "").replace(" ", "")) > 48 and ord(ligne[0].replace("\n", "").replace(" ", "")) < 58:
            l_questions.append(temp)
            temp = ""
        temp += ligne + "\n"
    l_questions.pop(0)
    l_questions.pop(0)
    print(l_questions[0])
    for i in range(len(l_questions)):
        question = l_questions[i]
        slicing = []
        while ")" in question:
            temp = question.split(")", 1)
            slicing.append(temp[0][:-1])
            question = temp[1]
        slicing.append(question)
        l_questions[i] = slicing[1:]
    for i in range(len(l_questions)):
        for j in range(len(l_questions[i])):
            item = l_questions[i][j]
            item = item.replace(" \n", "")
            item = item.replace("\n", "")
            l_questions[i][j] = item
    print(l_questions[0])
    for question in l_questions:
        for i in range(len(question)):
            while len(question[i]) > 0 and question[i][0] == " ":
                question[i] = question[i][1:]
            if i < len(question) - 1:
                res.write(question[i] + " : ")
            else:
                res.write(question[i] + "\n")
    res.close()
