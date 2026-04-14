# board.py
# ------------------------------------------
# Author: Michael Blaich
# Datum: 21.03.2025
# Beschreibung: Template für die Implementierung des A* Algorithmus
# ------------------------------------------
import heapq
from collections import deque
from board import Board
from typing import Optional


class Node:
    """
    Repräsentiert einen Knoten im Suchbaum für den A*-Algorithmus.

    Attribute:
        board (Board): Der aktuelle Zustand des Spielfelds.
        parent (Node, optional): Der Vorgängerknoten (Elternknoten) in der Pfadsuche.
        g (int): Die bisherigen Pfadkosten von Start bis zu diesem Knoten.
        h (int): Der geschätzte Abstand zum Zielzustand (Heuristik).
        f (int): Die geschätzten Gesamtkosten f = g + h.
    """

    def __init__(self, board: Board, parent: 'Node' = None, g=0):
        self.board = board
        self.parent = parent
        self.g = g  # Pfadkosten
        self.h = board.h2()  # Heuristikwert
        self.f = self.g + self.h  # f = g + h

    def __lt__(self, other):
        """
        Vergleichsmethode für die Prioritätswarteschlange.
        Knoten mit kleineren f-Werten werden bevorzugt.
        """
        return self.f < other.f  # Für PriorityQueue


def reconstruct_path(node: Node) -> deque[Board]:
    """
    Rekonstruiert den Pfad vom Startzustand bis zum Zielzustand.
    TODO: Implementiere das erstellen des Pfades.
    """
    path = deque()
    while node is not None:
        path.appendleft(node.board)
        node = node.parent
    return path


def a_star(start_board: Board) -> Optional[deque[Board]]:
    """
    Führt den A*-Algorithmus zur Lösung des 8-Puzzle-Problems aus.
    TODO: Implementiere den A*-Algorithmus.
    Es empfiehlt sich hierbei heapq für die open_list und set() für die
    closed_list zu verwenden.
    """
    open_list = []
    heapq.heappush(open_list, Node(start_board))
    closed_list = set()

    while open_list:
        current = heapq.heappop(open_list)

        if current.board.is_solved():
            return reconstruct_path(current)

        closed_list.add(current.board)

        for child_board in current.board.possible_actions():
            if child_board in closed_list:
                continue
            child_node = Node(child_board, parent=current, g=current.g + 1)
            heapq.heappush(open_list, child_node)


    return None  # Kein Pfad gefunden
