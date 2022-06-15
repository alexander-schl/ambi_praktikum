import os
import time
import traceback


def menu():
    print("AMBI Praktikum Aufgabe Nr.2 von Alexander Schleiter und Tim Stadager")
    while True:
        try:
            #aquifex-tRNA.fasta
            data = input("Geben Sie den Pfad einer Datei an, die Sie einlesen möchten:")
            if os.path.isfile(data):
                text = data_input(data)

                print("\nHamming-Distanzmatrix:")
                hamming = hamming_distance(text.copy())
                for row in hamming:
                    print(row)

                print("\nLevenshtein-Distanzmatrix:")
                levenshtein = levenshtein_distance(text.copy())
                for row in levenshtein:
                    print(row)

                start_time_upgma = time.time()
                print("\nUPGMA-Newick-String:")
                #upgma =
                #print(upgma)
                print("Laufzeit von UPGMA: ", time.time() - start_time_upgma)

                start_time_nj = time.time()
                print("\nNeighbour-Joinig-Newick-String:")
                neighbours = neighbor_joining_algorithm(levenshtein.copy())
                newick_neighbour = construct_newick_string(neighbours)
                print(newick_neighbour)
                print("Laufzeit von Neighbour Joining: ", time.time() - start_time_nj)

                break
            else:
                print("Der angegebene Pfad konnte nicht gefunden werden. Versuchen Sie es erneut.")
        except FileNotFoundError:
            print("Der angegebene Pfad konnte nicht gefunden werden. Versuchen Sie es erneut.")

def data_input(data):
    counter = 0
    t = []
    key = ""
    value = ""
    counter1 = 0
    path = os.path.abspath(data)
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8")as text:
            for i in text:
                if i[0] == ">":
                    for k in range(1, len(i)):
                        if i[k] == " ":
                            break
                        key += i[k]
                if i[0] != ">":
                    value += i

                counter += 1
                if counter == 3:
                    t.append([])
                    value = value.replace("\n", "")
                    t[counter1].append(key)
                    t[counter1].append(value)
                    key, value = "", ""
                    counter = 0
                    counter1 += 1
    return t


def hamming_distance(text):
    """
    Constructs distance matrix with Hamming distance. Unequal sequence length is marked as -1.

    :param text: list of lists with sequence names and sequences
    :return: list of lists
    """
    matrix = [[""]]

    for row in text:
        matrix.append([row[0]])
        matrix[0].append(row[0])

    # insert "" to account for index in final matrix when comparing
    text.insert(0, "")

    for y in range(1, len(matrix)):
        for x in range(1, len(matrix)):
            seq1 = text[y][1]
            seq2 = text[x][1]
            distance = 0
            if len(seq1) == len(seq2):
                for i in range(len(seq1)):
                    if seq1[i] != seq2[i]:
                        distance += 1
            else:
                distance = -1

            matrix[y].append(distance)



    return matrix

def levenshtein_distance(text):
    distance = 0
    final_distanz = [[]]
    final_distanz[0].append(" " * 25)
    for i in range(len(text)):
        final_distanz[0].append(text[i][0])
        final_distanz.append([])
        final_distanz[i + 1].append(text[i][0])
    for i in range(len(text)):  # initialization form x and y from the list
        for k in range(len(text)):
            table = []
            len_x = len(text[i][1])
            len_y = len(text[k][1])
            if text[i][0] == text[k][0]:
                distance = 0
            else:
                for a in range(len_y):  # column of matrix
                    table.append([])
                for x in range(len_x):
                    table[0].append(x)
                for y in range(len_y):
                    if y > 0:
                        table[y].append(y)
                for y in range(1, len_y):
                    for x in range(1, len_x):
                        if text[i][1][x - 1] == text[k][1][y - 1]:
                            gap_cost = 0
                        else:
                            gap_cost = 1
                        table[y].append(min(table[y - 1][x] + 1, table[y - 1][x - 1] + gap_cost,
                                            table[y][x - 1] + 1))
                distance = table[len_y - 1][len_x - 1]
            final_distanz[i + 1].append(distance)
    # for i in range(len(final_distanz)):
    #     print(final_distanz[i])
    return (final_distanz)

# def levenshtein_distance(text):
#     distance = 0
#     final_distanz = [[]]
#     final_distanz[0].append(" " * 25)
#     for i in range(len(text)):
#         final_distanz[0].append(text[i][0])
#         final_distanz.append([])
#         final_distanz[i + 1].append(text[i][0])
#     for i in range(len(text)):  # initialization form x and y from the list
#         for k in range(len(text)):
#             table = []
#             len_x = len(text[i][1])
#             len_y = len(text[k][1])
#             if text[i][0] == text[k][0]:
#                 distance = 0
#             else:
#                 for a in range(len_y):  # column of matrix
#                     table.append([])
#                 for x in range(len_x):
#                     table[0].append(x)
#                 for y in range(len_y):
#                     if y > 0:
#                         table[y].append(y)
#                 for y in range(1, len_y):
#                     for x in range(1, len_x):
#                         if text[i][1][x - 1] == text[k][1][y - 1]:
#                             gap_cost = 0
#                         else:
#                             gap_cost = 1
#                         table[y].append(min(table[y - 1][x] + 1, table[y - 1][x - 1] + gap_cost,
#                                             table[y][x - 1] + 1))
#                 distance = table[len_y - 1][len_x - 1]
#             final_distanz[i + 1].append(distance)
#     # for i in range(len(final_distanz)):
#     #     print(final_distanz[i])
#     return (final_distanz)


def neighbor_joining_algorithm(matrix):
    """
    Uses the neighbour joining algorithm to construct parent and child nodes of sequences with
    the following structure:
    {'parent': 'name', 'child1': ('name_child1', distance_to_parent_node),
        'child2': ('name_child2', distance_to_parent_node)}

    :param matrix: Distance matrix (list of lists).
    :return: List of dicts.
    """

    # stores pairs of joined sequences and parent
    all_neighbours = []

    u_counter = 0
    while len(matrix) > 3:
        divergence_matrix_template = make_divergence_matrix(matrix)
        divergence_matrix = divergence_matrix_template.copy()
        minimal_values = []
        for i in range(1, len(divergence_matrix)):
            all_vals = set(divergence_matrix[i][1:])

            # construct dict with lowest value for each row,
            # keep x and y indices of distance in matrix
            try:
                min_dict = {
                    "value": int(sorted(all_vals)[1]),
                    "y": divergence_matrix.index(divergence_matrix[i]),
                    "x": divergence_matrix[i].index(sorted(all_vals)[1])
                }
            except Exception:
                min_dict = {
                    "value": int(sorted(all_vals)[0]),
                    "y": divergence_matrix.index(divergence_matrix[i]),
                    "x": divergence_matrix[i].index(sorted(all_vals)[0])
                }

            minimal_values.append(min_dict)

        # get dict with lowest divergence
        lowest_divergence = min(minimal_values, key=lambda x: x["value"])

        x = lowest_divergence["x"]
        y = lowest_divergence["y"]

        # sum of all distances for sequence1
        sum1 = sum(matrix[y][1:])
        # sum of all distances for sequence2
        sum2 = sum(matrix[x][1:])

        dfu = 1 / 2 * matrix[y][x] + (sum1 - sum2) / (2 * ((len(matrix) - 1) - 2))
        dgu = matrix[y][x] - dfu

        # set smaller distance of child node to 0 and add absolute value of it to
        # other child node distance
        if dfu < 0 or dgu < 0:
            if dfu < dgu:
                dgu += abs(dfu)
                dfu = 0
            else:
                dfu += abs(dgu)
                dgu = 0

        new_sequence = "u" + str(u_counter)

        neighbours = {
            "parent": new_sequence,
            "child1": (matrix[y][0], dfu),
            "child2": (matrix[x][0], dgu)
        }
        all_neighbours.append(neighbours)

        matrix.append([new_sequence])
        matrix[0].append(new_sequence)

        # calc distance of new sequence to each old sequence and add them from top to bottom
        for i in range(1, len(matrix)):
            new_distance = 1 / 2 * (matrix[i][y] + matrix[i][x] - matrix[y][x])
            matrix[i].append(new_distance)
            matrix[-1].append(new_distance)

        # clean up because last value in last row is doubled
        matrix[-1].pop(len(matrix))

        # delete two old sequences, always delete larger index first, so that the reduction in
        # matrix size doesn't lead to wrong deletion, because of index shifts
        if y > x:
            matrix.pop(y)
            matrix.pop(x)
        else:
            matrix.pop(x)
            matrix.pop(y)

        for row in matrix:
            if y > x:
                row.pop(y)
                row.pop(x)
            else:
                row.pop(x)
                row.pop(y)

        u_counter += 1

    return all_neighbours


def make_divergence_matrix(matrix_template):
    """
    Cosntruct a divergence matrix.

    :param matrix_template: Distance matrix (list of lists).
    :return: List of lists
    """

    matrix = matrix_template.copy()
    divergence_matrix = []

    divergence_matrix.append(matrix[0])
    factor = (len(matrix) - 1) - 2

    for y in range(1, len(matrix)):
        divergent_row = [matrix[y][0]]
        for x in range(1, len(matrix[y]) - 1):
            try:
                # R_i sum of all distances for sequence1
                sum1 = sum(matrix[y][1:])
                # R_j sum of all distances for sequence2
                sum2 = sum(matrix[x][1:])
                divergence = factor * matrix[y][x] - sum1 - sum2
                divergent_row.append(divergence)
            except:
                print("...")
        divergence_matrix.append(divergent_row)

    return divergence_matrix


def construct_newick_string(all_neighbours):
    """
    Constructs a Newick string.

    :param all_neighbours: list of dicts with the following structure:
        {'parent': 'name', 'child1': ('name_child1', distance_to_parent_node),
        'child2': ('name_child2', distance_to_parent_node)}

    :return: str
    """

    newick_string_as_list = []

    # for pair in all_neighbours:
    #     print(pair)

    # holds nodes that are only parent nodes, and their children
    only_parents = keep_only_parents(all_neighbours)
    for pair in only_parents:
        newick_string_as_list.append("(")
        newick_string_as_list.append(pair["child1"][0])
        newick_string_as_list.append(",")
        newick_string_as_list.append(pair["child2"][0])
        newick_string_as_list.append(")")
        newick_string_as_list.append(pair["parent"])
        newick_string_as_list.append(",")

    # keep nodes that are parents as well as children of other nodes
    remaining_neighbours = [pair for pair in all_neighbours if pair not in only_parents]

    while len(remaining_neighbours) > 0:
        only_parents.clear()
        only_parents = keep_only_parents(remaining_neighbours)
        remaining_neighbours_backup = remaining_neighbours.copy()
        remaining_neighbours.clear()
        remaining_neighbours = [pair for pair in remaining_neighbours_backup if
                                pair not in only_parents]

        for pair in only_parents:
            # add children at position of parent node
            if pair["parent"] in newick_string_as_list:
                pos_of_parent = newick_string_as_list.index(pair["parent"])
                newick_string_as_list.insert(pos_of_parent, ")")
                newick_string_as_list.insert(pos_of_parent, pair["child2"][0])
                newick_string_as_list.insert(pos_of_parent, ",")
                newick_string_as_list.insert(pos_of_parent, pair["child1"][0])
                newick_string_as_list.insert(pos_of_parent, "(")

            # add parent node and children at the end of the string
            else:
                newick_string_as_list.append("(")
                newick_string_as_list.append(pair["child1"][0])
                newick_string_as_list.append(",")
                newick_string_as_list.append(pair["child2"][0])
                newick_string_as_list.append(")")
                newick_string_as_list.append(pair["parent"])
                newick_string_as_list.append(",")

    newick_string = "".join(newick_string_as_list)
    final_newick_string = newick_string.removesuffix(",")
    final_newick_string += ";"
    return final_newick_string


def keep_only_parents(neighbours):
    """
    Removes all nodes that are parent and child nodes simultaneously.
    Keeps only pure parent nodes (and their children).

    :param neighbours: list of dicts with parent node and two child nodes
    :return: list of dicts that contains only nodes that are parents but not children
    """

    all_parents = []
    for pair in neighbours:
        all_parents.append(pair)

    # put parents that are also children in a separate list as deletion in a for loop is bad
    parents_to_be_removed = []
    for parent in all_parents:
        for i in range(len(neighbours)):
            if parent["parent"] in neighbours[i]["child1"] or parent["parent"] in \
                    neighbours[i]["child2"]:
                parents_to_be_removed.append(parent)
                break

    only_parents = [pair for pair in all_parents if pair not in parents_to_be_removed]

    return only_parents


if __name__ == "__main__":
    # text = data_input("aquifex-tRNA.fasta")
    # levi = levenshtein_distance(text)
    # print(text)
    # menu()


    #print(levi)
    # all_neighbours = neighbor_joining_algorithm(levi)
    print(construct_newick_string([{'parent': 'u0', 'child1': 'a', 'child2': 'b'}, {'parent': 'u1', 'child1': 'u0', 'child2': 'e'}, {'parent': 'u2', 'child1': 'c', 'child2': 'd'}, {'parent': 'u3', 'child1': 'u1', 'child2': 'u2'}]))
