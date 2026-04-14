# puzzle8.py
# ------------------------------------------
# Author: Michael Blaich
# Datum: 21.03.2025
# Beschreibung: Beispiele zum Lösen des 8-Puzzles.
# ------------------------------------------
from board import Board
from a_star import a_star
from idfs import idfs
from collections import deque

def print_board(board: list[int], step: int, total: int):
    """Gibt ein einzelnes Board als 3x3 Gitter aus."""
    print(f"  Schritt {step} / {total}\n")
    print("  ┌───┬───┬───┐")
    for row in range(3):
        cells = board[row * 3 : row * 3 + 3]
        print("  │ " + " │ ".join(str(c) for c in cells) + " │")
        if row < 2:
            print("  ├───┼───┼───┤")
    print("  └───┴───┴───┘")

def main():
    # Beispiel mit zufälligem lösbaren Board
    # board = Board()

    # Beispiel mit festem Board (wie im Aufgabenblatt)
    board = Board([7, 2, 4, 5, 0, 6, 8, 3, 1])
    #board = Board([1, 2, 0, 3, 4, 5, 6, 7, 8])

    print("Startzustand:", board)
    print("Lösbar (Parität)?", board.parity())
    if not board.parity():
        return
    print("Heuristik h1:", board.h1())
    print("Heuristik h2:", board.h2())

    # --- A* ---
    print("\n--- A* Suche ---")
    a_star_result = a_star(board)
    if a_star_result is None:
        print("Keine Lösung gefunden.")
    else:
        print(f"Züge: {len(a_star_result) - 1}")
        [print(step) for step in a_star_result]
        for i, b in enumerate(a_star_result):
            print_board(b.board, i, len(a_star_result) - 1)

    # --- IDFS ---
    print("\n--- IDFS Suche ---")
    idfs_result = idfs(board)
    if idfs_result is None:
        print("Keine Lösung gefunden.")
    else:
        print(f"Züge: {len(idfs_result) - 1}")
        [print(step) for step in idfs_result]
        for i, b in enumerate(idfs_result):
            print_board(b.board, i, len(idfs_result) - 1)


if __name__ == "__main__":
    main()


    """
    A1:
    a) Parität 6
    b) siehe board.py parity()

    A2:
    a) siehe board.py h1()
    b) siehe board.py h2()
    c) siehe board.py h2()
    d) siehe board.py h1() und h2()

    A3:
    a) siehe idfs.py und a_star.py
    b) Funktioniert? Bei ungerader Parität ist es halt nicht lösbar
    c) siehe Ausgabe
    d) Tiefensuche ist optimal, da wir iterativ vertiefen und jeder Zug die gleichen
    Kosten hat. Da wir immer erst alle Züge mit derselben Tiefe ausprobieren, probieren wir alle Züge mit
    den niedrigsten Kosten aus, bis wir zu zügen mit höheren Kosten gehen. Dafür muss der 
    Zustandsraum endlich sein.
    A* ist optimal, da die Heuristik die Vorraussetzung h(n)<= h*(n) erfüllt
    und monoton ist, also die Kosten der Heuristik die tatsächlichen Kosten nie überschreiten
    und die kosten eines zusätzlichen Zugs immer steigen (in der Heuristik und im Spiel).
    Auch hier muss der Zustandsraum endlich sein.
    e) Was für ein problem passiert bei 15-Puzzle? TODO
    """