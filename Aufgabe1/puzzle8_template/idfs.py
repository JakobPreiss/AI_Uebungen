# idfs.py
# ------------------------------------------
# Author: Michael Blaich
# Datum: 21.03.2025
# Beschreibung: Implementierung der Iterativen Tiefensuche für
# das 8-Puzzle-Problem.
# ------------------------------------------
from board import Board
from collections import deque


def dfs(cur_board, path, limit, visited):
    """
    TODO: Implementiere die Rekursive Tiefensuche mit Limitierung.
    """
    if(cur_board.is_solved()):
        return cur_board
    if len(path) >= limit:
        return None
    
    #was_cut_off = False
    for i, board in enumerate(cur_board.possible_actions()):
        if board in path:
            continue
        visited.add(board)
        path.append(board)
       
        result = dfs(board, path, limit, visited)
        if result:
            return result
        else:
            #was_cut_off = True
            path.pop()

    
    return None


def idfs(start_board: Board, limit=1000):  # max. Tiefe arbiträr gesetzt
    """
    Iterative Tiefensuche mit Schleife zur Erhöhung des Tiefenlimits.
    Gibt den Lösungspfad als deque zurück oder None, wenn keine Lösung gefunden
    wurde.
    """
    for depth in range(limit):
        path = deque([start_board])
        visited = set()
        result = dfs(start_board, path, depth, visited)
        if result:
            return path
        print("depth: " + str(depth))
    return None
