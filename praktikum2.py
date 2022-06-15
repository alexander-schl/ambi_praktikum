import copy
import os
import time

def menu():
    print("AMBI Praktikum Aufgabe Nr.2 von Alexander Schleiter und Tim Stadager")
    #data = input("Geben sie die Datei an die sie einlesen möchten:"     )
    #text = data_input(data)
    i = 0
    while i == 0:
        #lev_distance =  levenshtein_distance(text)
        lev_distance = [[" ","a","b","c","d","e"],["a",0,17,21,31,23],["b",17,0,30,34,21],["c",21,30,0,28,39],["d",31,34,28,0,43],["e",
                        23,21,39,43,0]]
        upgma(lev_distance)
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

    distance = 0
    final_distanz = [[]]
    final_distanz[0].append(" "*25)
    for i in range(len(text)):
        final_distanz[0].append(text[i][0])
        final_distanz.append([])
        final_distanz[i+1].append(text[i][0])
    for i in range(len(text)):#initialization form x and y from the list
        for k in range(len(text)):
            table = []
            len_x = len(text[i][1])
            len_y = len(text[k][1])
            if text[i][0] == text[k][0]:
                distance = 0
            else:
                for a in range(len_y): # column of matrix
                    table.append([])
                for x in range(len_x):
                    table[0].append(x)
                for y in range(len_y):
                    if y > 0:
                        table[y].append(y)
                for y in range(1, len_y):
                    for x in range(1, len_x):
                        if text[i][1][x-1] == text[k][1][y-1]:
                            gap_cost = 0
                        else:
                            gap_cost = 1
                        table[y].append(min(table[y-1][x]+1, table[y-1][x-1]+gap_cost, table[y][x-1]+1))
                distance = table[len_y-1][len_x-1]
            final_distanz[i+1].append(distance)
    for i in range(len(final_distanz)):
        print(final_distanz[i])
    return(final_distanz)


def upgma(matrix):
    """""
    for i in range(1, len(matrix)):
        counter = 1
        for k in range(1, len(matrix)):
            if matrix[i][k] == 0:
                while counter >= 1:
                    matrix[i].pop(1)
                    counter -= 1
                break
            counter += 1
    
    for i in range(len(matrix)):
        print(matrix[i])
    """""
    while len(matrix[1]) > 3:
        counter = 0
        minimum = matrix[1][2]
        min_list = [1,2]
        for i in range(1, len(matrix)):
            for k in range(1, len(matrix[i])):
                if minimum > matrix[i][k] >= 0 and i != k:
                    min_list[0] = i # Weiterarbeiten mit der vollständige Matrix und zurückführen
                    min_list[1] = k
                    minimum = matrix[min_list[0]][min_list[1]]
        min_list.sort()
        print(minimum)
        print(min_list)
        updated_list = [matrix[min_list[0]][0]+"+"+matrix[min_list[1]][0]]
        print(len(updated_list[0].split("+")))
        proportional = len(updated_list[0].split("+"))
        for i in range(1, len(matrix[min_list[0]])):
            if matrix[min_list[0]][i] == 0 or matrix[i][min_list[1]] == 0:
                continue
            else:
                updated_list.append((matrix[min_list[0]][i]*(proportional-1)+(matrix[i][min_list[1]]))/proportional)
        updated_list.insert(min_list[0], 0)
        print("Updated List:",  updated_list)
        matrix.pop(min_list[0])         #Attention the bigger indix must be deleted first
        matrix.insert(min_list[0], updated_list)
        matrix.pop(min_list[1])
        copy_list = copy.copy(updated_list)
        #matrix.insert(updated_list, min(min_list))
        for i in range(len(matrix)):
                matrix[i].pop(min_list[0])
                matrix[i].insert(min_list[0], copy_list[i])
                if i == min_list[0]:
                    continue
                matrix[i].pop(min_list[1])
        #matrix.insert(min(min_list), updated_list)
        for i in range(len(matrix)):
            print(matrix[i])


def neighbor_joining_algorithm(matrix):
    for row in matrix:
        print(row)

    divergence_matrix = []

    divergence_matrix.append(matrix[0])
    factor = (len(matrix) - 1) - 2

    for y in range(1, len(matrix)):
        divergent_row = [matrix[y][0]]
        for x in range(1, len(matrix[y]) -1):
            try:
                # R_i sum of all distances for sequence1
                sum1 = sum(matrix[y][1:])
                # R_j sum of all distances for sequence2
                sum2 = sum(matrix[x][1:])
                gfgf = len(matrix)
                divergence = factor * matrix[y][x] - sum1 - sum2
                divergent_row.append(divergence)
            except:
                print("hfd")
        divergence_matrix.append(divergent_row)

    for row in divergence_matrix:
        print(row),

    # text = data_input("aquifex-tRNA.fasta")
    # levi = levenshtein_distance(text)
    # neighbor_joining_algorithm(levi)
if __name__ == "__main__":
    menu()



