import copy

def menu():
    pass


def calc_hidden_markov_model():
    pass


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

    # 1/2 because of two states
    starting_state_prob = 1 / 2
    # 1/4 because of ACGT
    starting_emission_prob = 1 / 4

    minus_path.append(("-", starting_state_prob * starting_emission_prob))
    plus_path.append(("+", starting_state_prob * starting_emission_prob))

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

        # calc max probability for minus path
        minus_to_minus_prob = minus_path[char_index - 1][1] * transitions[0][0] * minus_model[pci][i]
        plus_to_minus_prob = plus_path[char_index - 1][1] * transitions[1][0] * plus_model[pci][i]

        if minus_to_minus_prob >= plus_to_minus_prob:
            minus_path.append(("-", minus_to_minus_prob))
        else:
            minus_path.append(("+", plus_to_minus_prob))


        # calc max probability for plus path
        minus_to_plus_prob = minus_path[char_index - 1][1] * transitions[0][1] * minus_model[pci][i]
        plus_to_plus_prob = plus_path[char_index - 1][1] * transitions[1][1] * plus_model[pci][i]

        if plus_to_plus_prob >= minus_to_plus_prob:
            plus_path.append(("+", plus_to_plus_prob))
        else:
            plus_path.append(("-", minus_to_plus_prob))


    print(minus_path)
    print(plus_path)

    # get viterbi path with higher end probability
    if minus_path[-1] >= plus_path[-1]:
        viterbi_path = copy.deepcopy(minus_path)
    else:
        viterbi_path = copy.deepcopy(plus_path)

    viterbi_path_str = ""
    for state in viterbi_path:
        viterbi_path_str += state[0]

    return viterbi_path_str

if __name__ == "__main__":
    # order of values: ACGT
    minus_model = [[0.300, 0.205, 0.285, 0.210],
                   [0.322, 0.298, 0.078, 0.302],
                   [0.177, 0.239, 0.292, 0.292],
                   [0.248, 0.246, 0.298, 0.208]]

    # order of values: ACGT
    plus_model = [[0.180, 0.274, 0.426, 0.120],
                  [0.171, 0.368, 0.274, 0.188],
                  [0.079, 0.355, 0.384, 0.182],
                  [0.161, 0.339, 0.375, 0.125]]

    # order of values: minus, plus
    transitions = [[0.9, 0.1], [0.2, 0.8]]

    sequence = "GCGGGCGTAGCTCAGAGGTAGAGCACCTGCTTCCCAAGCAGGAGGTCGCCGGTTCGAGTC"

    print("Viterbi path:", calc_viterbi_path(sequence, minus_model, plus_model, transitions))

    # menu()
