import numpy as np
import Piece

class ChessBoard:
    def __init__(self, board=None, player_to_move="white", previous_board=None):
        if board is None:
            board = generate_board()
        self.board = board
        self.player_to_move = player_to_move
        self.previous_board = previous_board      # Used to check for en-passant

    def update(self, board):
        self.previous_board = self.board
        self.board = board
        self.player_to_move = n(self.player_to_move)


def generate_board():
    board = np.zeros((8, 8), dtype=object)
    for y in range(8):
        for x in range(8):
            pos = (x, y)
            if y == 0:
                if x == 0 or x == 7:
                    board[pos] = Piece.Rook(pos, "white")
                elif x == 1 or x == 6:
                    board[pos] = Piece.Knight(pos, "white")
                elif x == 2 or x == 5:
                    board[pos] = Piece.Bishop(pos, "white")
                elif x == 3:
                    board[pos] = Piece.Queen(pos, "white")
                elif x == 4:
                    board[pos] = Piece.King(pos, "white")
            elif y == 1:
                board[pos] = Piece.Pawn(pos, "white")
            elif y == 6:
                board[pos] = Piece.Pawn(pos, n("white"))
            elif y == 7:
                if x == 0 or x == 7:
                    board[pos] = Piece.Rook(pos, n("white"))
                elif x == 1 or x == 6:
                    board[pos] = Piece.Knight(pos, n("white"))
                elif x == 2 or x == 5:
                    board[pos] = Piece.Bishop(pos, n("white"))
                elif x == 3:
                    board[pos] = Piece.Queen(pos, n("white"))
                elif x == 4:
                    board[pos] = Piece.King(pos, n("white"))
            else:
                board[pos] = None
    return board


def n(col):
    if col == "white":
        return "black"
    elif col == "black":
        return "white"
    else:
        raise Exception(f"Invalid color. Color was {col}.")


    # Check if there is a piece at pos with the given attributes
def is_p(chess_board, pos, color=None, piece=None, b="current"):
    if b == "current":
        b = chess_board.board
    elif b == "previous":
        b = chess_board.previous_board
    else:
        raise Exception(f"Invalid board. Board was {b}.")
    spot = b[tuple(pos)]
    if spot is not None:
        if color is not None:
            if spot.color != color:
                return False
        if piece is not None:
            if not isinstance(spot, piece):
                return False
        return True
    else:
        return False
