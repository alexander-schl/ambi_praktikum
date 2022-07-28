import copy
import math
import random



def calc_hidden_markov_model():
    k = 999
    change = ["0.9", "0.1", "0.8", "0.2"]
    sequenz = []
    state = []
    symbol = ["", "-", "+"]
    model1 = [["", "A", "C", "G", "T"],
              ["A", "0.300", "0.205", "0.285", "0.210"],
              ["C", "0.322", "0.298", "0.078", "0.302"],
              ["T", "0.248", "0.246", "0.298", "0.208"],
              ["G", "0.177", "0.239", "0.292", "0.292"]]
    model2 = [["", "A", "C", "G", "T"],
              ["A", "0.180", "0.274", "0.426", "0.120"],
              ["C", "0.171", "0.368", "0.274", "0.188"],
              ["T", "0.161", "0.339", "0.375", "0.125"],
              ["G", "0.079", "0.355", "0.384", "0.182"]]
    steady = 1  # which model
    if random.randint(1, 2) == 2:
        steady = 2
    start = random.randint(1, 4)    #random choice for the first base
    if sequenz == 1:
        sequenz.append(model1[0][start])
    else:
        sequenz.append(model2[0][start])
    state.append(symbol[steady])
    while k > 0:
        if steady == 1:             #decide which modell is used
            if random.random() > 0.9:
                steady = 2
                switch = change[1]
            else:
                steady = 1
                switch = change[0]
        else:
            if random.random() > 0.8:
                steady = 1
                switch = change[3]
            else:
                steady = 2
                switch = change[2]
        add = 0
        if switch == "0.9" or switch == "0.8":
            end = random.random()
        elif switch == "0.1":
            end = random.uniform(0.0, 0.1)
        else:
            end = random.uniform(0.0, 0.2)
        state.append(symbol[steady])
        if steady == 1:
            for i in range(1, len(model1[start])):  #sum the line when the same model is used or sum the same value
                if switch == "0.9":
                    add += float(model1[start][i])
                else:
                    add += float(switch)*0.25
                if end <= add:
                    sequenz.append(model1[0][i])
                    start = i
                    break
        else:
            for i in range(1, len(model2[start])):
                if switch == "0.8":
                    add += float(model2[start][i])
                else:
                    add += float(switch)*0.25
                if end <= add:
                    sequenz.append(model2[0][i])
                    start = i
                    break
        k -= 1
    s = "".join(sequenz)
    st = "".join(state)
    return s, st


def calc_viterbi_path(sequence, minus_model, plus_model, transitions):
    """
    Calculates the Viterbi path for a given nucleotide sequence.

    :param sequence: A string containing the nucleotide sequence
    :param minus_model: A matrix (list of lists) with the emission probabilities based on a state.
    :param plus_model: A matrix (list of lists) with the emission probabilities based on another state.
    :param transitions: A matrix (list of lists) with the transition probabilities for two states.
    :return: Viterbi path (str)
    """
    minus_path = []
    plus_path = []
    viterbi_path_str = ""

    # 1/2 because of two states
    starting_state_prob = 1 / 2

    # 1/4 because of ACGT
    starting_emission_prob = 1 / 4
    minus_path.append(("-", math.log(starting_state_prob * starting_emission_prob, 2)))
    plus_path.append(("+", math.log(starting_state_prob * starting_emission_prob, 2)))

    for char_index in range(1, len(sequence)):
        # default assume A
        i = 0
        if sequence[char_index] == "C":
            i = 1
        elif sequence[char_index] == "G":
            i = 2
        elif sequence[char_index] == "T":
            i = 3

        # previous char index
        pci = 0
        if sequence[char_index - 1] == "C":
            pci = 1
        elif sequence[char_index - 1] == "G":
            pci = 2
        elif sequence[char_index - 1] == "T":
            pci = 3

        # calc max probability for minus path with log
        minus_to_minus_prob = minus_path[char_index - 1][1] + math.log(
            transitions[0][0] * minus_model[pci][
                i], 2)
        plus_to_minus_prob = plus_path[char_index - 1][1] + math.log(
            transitions[1][0] * plus_model[pci][i], 2)

        if minus_to_minus_prob >= plus_to_minus_prob:
            minus_path.append(("-", minus_to_minus_prob, 2))
        else:
            minus_path.append(("+", plus_to_minus_prob, 2))

        # calc max probability for plus path with log
        minus_to_plus_prob = minus_path[char_index - 1][1] + math.log(
            transitions[0][1] * minus_model[pci][
                i], 2)
        plus_to_plus_prob = plus_path[char_index - 1][1] + math.log(
            transitions[1][1] * plus_model[pci][
                i], 2)

        if plus_to_plus_prob >= minus_to_plus_prob:
            plus_path.append(("+", plus_to_plus_prob, 2))
        else:
            plus_path.append(("-", minus_to_plus_prob, 2))

    # get viterbi path with higher end probability
    if minus_path[-1] >= plus_path[-1]:
        viterbi_path = copy.deepcopy(minus_path)
    else:
        viterbi_path = copy.deepcopy(plus_path)

    for state in viterbi_path:
        viterbi_path_str += state[0]

    return viterbi_path_str


def calc_error_rate(seq1, seq2):
    """
    Calculate error rate between two strings.

    :param seq1: str
    :param seq2: str
    :return: float
    """
    similarity = 0
    if len(seq1) == len(seq2):
        for i in range(len(seq1)):
            if seq1[i] == seq2[i]:
                similarity += 1

        return 1 - (similarity / len(seq1))

    else:
        print("Strings need to have the same length.")


if __name__ == "__main__":
    # get data from hmm
    sequence, real_states = calc_hidden_markov_model()

    # order of values: ACGT
    minus_model_viterbi = [[0.300, 0.205, 0.285, 0.210],
                           [0.322, 0.298, 0.078, 0.302],
                           [0.177, 0.239, 0.292, 0.292],
                           [0.248, 0.246, 0.298, 0.208]]

    # order of values: ACGT
    plus_model_viterbi = [[0.180, 0.274, 0.426, 0.120],
                          [0.171, 0.368, 0.274, 0.188],
                          [0.079, 0.355, 0.384, 0.182],
                          [0.161, 0.339, 0.375, 0.125]]

    # order of values: minus, plus
    transitions = [[0.9, 0.1], [0.2, 0.8]]


    viterbi_path = calc_viterbi_path(sequence, minus_model_viterbi, plus_model_viterbi, transitions)
    print("Sequence: ", sequence)
    print("Real states: ", real_states)
    print("Viterbi path:", viterbi_path)

    print("Error rate: ", calc_error_rate(real_states, viterbi_path))

