import os
import time

def menu():
    print("AMBI Praktikum Aufgabe Nr.2 von Alexander Schleiter und Tim Stadager")
    data = input("Geben sie die Datei an die sie einlesen möchten:"     )
    text = data_input(data)
    print(text)
    i = 0
    while i == 0:
        levenshtein_distanz(text)


def data_input(data):
    counter = 0
    t = {}
    key = ""
    value = ""
    path = os.path.abspath(data)
    if os.path.isfile(path):
        with open(path,"r", encoding="utf-8")as text:
            for i in text:
                if i[0] == ">":
                    for k in range(1, len(i)):
                        if i[k] == " ":
                            break
                        key += i[k]
                if i[0] != ">":
                    value += i

                counter += 1
                if counter == 3 :
                    value = value.replace("\n","")
                    t[key] = value
                    key, value = "", ""
                    counter = 0

    return t

def levenshtein_distanz(text):
    gap_cost = 5
    table = []
    for i in range(0, len(text.values()[0])):
        table[i, 0] = table[i-1, 0]+gap_cost
    for j in range(0, len(text.values()[1])):
        table[0, j] = table[0, j-1]+gap_cost
    for i in range(0, len(text.values()[0])):
        for j in range(0, len(text.values()[1])):
            # Anfang der Levenshstein-Distanz Abgeschrieben von den Folien
if __name__ == "__main__":
    menu()



