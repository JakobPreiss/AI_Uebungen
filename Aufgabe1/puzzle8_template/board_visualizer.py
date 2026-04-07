import time
import os


class Board:
    def __init__(self, board: list[int]):
        self.board = board  # Liste mit 9 Elementen (0-8)


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


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


def visualize_boards(boards: list[Board], delay: float = 0.5):
    """
    Zeigt eine Liste von Board-Objekten nacheinander als 3x3 Gitter an.

    Args:
        boards: Liste von Board-Objekten mit je einer 'board'-Variable (9 Elemente, Ziffern 0–8).
        delay:  Wartezeit in Sekunden zwischen zwei Boards (Standard: 0.5s).
    """
    total = len(boards)

    for i, board_obj in enumerate(boards, start=1):
        clear_console()
        print_board(board_obj.board, i, total)
        time.sleep(delay)

    # Abschlussmeldung
    print("\n  ✓ Alle Boards angezeigt.")


# ---------------------------------------------------------------------------
# Beispiel
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    beispiel_boards = [
        Board([0, 1, 2, 3, 4, 5, 6, 7, 8]),
        Board([1, 0, 2, 3, 4, 5, 6, 7, 8]),
        Board([1, 4, 2, 3, 0, 5, 6, 7, 8]),
        Board([1, 4, 2, 3, 5, 0, 6, 7, 8]),
        Board([1, 4, 2, 3, 5, 8, 6, 7, 0]),
    ]

    visualize_boards(beispiel_boards)
