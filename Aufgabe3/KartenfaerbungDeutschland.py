from constraint import Problem

bundeslaender = [
    "BWU",  # baden-Württemberg
    "BYN",  # Bayern
    "BER",  # Berlin
    "BRB",  # Brandenburg
    "BRE",  # Bremen
    "HAM",  # Hamburg
    "HES",  # Hessen
    "MVP",  # Mecklenburg-Vorpommern
    "NDS",  # Niedersachsen
    "NRW",  # Nordrhein-westfalen
    "RLP",  # Rheinland-Pfalz
    "SAR",  # Saarland
    "SAX",  # Sachen
    "SAA",  # Sachsen-Anhalt
    "SHL",  # Schleswig-Holstein
    "THU"  # Thüringen
]

def solve():
    problem = Problem()

    problem.addVariables(bundeslaender, ["rot", "blau", "grün", "gelb"])

    #BWU
    problem.addConstraint(diffenent_from, ["BWU"] + ["BYN", "RLP", "HES"])

    #BAYERN
    problem.addConstraint(diffenent_from, ["BYN"] + ["BWU", "HES", "THU", "SAX"])

    #SAARLAND
    problem.addConstraint(diffenent_from, ["SAR"] + ["RLP"])

    # RHEINLAND-PFALZ
    problem.addConstraint(diffenent_from, ["RLP"] + ["BWU", "HES", "NRW", "SAR"])

    # HESSEN
    problem.addConstraint(diffenent_from, ["HES"] + ["NRW", "RLP", "BWU", "BYN", "THU", "NDS"])

    # NORDRHEIN-WESTFALEN
    problem.addConstraint(diffenent_from, ["NRW"] + ["NDS", "HES", "RLP"])

    # NIEDERSACHSEN
    problem.addConstraint(diffenent_from, ["NDS"] + ["SHL", "HAM", "BRE", "NRW", "HES", "THU", "SAA", "BRB", "MVP"])

    # SCHLESWIG-HOLSTEIN
    problem.addConstraint(diffenent_from, ["SHL"] + ["NDS", "HAM", "MVP"])

    # HAMBURG
    problem.addConstraint(diffenent_from, ["HAM"] + ["SHL", "NDS"])

    # BREMEN
    problem.addConstraint(diffenent_from, ["BRE"] + ["NDS"])

    # BRANDENBURG
    problem.addConstraint(diffenent_from, ["BRB"] + ["MVP", "NDS", "SAA", "SAX", "BER"])

    # BERLIN
    problem.addConstraint(diffenent_from, ["BER"] + ["BRB"])

    # MECKLENBURG-VORPOMMERN
    problem.addConstraint(diffenent_from, ["MVP"] + ["SHL", "NDS", "BRB"])

    # SACHSEN-ANHALT
    problem.addConstraint(diffenent_from, ["SAA"] + ["NDS", "BRB", "SAX", "THU"])

    # SACHSEN
    problem.addConstraint(diffenent_from, ["SAX"] + ["BRB", "SAA", "THU", "BYN"])

    # THÜRINGEN
    problem.addConstraint(diffenent_from, ["THU"] + ["HES", "BYN", "SAX", "SAA", "NDS"])

    solutions = problem.getSolutions()
    return solutions


def diffenent_from(land, *otherlands):
    return all(land != o for o in otherlands)


def main():
    solutions = solve()
    if solutions is None:
        print("No solutions")
        return
    print("Found %d solution(s)!" % len(solutions))
    print("")
    for solution in solutions:
        print(solution)


if __name__ == "__main__":
    main()