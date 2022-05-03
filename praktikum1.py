def menu():
    print("AMBI Praktikum Aufgabe 1 von Alexander Schleiter & Tim Stadager")
    i = 0
    while i == 0:
        print("Als erstes bitte ein Pattern als Datei pfad angeben"
              "und dann den darin zu suchenden String")
        try:
            pattern = str(input(r"Pattern:    "))
            search_string = str(input(r"String:  "))
            string_input(pattern, search_string)
        except TypeError:
            print("Das Pattern konnte nicht gefunden werden.")
            continue
        except FileNotFoundError:
            print("Der Eingegebene Pfad ist nicht vorhanden.")
            continue
        print("Für die Verschiedenen Algorithmen drücken sie die 1-5")
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
                boyer()
            if number == 5:
                exit()
            else:
                print("Die Angegebene Zahl liegt nicht zwischen 1 und 5\n"
                      "Bitte versuchen sie es erneut")
        except ValueError:
            print("Geben sie eine Zahl zwischen 1 und 5 ein")


def string_input(pattern, search_string, ):
    t = " "
    s = " "
    pattern.replace("\"", "/")

    with open(pattern, "r") as text:
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


def rabin_karp_matcher(T, P, d=144697, q=999999999989):
    n = len(T)
    m = len(P)
    h = d ^ (m - 1) % q
    p = 0
    t0 = 0

    for i in range(0, m+1):
        p = (d*p+P[i]) % q
        t0 = (d*t0 + T[i]) % q

def knuth():
    pass


def boyer():
    pass


if __name__ == "__main__":
    naive_string_matcher("gdjensjen", "jen")
    # menu()
