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
    
    def __eq__(self, other):
        return isinstance(other, Node) and self.board == other.board


def reconstruct_path(node: Node) -> deque[Board]:
    """
    Rekonstruiert den Pfad vom Startzustand bis zum Zielzustand.
    """
    path = deque()
    path.append(node.board)
    current_node = node
    while(current_node.parent):
        current_node = current_node.parent
        path.appendleft(current_node.board)

    return path


def a_star(start_board: Board) -> Optional[deque[Board]]:
    """
    Führt den A*-Algorithmus zur Lösung des 8-Puzzle-Problems aus.
    Es empfiehlt sich hierbei heapq für die open_list und set() für die
    closed_list zu verwenden.
    """

    open_list = []
    heapq.heappush(open_list, Node(start_board))
    closed_list = set()
    
    while(len(open_list) > 0):
        current_Node = heapq.heappop(open_list)
        if current_Node.board.is_solved():
            return reconstruct_path(current_Node)
        #Node wurde besucht
        closed_list.add(current_Node.board)
        for i, board in enumerate(current_Node.board.possible_actions()):
            newNode = Node(board, current_Node, (current_Node.g + 1))

            #Falls neuer zustand -> in openList
            if newNode not in open_list and newNode.board not in closed_list:
                heapq.heappush(open_list, newNode)
            
            #Board wurde schonmal erreicht. Vielleicht war's jetzt aber schneller?
            elif newNode in open_list:
                existing_node = next(n for n in open_list if n == newNode)
                if newNode.f < existing_node.f:
                    open_list.remove(existing_node)
                    heapq.heappush(open_list, newNode)

    return None  # Kein Pfad gefunden
