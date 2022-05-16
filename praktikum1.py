import time
def menu():
    print("AMBI Praktikum Aufgabe 1 von Alexander Schleiter & Tim Stadager")
    i = 0
    while i == 0:
        print("Als erstes bitte einen Text als Dateipfad angeben"
              "und dann den darin zu suchenden Pattern.")
        try:
            pattern = str(input(r"Text:    "))
            search_string = str(input(r"Pattern:  "))
            t,p = string_input(pattern, search_string)
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
                start = time.process_time()
                steps = naive_string_matcher(t, p)
                end = time.process_time()
                print("Zeit: {5.3f}s".format(end-start))
                print("Anzahl der Verlgeiche:   ", steps)
            if number == 2:
                start = time.process_time()
                steps = rabin_karp_matcher(t, p,)
                end = time.process_time()
                print("Zeit: {5.3f}s".format(end - start))
                print("Anzahl der Verlgeiche:   ", steps)
            if number == 3:
                start = time.process_time()
                knuth_morris_pratt(t, p)
                end = time.process_time()
                print("Zeit: {5.3f}s".format(end - start))
                print("Anzahl der Verlgeiche:   ", steps)
            if number == 4:
                start = time.process_time()
                boyer_moore_matcher(t, p, char_list)
                end = time.process_time()
                print("Zeit: {5.3f}s".format(end - start))
                print("Anzahl der Verlgeiche:   ", steps)
            if number == 5:
                exit()
            else:
                print("Die angegebene Zahl liegt nicht zwischen 1 und 5\n"
                      "Bitte versuchen Sie es erneut.")
        except ValueError:
            print("Geben Sie eine Zahl zwischen 1 und 5 ein.")


def string_input(data, pattern ):
    t = " " #text
    p = " " #pattern
    data.replace("\"", "/")

    with open(data, "r", encoding="utf-8") as text:
        # content = text.read().replace("\n","")
        for i in text:
            if i[0] == ">":
                pass
            else:
                t += i  # \n muss noch aus t rausgenommen werden oder nicht?
        print(t)
    if "\"" in pattern:  # checks if the search_string is a path
        pattern.replace("\"", "/")
        with open(pattern, "r", encoding="utf-8") as text:
            for i in text:
                if i[0] == ">":
                    pass
                else:
                    p += i
    else:
        p = pattern
    return t, p


def naive_string_matcher(t, p):
    n = len(t)
    m = len(p)
    steps = 0

    shifts = []

    for s in range(0, n - m + 1):
        steps += 1
        if p == t[s:s + m]:
            shifts.append(s)
            print("Pattern occurs with shift", s)
    return steps


def rabin_karp_matcher(T, P, d=144697, q=1000000009):
    n = len(T)
    m = len(P)
    h = pow(d, m - 1) % q
    p = 0
    t = 0
    steps = 0
    for i in range(0, m):
        p = (d * p + ord(u"{}".format(P[i]))) % q
        t = (d * t + ord(u"{}".format(T[i]))) % q

    for s in range(0, n - m + 1):
        if p == t:
            if P[0:m] == T[s: s + m]:

                print("Pattern occurs with shift", s)

        if s < (n - m):
            t = (ord(u"{}".format(T[s + m])) + d * (t - ord(u"{}".format(T[s])) * h)) % q

            if t < 0:
                t = t + q


def knuth_morris_pratt(T, P):
    steps = 0
    n = len(T)
    m = len(P)
    pi, steps = compute_prefix(P, steps)
    q = 0

    for i in range(n):
        steps += 1
        while q > 0 and P[q] != T[i]:
            q = pi[q]
        if P[q] == T[i]:
            q = q + 1

        if q == m:
            print("Pattern occurs with shift", i - m + 1)
            q = pi[q-1]
    return steps

def compute_prefix(P, steps):
    m = len(P)
    # initialize list of length m
    pi = [0] * m
    k = 0

    for q in range(2, m):
        steps += 1
        while k > 0 and P[k + 1] != P[q]:
            k = pi[k]

        if P[k + 1] == P[q]:
            k = k + 1
        pi[q] = k

    return pi,steps


def boyer_moore_matcher(T, P, sigma):
    steps = 0
    n = len(T)
    m = len(P)
    lambd = compute_last_occurrence(P, m, sigma)
    gamma,steps = compute_good_suffix(P, m, steps)
    o = 0
    s = o

    while s <= n - m:
        j = m - 1
        steps += 1
        while j > o and P[j] == T[s + j]:
            j = j - 1
        steps += 1
        if j == o:
            print("Pattern occurs with shift ", s)
            s = s + gamma[o]
        else:
            s = s + max(gamma[j], j - lambd[ord(T[s + j])])
    return steps

def compute_last_occurrence(P, m, sigma):
    lambd = []

    for char in sigma:
        lambd.append(0)

    # add numeric value of every char to a list
    for j in range(m):
        lambd[ord(P[j])] = j

    return lambd


def compute_good_suffix(P, m, steps):
    pi,steps = compute_prefix(P,steps)
    P1 = P[::-1]
    pi1,steps = compute_prefix(P1, steps)
    gamma = [0] * m

    for j in range(m):
        gamma[j] = m - pi[m - 1]
    for l in range(m):
        j = m - pi1[l]
        steps += 1
        if gamma[j - 1] > (l - pi1[l]):
            gamma[j - 1] = l - pi1[l]

    return gamma,steps


if __name__ == "__main__":
    print("Rabin Karp:")
    rabin_karp_matcher("jengdjensjen", "jen")
    print("KMP:")
    knuth_morris_pratt("jengdjensjen", "jen")
    print("Booyer Moore:")
    char_list = [chr(x) for x in range(144697)]
    boyer_moore_matcher("jengdjensjen", "jen", char_list)
    # menu()
