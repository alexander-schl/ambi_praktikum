import time
import os


def menu():
    print("AMBI Praktikum Aufgabe 1 von Alexander Schleiter & Tim Stadager")
    i = 0
    while i == 0:
        print("Als erstes bitte einen Text als Dateipfad angeben "
              "und dann den darin zu suchenden Pattern.")
        try:
            pattern = str(input(r"Text:    "))
            search_string = str(input(r"Pattern:  "))
            t, p = string_input(pattern, search_string)
        except TypeError:
            print("Das Pattern konnte nicht gefunden werden.")
            continue
        except FileNotFoundError:
            print("Der Eingegebene Pfad ist nicht vorhanden.")
            continue
        print("Für die verschiedenen Algorithmen drücken Sie die 1-5:")
        print("1. Naiver Pattern Matcher\n"
              "2. Rabin-Karp\n"
              "3. Knuth-Morris-Pratt\n"
              "4. Boyer-Moore\n"
              "5. Exit\n"
              )
        try:
            char_list = [chr(x) for x in range(144697)]
            number = int(input())
            if number == 1:
                start = time.time()
                steps = naive_string_matcher(t, p)
                end = time.time()
                print("Zeit:", (end - start))
                print("Anzahl der Verlgeiche:   ", steps)
            elif number == 2:
                start = time.time()
                steps = rabin_karp_matcher(t, p, )
                end = time.time()
                print("Zeit:", (end - start))
                print("Anzahl der Verlgeiche:   ", steps)
            elif number == 3:
                start = time.time()
                steps = knuth_morris_pratt(t, p)
                end = time.time()
                print("Zeit:", (end - start))
                print("Anzahl der Verlgeiche:   ", steps)
            elif number == 4:
                start = time.time()
                steps = boyer_moore_matcher(t, p, char_list)
                end = time.time()
                print("Zeit:", (end - start))
                print("Anzahl der Verlgeiche:   ", steps)
            elif number == 5:
                exit()
            else:
                print("Die angegebene Zahl liegt nicht zwischen 1 und 5\n"
                      "Bitte versuchen Sie es erneut.")
        except ValueError:
            print("Geben Sie eine Zahl zwischen 1 und 5 ein.")


def string_input(data, pattern):
    t = ""  # text
    p = ""  # pattern

    path = os.path.abspath(data)

    with open(path, "r", encoding="utf-8") as text:
        for i in text:
            if i[0] == ">":
                pass
            else:
                str = i.replace("\n", "")
                t += str
    if os.path.isfile(pattern):  # checks if the search_string is a file
        with open(pattern, "r", encoding="utf-8") as text:
            for i in text:
                if i[0] == ">":
                    pass
                else:
                    str = i.replace("\n", "")
                    p += str
    else:
        p = pattern
    return t, p


def naive_string_matcher(t, p):
    n = len(t)
    m = len(p)
    steps = 0
    number_of_occurrences = 0

    for s in range(0, n - m + 1):
        steps += 1
        for i in range(len(p)):
            steps += 1
            if p[i] == t[s + i]:
                if i + 1 == m:
                    print("Pattern occurs with shift", s)
                    number_of_occurrences += 1
            else:
                break
    print(f"Pattern occurs {number_of_occurrences} times.")
    return steps


# d is number of unicode characters
def rabin_karp_matcher(T, P, d=144697, q=1000000009):
    n = len(T)
    m = len(P)
    h = pow(d, m - 1) % q
    p = 0
    t = 0
    steps = 0
    number_of_occurrences = 0

    for i in range(0, m):
        p = (d * p + ord(u"{}".format(P[i]))) % q
        t = (d * t + ord(u"{}".format(T[i]))) % q

    for s in range(0, n - m + 1):
        steps += 1
        if p == t:
            # if P[0:m] == T[s: s + m]:
            # check character for character
            for i in range(m):
                steps += 1
                if T[s + i] != P[i]:
                    break
                else:
                    i += 1

            if i == m:
                print("Pattern occurs with shift", s)
                number_of_occurrences += 1

        if s < (n - m):
            t = (ord(u"{}".format(T[s + m])) + d * (t - ord(u"{}".format(T[s])) * h)) % q

            if t < 0:
                t = t + q

    print(f"Pattern occurs {number_of_occurrences} times.")
    return steps


def knuth_morris_pratt(T, P):
    steps = 0
    n = len(T)
    m = len(P)
    pi = compute_prefix(P)
    q = 0
    number_of_occurrences = 0

    for i in range(n):
        steps += 1

        while q > 0 and P[q] != T[i]:
            q = pi[q - 1]

        if P[q] == T[i]:
            q = q + 1

        if q == m:
            print("Pattern occurs with shift", i - m + 1)
            number_of_occurrences += 1
            q = pi[q - 1]

    print(f"Pattern occurs {number_of_occurrences} times.")
    return steps


def compute_prefix(P):
    m = len(P)
    # initialize list of length m
    pi = [-1]
    k = -1

    for q in range(0, m):
        while k >= 0 and P[k] != P[q]:
            k = pi[k]

        k = k + 1
        pi.append(k)

    pi.pop(0)
    return pi


def boyer_moore_matcher(T, P, sigma):
    steps = 0
    n = len(T)
    m = len(P)
    lambd = compute_last_occurrence(P, m, sigma)
    gamma = compute_good_suffix(P, m)
    s = 0
    number_of_occurrences = 0

    while s <= n - m:
        steps += 1
        j = m - 1
        while j >= 0 and P[j] == T[s + j]:
            j = j - 1
            steps += 1

        if j < 0:
            print("Pattern occurs with shift ", s)
            number_of_occurrences += 1
            s = s + gamma[0]
        else:
            s = s + max(gamma[j], j - lambd[ord(T[s + j])])

    print(f"Pattern occurs {number_of_occurrences} times.")
    return steps


def compute_last_occurrence(P, m, sigma):
    lambd = []

    for char in sigma:
        lambd.append(0)

    # add numeric value of every char to a list
    for j in range(m):
        lambd[ord(P[j])] = j

    return lambd


def compute_good_suffix(P, m):
    pi = compute_prefix(P)
    P1 = P[::-1]
    pi1 = compute_prefix(P1)
    gamma = [0] * m

    for j in range(m):
        gamma[j] = m - pi[m - 1]
    for l in range(m):
        j = m - pi1[l]
        if gamma[j - 1] > (l - pi1[l]):
            gamma[j - 1] = l - pi1[l]

    return gamma


if __name__ == "__main__":
    menu()
