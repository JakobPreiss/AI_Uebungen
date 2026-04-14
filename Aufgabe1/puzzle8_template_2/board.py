
# board.py
# ------------------------------------------
# Author: Michael Blaich
# Datum: 21.03.2025
# Beschreibung: Implementierung der Board-Klasse für das 8-Puzzle-Problem.
# ------------------------------------------
import random


class Board:
    """
    Repräsentiert ein 8-Puzzle-Board.

    Methoden:
    - parity(): Prüft, ob das Puzzle lösbar ist.
    - h1(), h2(): Platzhalter für Heuristikfunktionen.
    - possible_actions(): Liefert gültige Nachfolgezustände.
    - is_solved(): Prüft, ob das Ziel erreicht ist.
    """

    N = 8  # Problemgröße

    def __init__(self, board=None):
        """
        Initialisiert das Board.
        Wenn kein Board übergeben wird, wird ein zufälliges, lösbares Board
        erzeugt.
        """
        if board:
            self.board = list(board)
        else:
            self.board = list(range(Board.N + 1))
            while True:
                random.shuffle(self.board)
                if self.parity():
                    break

    def __str__(self):
        """
        Gibt das Board als String aus.
        """
        return f"Puzzle{{board={self.board}}}"

    def __eq__(self, other):
        """
        Zwei Boards sind gleich, wenn ihr Zustand gleich ist.
        """
        return isinstance(other, Board) and self.board == other.board

    def __hash__(self):
        """
        Ermöglicht das Nutzen von Board in Sets oder als Dictionary-Keys.
        """
        return hash(tuple(self.board))

    def parity(self):
        """
        Paritätsprüfung:
        Gibt True zurück, wenn das Board lösbar ist.
        TODO: Implementiere die Berechnung der Parität
        """

        parity_num = 0
        board_array = [x for x in self.board if x != 0]

        for y in range(len(board_array)):
            for x in range(y + 1, len(board_array)): 
                if board_array[x] < board_array[y]:
                    parity_num += 1
                    # print("(" + str(board_array[x]) + "," + str(board_array[y]) + "), ")

        return parity_num % 2 == 0

    def h1(self):
        """
        Heuristikfunktion h1 (siehe Aufgabenstellung).
        TODO: Implementiere einfache Heuristik
        """

        wrong_pos_count = 0

        for index, val in enumerate(self.board):
            if val != 0 and val != index:
                wrong_pos_count += 1

        return wrong_pos_count 

    def h2(self):
        """
        Heuristikfunktion h2 (siehe Aufgabenstellung).
        TODO: Implementiere verbesserte Heuristik
        """

        manhattan_distance = 0

        for i, val in enumerate(self.board):
            if val == 0:
                continue
            x_diff = abs((i % 3) - (val % 3))
            y_diff = abs((i // 3) - (val // 3))

            manhattan_distance += (x_diff + y_diff)

        return manhattan_distance

    def possible_actions(self):
        """
        Gibt eine Liste aller möglichen Folge-Boards zurück,
        die durch einen gültigen Zug entstehen.
        """
        zero_pos = self.board.index(0)
        neighbors = []
        if zero_pos - 3 >= 0:
            neighbors.append(zero_pos - 3)
        if zero_pos + 3 <= 8:
            neighbors.append(zero_pos + 3)
        if zero_pos % 3 != 0:
            neighbors.append(zero_pos - 1)
        if zero_pos % 3 != 2:
            neighbors.append(zero_pos + 1)

        result = []
        for i in neighbors:
            new_board = self.board.copy()
            new_board[zero_pos], new_board[i] = new_board[i], new_board[zero_pos]
            result.append(Board(new_board))
        return result

    def is_solved(self):
        """
        Prüft, ob das Board im Zielzustand ist (0,1,2,3,...,8).
        TODO: Implementiere die Prüfung ob das Board gelöst ist.
        """
        return self.board == list(range(Board.N + 1))


def main():
    b = Board([7, 2, 4, 5, 0, 6, 8, 3, 1])  # Startzustand manuell setzen
    # b = Board()  # Lösbares Puzzle zufällig generieren
    #b = Board([0, 1, 4, 2, 6, 7, 8, 3, 5])
    b = Board([0, 5, 7, 3, 8, 1, 2, 4, 6])


    print("Startzustand:", b)

    print("Parität:,", b.parity())

    print("Heuristik h1: ", b.h1())
    print("Heuristik h2: ", b.h2())

    for child in b.possible_actions():
        print(child)

    print("Ist gelöst:", b.is_solved())


if __name__ == "__main__":
    main()
