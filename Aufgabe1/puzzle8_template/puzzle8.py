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