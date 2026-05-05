from constraint import Problem, AllDifferentConstraint

def solve():
    problem = Problem()
    for i in range(1, 5):
        problem.addVariable("lehrer%d" % i, ["Maier", "Mueller", "Huber", "Schmid"])
        problem.addVariable("fach%d" % i, ["Deutsch", "Englisch", "Mathe", "Physik"])

    #leher und fächer gibts nicht doppelt
    problem.addConstraint(AllDifferentConstraint(), ["lehrer%d" % i for i in range(1, 5)])
    problem.addConstraint(AllDifferentConstraint(), ["fach%d" % i for i in range(1, 5)])

    #Herr Maier prüft nie in Raum 4
    problem.addConstraint(lambda lehrer4: lehrer4 != "Maier", ("lehrer4",))

    #Physik wird immer in Raum 4 geprüft
    problem.addConstraint(lambda fach4: fach4 == "Physik", ("fach4",))

    #Deutsch und Englisch werden nicht in Raum 1 geprüft
    problem.addConstraint(lambda fach1: fach1 != "Deutsch" and fach1 != "Englisch", ("fach1",))


    for i in range(1, 5):
        #Herr Müller prüft immer Deutsch
        problem.addConstraint(lambda lehrer, fach: (lehrer == "Mueller" and fach == "Deutsch")
                                or (lehrer != "Mueller" and fach != "Deutsch"),
                              ("lehrer%d" % i, "fach%d" % i))

        #Frau Huber prüft Mathematik
        problem.addConstraint(lambda lehrer, fach: (lehrer == "Huber" and fach == "Mathe")
                          or (lehrer != "Huber" and fach != "Mathe"),
                              ("lehrer%d" % i, "fach%d" % i))

    for i in range(1, 4):
        #Herr Schmid und Herr Müller prüfen nicht in benachbarten Räumen
        problem.addConstraint(lambda lehrerLinks, lehrerRechts: (lehrerLinks != "Schmid" and lehrerLinks != "Mueller") or
                                                                ((lehrerLinks == "Schmid" and lehrerRechts != "Mueller")
                                                                or (lehrerLinks == "Mueller" and lehrerRechts != "Schmid")),
                                ("lehrer%d" % i, "lehrer%d" % (i + 1)))

    solutions = problem.getSolutions()
    return solutions

def showSolution(solution):
    for i in range(1, 5):
        print(f"In Raum {i} prüft " + solution["lehrer%d" % i] + " " + solution["fach%d" % i])

def main():
    solutions = solve()
    print("Found %d solution(s)!" % len(solutions))
    print("")
    for solution in solutions:
        showSolution(solution)


if __name__ == "__main__":
    main()