cur = open("entree.txt", "r", encoding="utf-8")

data = ""
for line in cur:
    data += line
bg = data

for i in range(97, 123):
    bg = bg.replace(chr(i), "a")
for i in range(65, 91):
    bg = bg.replace(chr(i), "A")
for i in range(48, 58):
    bg = bg.replace(chr(i), "1")
#bg = bg.replace("\n", " ")
bg = bg.replace("\t", " ")
for i in range(len(bg)):
    if bg[i] != "a" and bg[i] != "A" and bg[i] != " " and bg[i] != "." and bg[i] != "\n" and bg[i] != "1":
        bg = bg[:i] + "!" + bg[i+1:]
# print(bg)
assert len(bg) == len(data)

extraction = []
last_i = 0
temp = []
compt = 0

data = data.replace("\n", " ")
bg = bg.replace("\n", " ")
# print(bg)
for i in range(len(data)-3):
    if bg[i:i+3] == "1! ":
        compt += 1
        temp.append(data[last_i+3: i])
        extraction.append(temp)
        temp = []
        last_i = i
    elif bg[i:i+4] == " A! ":
        if len(temp) == 0:
            temp.append(data[last_i+3: i])
        else:
            temp.append(data[last_i+4: i])
        last_i = i
temp.append(data[last_i+4: len(data)])
extraction.append(temp)
# print(extraction)

for i in range(len(extraction)):
    for j in range(len(extraction[i])):
        temp = extraction[i][j]
        while len(temp) > 0 and temp[0] == " ":
            temp = temp[1:]
        while len(temp) > 0 and (temp[-1] == " " or (ord(temp[-1]) >= 48 and ord(temp[-1]) < 58)):
            temp = temp[:-1]
        temp = temp.replace(" :", ":")
        temp = temp.replace(": ", ":")
        extraction[i][j] = temp

res = open("sortie.txt", "w", encoding="utf-8")

extraction = extraction[1:]

for i in range(len(extraction)):
    for j in range(len(extraction[i])):
        if j == len(extraction[i]) - 1:
            res.write(extraction[i][j] + "\n")
        else:
            res.write(extraction[i][j] + " : ")
cur.close()
res.close()
