def menu():
    print("AMBI Praktikum Aufgabe 1 von Alexander Schleiter & Tim Stadager")
    i = 0
    while i == 0:
        print("Als erstes bitte einen Text als Dateipfad angeben"
              "und dann den darin zu suchenden Pattern.")
        try:
            pattern = str(input(r"Text:    "))
            search_string = str(input(r"Pattern:  "))
            string_input(pattern, search_string)
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

            number = int(input())
            if number == 1:
                naive_string_matcher()
            if number == 2:
                rabin_karp_matcher()
            if number == 3:
                knuth()
            if number == 4:
                boyer_moore_matcher()
            if number == 5:
                exit()
            else:
                print("Die angegebene Zahl liegt nicht zwischen 1 und 5\n"
                      "Bitte versuchen Sie es erneut.")
        except ValueError:
            print("Geben Sie eine Zahl zwischen 1 und 5 ein.")


def string_input(pattern, search_string, ):
    t = " "
    s = " "
    pattern.replace("\"", "/")

    with open(pattern, "r", encoding="utf-8") as text:
        # content = text.read().replace("\n","")
        for i in text:
            if i[0] == ">":
                pass
            else:
                t += i  # \n muss noch aus t rausgenommen werden oder nicht?
        print(t)
    if "\"" in search_string:  # checks if the search_string is a path
        search_string.replace("\"", "/")
        with open(pattern, "r") as text:
            for i in text:
                if i[0] == ">":
                    pass
                else:
                    s += i
    else:
        s = search_string
    return t, s


def naive_string_matcher(t, p):
    n = len(t)
    m = len(p)

    shifts = []

    for s in range(0, n - m + 1):
        if p == t[s:s + m]:
            shifts.append(s)
            print("Pattern occurs with shift", s)

    return shifts


def rabin_karp_matcher(T, P, d=144697, q=1000000009):
    n = len(T)
    m = len(P)
    h = pow(d, m - 1) % q
    p = 0
    t = 0

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


def knuth():
    pass


def compute_prefix(P):
    m = len(P)
    # initialize list of length m
    pi = [0] * m
    k = 0

    for q in range(2, m):
        while k > 0 and P[k + 1] != P[q]:
            k = pi[k]

        if P[k + 1] == P[q]:
            k = k + 1
        pi[q] = k

    return pi


def boyer_moore_matcher(T, P, sigma):
    n = len(T)
    m = len(P)
    lambd = compute_last_occurrence(P, m, sigma)
    gamma = compute_good_suffix(P, m)
    o = 0
    s = o

    while s <= n - m:
        j = m
        while j > o and P[j] == T[s + j]:
            j = j - 1
            if j == o:
                print("Pattern occurs with shift ", s)
                s = s + gamma[o]
            else:
                s = s + max(gamma[j], j - lambd[T[s + j]])


def compute_last_occurrence(P, m, sigma):
    lambd = []

    for char in sigma:
        lambd.append(0)

    for j in range(m):
        lambd[P[j]] = j

    return lambd


def compute_good_suffix(P, m):
    pi = compute_prefix(P)
    P1 = reversed(P)
    pi1 = compute_prefix(P1)
    gamma = [0] * m

    for j in range(m):
        gamma[j] = m - pi[m]
    for l in range(m):
        j = m - pi1[l]
        if gamma[j] > l - pi1[l]:
            gamma[j] = l - pi1[l]

    return gamma


if __name__ == "__main__":
    rabin_karp_matcher("jengdjensjen", "jen")
    unicode_char_list = [chr(x) for x in range(255)]
    print(unicode_char_list)
    boyer_moore_matcher("jengdjensjen", "jen", unicode_char_list)
    # menu()
