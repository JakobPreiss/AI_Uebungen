from constraint import Problem

from constraint import Problem

def solve_packing(W: int, H: int, rectangles: list[tuple[int, int]]):
    """
    W, H       : Dimensionen des großen Rechtecks
    rectangles : Liste von (w, h) für jedes kleine Rechteck
    """
    problem = Problem()
    N = len(rectangles)

    # ── 1. Variablen & Domänen ────────────────────────────────────────────────
    for i, (w, h) in enumerate(rectangles):
        max_x = W - min(w, h)   # engste Schranke über beide Orientierungen
        max_y = H - min(w, h)
        problem.addVariable(f"x_{i}", range(max_x + 1))
        problem.addVariable(f"y_{i}", range(max_y + 1))
        # Orientierung nur wenn sinnvoll (quadratisch → nur 1 Wert nötig)
        problem.addVariable(f"o_{i}", [0] if w == h else [0, 1])

    # ── 2. Randbedingung: Rechteck i bleibt im großen Rechteck ───────────────
    for i, (w, h) in enumerate(rectangles):
        def boundary(x, y, o, w=w, h=h, W=W, H=H):
            aw, ah = (w, h) if o == 0 else (h, w)   # actual width / height
            return x + aw <= W and y + ah <= H

        problem.addConstraint(boundary, [f"x_{i}", f"y_{i}", f"o_{i}"])

    # ── 3. Überschneidungsfreiheit: alle Paare (i, j) ────────────────────────
    for i in range(N):
        for j in range(i + 1, N):
            wi, hi = rectangles[i]
            wj, hj = rectangles[j]

            def no_overlap(xi, yi, oi, xj, yj, oj,
                           wi=wi, hi=hi, wj=wj, hj=hj):
                # Effektive Maße je nach Orientierung
                awi, ahi = (wi, hi) if oi == 0 else (hi, wi)
                awj, ahj = (wj, hj) if oj == 0 else (hj, wj)

                return (
                    xi + awi <= xj or   # i vollständig links von j
                    xj + awj <= xi or   # j vollständig links von i
                    yi + ahi <= yj or   # i vollständig oberhalb von j
                    yj + ahj <= yi      # j vollständig oberhalb von i
                )

            problem.addConstraint(
                no_overlap,
                [f"x_{i}", f"y_{i}", f"o_{i}", f"x_{j}", f"y_{j}", f"o_{j}"]
            )

    return problem.getSolution()


# ── Beispiel ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    W, H = 7, 8
    rects = [(6, 4), (5, 2), (3, 2), (2, 2), (8, 1), (4, 1)]   #Rechtecke

    solution = solve_packing(W, H, rects)

    if solution:
        for i, (w, h) in enumerate(rects):
            x, y, o = solution[f"x_{i}"], solution[f"y_{i}"], solution[f"o_{i}"]
            aw, ah = (w, h) if o == 0 else (h, w)
            print(f"Rechteck {i} ({aw}×{ah}): Ecke ({x},{y})")
    else:
        print("Keine Lösung gefunden.")

"""
def solve():
    problem = Problem()
    #6x4
    for i in range (1, 7):
        for j in range(1, 5):
            problem.addVariable(f"A{i}{j}", range(0, 55))

    #5x2
    for i in range (1, 6):
        for j in range(1, 3):
            problem.addVariable(f"B{i}{j}", range(0, 55))

    #2x2
    for i in range (1, 3):
        for j in range(1, 3):
            problem.addVariable(f"C{i}{j}", range(0, 55))

    #3x2
    for i in range (1, 4):
        for j in range(1, 3):
            problem.addVariable(f"D{i}{j}", range(0, 55))

    #8x1
    for i in range (1, 9):
        problem.addVariable(f"E{i}", range(0, 55))

    #4x1
    for i in range (1, 5):
        problem.addVariable(f"F{i}", range(0, 55))


    #6x4
    for j in range (1, 5):
        for i in range(1, 6):
            problem.addConstraint(right_or_under, (f"A{i}{j}", f"A{i+1}{j}"))
    for i in range (1, 7):
        for j in range(1, 4):
            problem.addConstraint(under_or_left, ((f"A{i}{j}", f"A{i}{j + 1}")))

    #5x2
    for j in range (1, 3):
        for i in range(1, 5):
            problem.addConstraint(right_or_under, (f"B{i}{j}", f"B{i+1}{j}"))
    for i in range (1, 6):
        j = 1
        problem.addConstraint(under_or_left, ((f"B{i}{j}", f"B{i}{j + 1}")))

    #3x2
    for j in range (1, 3):
        for i in range(1, 3):
            problem.addConstraint(right_or_under, (f"D{i}{j}", f"D{i+1}{j}"))
    for i in range (1, 3):
        j = 1
        problem.addConstraint(under_or_left, ((f"D{i}{j}", f"D{i}{j + 1}")))

    #2x2
    for j in range (1, 3):
        i = 1
        problem.addConstraint(right_or_under, (f"C{i}{j}", f"C{i+1}{j}"))
    for i in range (1, 3):
        j = 1
        problem.addConstraint(under_or_left, ((f"C{i}{j}", f"C{i}{j + 1}")))

    #8x1
    for i in range (1, 8):
        problem.addConstraint(right_or_under, (f"E{i}", f"E{i+1}"))

    # 8x1
    for i in range(1, 4):
        problem.addConstraint(right_or_under, (f"F{i}", f"F{i + 1}"))

    solutions = problem.getSolutions()
    return solutions

def right_or_under(z1, z2):
    return z1 + 1 == z2 or z1 + 7 == z2

def under_or_left(z1, z2):
    return z1 - 1 == z2 or z1 + 7 == z2


def solve():
    problem = Problem()

    problem.addVariables(range(1,57), ["6x4", "8x1", "4x1", "5x2", "2x2", "3x2"])

    #8x1
    problem.addConstraint(check8x1, range(1, 57))

    #4x1
    problem.addConstraint(check4x1, range(1, 57))

    #5x2
    problem.addConstraint(check5x2, range(1, 57))

    #2x2
    problem.addConstraint(check2x2, range(1, 57))

    #3x2
    problem.addConstraint(check3x2, range(1, 57))

    #6x4
    problem.addConstraint(check6x4, range(1, 57))

    #Menge der Zuweisungen passt checken
    problem.addConstraint(checkQuantity, range(1, 57))

    solutions = problem.getSolutions()
    return solutions

def check8x1(*variables):
    for i in range(1, 57):
        variable = variables[i - 1]
        if variable == "8x1":
            column = i % 7
            for row in range(1, 8):
                if variables[row * 7 + column] != "8x1":
                    return False
    return True

def check4x1(*variables):
    for i in range(1, 57):
        variable = variables[i - 1]
        if variable == "4x1":
            result = check_directions(variables, i - 1, 4, 1, "4x1")
            if not result:
                return False

    return True


def check5x2(*variables):
    for i in range(1, 57):
        variable = variables[i - 1]
        if variable == "5x2":
            result = check_directions(variables, i - 1, 5, 2, "5x2")
            if not result:
                return False

    return True

def check2x2(*variables):
    for i in range(1, 57):
        variable = variables[i - 1]
        if variable == "2x2":
            result = check_directions(variables, i - 1, 2, 2, "2x2")
            if not result:
                return False

    return True

def check3x2(*variables):
    for i in range(1, 57):
        variable = variables[i - 1]
        if variable == "5x2":
            result = check_directions(variables, i - 1, 3, 2, "3x2")
            if not result:
                return False

    return True

def check6x4(*variables):
    for i in range(1, 57):
        variable = variables[i - 1]
        if variable == "6x4":
            result = check_directions(variables, i - 1, 6, 4, "5x2")
            if not result:
                return False

    return True

def checkQuantity(*variables):
    counter6x4 = 0
    counter5x2 = 0
    counter3x2 = 0
    counter2x2 = 0
    counter4x1 = 0
    counter8x1 = 0
    for i in range(1, 57):
        variable = variables[i - 1]
        if variable == "6x4":
            counter6x4 += 1
            continue
        if variable == "5x2":
            counter5x2 += 1
            continue
        if variable == "3x2":
            counter3x2 += 1
            continue
        if variable == "2x2":
            counter2x2 += 1
            continue
        if variable == "4x1":
            counter4x1 += 1
            continue
        if variable == "8x1":
            counter8x1 += 1
            continue
        return False

    return counter6x4 == 24 and counter5x2 == 10 and counter3x2 == 6 and counter2x2 == 4 and counter4x1 == 4 and counter8x1 == 8

def check_directions(variables, i, firstSide, secondSide, value):
    boxes = 1
    expected_boxes = firstSide + secondSide - 1
    # move left
    j = i - 1
    while j > (i - (i % 7)) and variables[j] == value:
        boxes += 1
        j -= 1
    if boxes == expected_boxes:
        return True
    # move right
    j = i + 1
    while j < ((i - (i % 7)) + 7) and variables[j] == value:
        boxes += 1
        j += 1
    if boxes == expected_boxes:
        return True

    # move up
    j = i - 7
    while j >= 0 and variables[j] == value:
        boxes += 1
        j = j - 7
    if boxes == expected_boxes:
        return True

    # move down
    j = i + 7
    while j < len(variables) and variables[j] == value:
        boxes += 1
        j = j + 7
    if boxes == expected_boxes:
        return True

    return False

def showSolution(solution):
    for i in range(0, 8):
        for j in range(0, 7):
            print(solution[i][j], end=" ")
        print()
def main():
    solutions = solve()
    if solutions is None:
        print("No solutions")
        return
    print("Found %d solution(s)!" % len(solutions))
    print("")
    for solution in solutions:
        showSolution(solution)


if __name__ == "__main__":
    main()
    """