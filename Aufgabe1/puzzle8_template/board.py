
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
        """
        wrong_pair_count = 0
        for i, val in enumerate(self.board):
            if val == 0:
                continue
            for j in range(i, -1, -1):
                if self.board[j] == 0:
                    continue
                if val < self.board[j]:
                    wrong_pair_count += 1
                    break
            
        return wrong_pair_count % 2 == 0

    def h1(self):
        """
        Heuristikfunktion h1 (siehe Aufgabenstellung).
        Heuristik ist monoton, weil eine Korrektur einer position eines Spielsteins mindestens die Kosten von 1 hat,
        wodurch die Heuristik von einem verbesserten Zustand (-1 falsche position), immer mit der Mindesterhöhung von 1
        einhergeht, wodurch die Gleichung h(n) <= c(n,n') + h(n') nicht verletzt wird  
        """
        wrong_position_count = 0
        for i, val in enumerate(self.board):
            if val != 0 and i != val:
                wrong_position_count += 1

        return wrong_position_count

    def h2(self):
        """
        Heuristikfunktion h2 (siehe Aufgabenstellung).
        Heuristik ist monoton, weil eine veränderung eines Steins näher zu seiner Zielposition immer auch die Kosten 1 hat.
        Wenn heuristik 1 weniger wird, weil stein seiner position näher gekommen ist, dann ist durch die Schrittkosten
        die Gleichung h(n) <= c(n,n') + h(n') nicht verletzt.
        h1 <= h2(n), da ein Stein um für h1 zu zählen (also Wert 1 zu haben), mindestens 1 Feld von seiner richtigen
        Position entfernt sein muss, was ihm in h2 auch den Wert 1 geben würde. Nur dass in h2 der Wert auch höher sein kann.
        """
        manhatten_sum = 0
        for i, val in enumerate(self.board):
            if val == 0:
                continue
            x_diff = abs((i % 3) - (val % 3))
            y_diff = abs((i // 3) - (val // 3))

            manhatten_sum += (x_diff + y_diff)
            #print("value: " + str(val) + ".  manhatten: " + str((x_diff + y_diff)) + "  x: " + str(x_diff) + "  y: " + str(y_diff))

        return manhatten_sum

    def possible_actions(self):
        """
        Gibt eine Liste aller möglichen Folge-Boards zurück,
        die durch einen gültigen Zug entstehen.
        """
        zero_position = next(i for i, x in enumerate(self.board) if x == 0)
        switch_index_list = Board.get_possible_switches(zero_position)
        
        possible_boards = []
        for i, switch_val in enumerate(switch_index_list):
            possible_boards.append(Board(board=Board.switch(self.board, zero_position, switch_val)))

        return possible_boards

    @staticmethod
    def switch(board, zero_index, switch_index):
        newboard = board.copy()
        newboard[zero_index] = newboard[switch_index]
        newboard[switch_index] = 0
        return newboard

    @staticmethod
    def get_possible_switches(zero_position):
        switch_index_list = []
        if zero_position - 3 > -1:
            switch_index_list.append(zero_position - 3)
        if zero_position + 3 < 9:
            switch_index_list.append(zero_position + 3)
        if zero_position % 3 != 0:
            switch_index_list.append(zero_position - 1)
        if zero_position % 3 != 2:
            switch_index_list.append(zero_position + 1)

        return switch_index_list

    def is_solved(self):
        """
        Prüft, ob das Board im Zielzustand ist (0,1,2,3,...,8).
        """

        return self.h1() == 0


def main():
    b = Board([7, 2, 4, 5, 0, 6, 8, 3, 1])  # Startzustand manuell setzen
    #b = Board()  # Lösbares Puzzle zufällig generieren
    #b = Board([0, 1, 2, 3, 4, 5, 6, 7, 8])
    print("Startzustand:", b)

    print("Parität:,", b.parity())

    print("Heuristik h1: ", b.h1())
    print("Heuristik h2: ", b.h2())

    for child in b.possible_actions():
        print(child)

    print("Ist gelöst:", b.is_solved())


if __name__ == "__main__":
    main()
