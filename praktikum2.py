import os
import time

def menu():
    print("AMBI Praktikum Aufgabe Nr.2 von Alexander Schleiter und Tim Stadager")
    data = input("Geben sie die Datei an die sie einlesen möchten:"     )
    text = data_input(data)
    i = 0
    while i == 0:
        levenshtein_distance(text)
        i = 1

def data_input(data):
    counter = 0
    t = []
    key = ""
    value = ""
    counter1 = 0
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
                    t.append([])
                    value = value.replace("\n","")
                    t[counter1].append(key)
                    t[counter1].append(value)
                    key, value = "", ""
                    counter = 0
                    counter1 += 1
    return t

def levenshtein_distance(text):
    gap_cost = 1
    table = []
    distance = 0
    final_distanz = [[]]
    final_distanz[0].append(" "*30)
    for i in range(len(text)):
        final_distanz[0].append(text[i][0])
        final_distanz.append([])
        if i >= 1:
            final_distanz[i].append(text[i][0])
    final_distanz.pop(len(text))
    for i in range(len(text)):#initialization form x and y from the list
        for k in range(len(text)):
            len_x = len(text[i][1])
            len_y = len(text[k][1])
            if len_x == len_y:
                distance = 0
            elif len_x != len_y:
                for a in range(len_y): # column of matrix
                    table.append([])
                for x in range(len_x):
                    table[0].append(x)
                for y in range(1,len_y):
                    table[y].append(y)
                for y in range(1,len_y):
                    for x in range(1,len_x):
                        if text[i][1][x] == text[k][1][y]:
                            gap_cost = 0
                        else:
                            gap_cost = 1
                        table[y].append(min(table[y-1][x]+1, table[y-1][x-1]+gap_cost, table[y][x-1]+1))
                distance = table[len_y-1][len_x-1]
            if i >= len(text):
                final_distanz[i+1].append(distance)
            else:
                final_distanz[i].append(distance)
    print(final_distanz)

if __name__ == "__main__":
    menu()



