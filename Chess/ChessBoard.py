from Piece import *
import numpy as np

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
                    board[pos] = Rook(pos, "white")
                elif x == 1 or x == 6:
                    board[pos] = Knight(pos, "white")
                elif x == 2 or x == 5:
                    board[pos] = Bishop(pos, "white")
                elif x == 3:
                    board[pos] = Queen(pos, "white")
                elif x == 4:
                    board[pos] = King(pos, "white")
            elif y == 1:
                board[pos] = Pawn(pos, "white")
            elif y == 6:
                board[pos] = Pawn(pos, n("white"))
            elif y == 7:
                if x == 0 or x == 7:
                    board[pos] = Rook(pos, n("white"))
                elif x == 1 or x == 6:
                    board[pos] = Knight(pos, n("white"))
                elif x == 2 or x == 5:
                    board[pos] = Bishop(pos, n("white"))
                elif x == 3:
                    board[pos] = Queen(pos, n("white"))
                elif x == 4:
                    board[pos] = King(pos, n("white"))
            else:
                board[pos] = None
    print(board)
    return board


def n(col):
    if col == "white":
        return "black"
    elif col == "black":
        return "white"
    else:
        raise Exception(f"Invalid color. Color was {col}.")