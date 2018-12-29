import numpy as np
import ChessBoard


class Piece:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

    def legal_moves(self, chess_board):
        pass


class Pawn(Piece):
    def __init__(self, pos, color):
        super().__init__(pos, color)
        self.text = "P"

    def legal_moves(self, chess_board):
        legal_moves = []
        legal_captures = []
        if self.color == "white":

            if not ChessBoard.is_p(chess_board, self.pos + np.array([0, 1])):   # Move straight forward
                legal_moves.append(self.pos + np.array([0, 1]))
                if self.pos[1] == 1 and not ChessBoard.is_p(chess_board, self.pos + np.array([0, 2])): # Two steps if it hasn't moved yet
                    legal_moves.append(self.pos + np.array([0, 2]))

            if inside(self.pos + np.array([-1, 1])) and \
                    ChessBoard.is_p(chess_board, self.pos + np.array([-1, 1]), color="black"):
                    legal_captures.append(self.pos + np.array([-1, 1]))

            if inside(self.pos + np.array([1, 1])) and \
                    ChessBoard.is_p(chess_board, self.pos + np.array([1, 1]), color="black"):
                    legal_captures.append(self.pos + np.array([1, 1]))

            if self.pos[1] == 4 and self.pos[0] != 0:       # En passant to the right
                if ChessBoard.is_p(chess_board, self.pos + np.array([1, 0]), color="black", piece=Pawn) and \
                        ChessBoard.is_p(chess_board, self.pos + np.array([1, 2]), color="black", piece=Pawn, b="previous"):
                    legal_captures.append(self.pos + np.array([1, 1]))
            elif self.pos[1] == 4 and self.pos[0] != 7:       # En passant to the left
                if ChessBoard.is_p(chess_board, self.pos + np.array([-1, 0]), color="black", piece=Pawn) and \
                        ChessBoard.is_p(chess_board, self.pos + np.array([-1, 2]), color="black", piece=Pawn, b="previous"):
                    legal_captures.append(self.pos + np.array([-1, 1]))
        else:   # self.color == "black"
            if chess_board.board[tuple(self.pos + np.array([0, -1]))] is None:  # Move straight forward
                legal_moves.append(self.pos + np.array([0, -1]))
                if self.pos[1] == 6 and chess_board.board[tuple(self.pos + np.array([0, -2]))] is None:
                    legal_moves.append(self.pos + np.array([0, -2]))

            if inside(self.pos + np.array([-1, -1])) and \
                    chess_board.board[tuple(self.pos + np.array([-1, -1]))] is not None:  # Capture to the left
                if chess_board.board[tuple(self.pos + np.array([-1, -1]))].color == "white":
                    legal_captures.append(self.pos + np.array([-1, -1]))

            if inside(self.pos + np.array([1, -1])) and \
                    chess_board.board[tuple(self.pos + np.array([1, -1]))] is not None:  # Capture to the right
                if chess_board.board[tuple(self.pos + np.array([1, -1]))].color == "white":
                    legal_captures.append(self.pos + np.array([1, -1]))
            if self.pos[1] == 3 and self.pos[0] != 0:       # En passant to the right
                if ChessBoard.is_p(chess_board, self.pos + np.array([1, 0]), color="white", piece=Pawn) and \
                        ChessBoard.is_p(chess_board, self.pos + np.array([1, -2]), color="white", piece=Pawn, b="previous"):
                    legal_captures.append(self.pos + np.array([1, -1]))
            elif self.pos[1] == 3 and self.pos[0] != 7:       # En passant to the left
                if ChessBoard.is_p(chess_board, self.pos + np.array([-1, 0]), color="white", piece=Pawn) and \
                        ChessBoard.is_p(chess_board, self.pos + np.array([-1, -2]), color="white", piece=Pawn, b="previous"):
                    legal_captures.append(self.pos + np.array([-1, -1]))

        return legal_moves, legal_captures


class Rook(Piece):
    def __init__(self, pos, color):
        super().__init__(pos, color)
        self.text = "R"

    def legal_moves(self, chess_board):
        legal_moves = []
        legal_captures = []
        for n in range(1, 7):
            if not inside(self.pos + np.array([n, 0])):
                break
            spot = chess_board.board[tuple(self.pos + np.array([n, 0]))]
            if spot is not None:
                if spot.color == self.color:
                    break
                else:
                    legal_captures.append(self.pos + np.array([n, 0]))
                    break
            legal_moves.append(self.pos + np.array([n, 0]))

        for n in range(1, 7):
            if not inside(self.pos + np.array([-n, 0])):
                break
            spot = chess_board.board[tuple(self.pos + np.array([-n, 0]))]
            if spot is not None:
                if spot.color == self.color:
                    break
                else:
                    legal_captures.append(self.pos + np.array([-n, 0]))
                    break
            legal_moves.append(self.pos + np.array([-n, 0]))

        for n in range(1, 7):
            if not inside(self.pos + np.array([0, n])):
                break
            spot = chess_board.board[tuple(self.pos + np.array([0, n]))]
            if spot is not None:
                if spot.color == self.color:
                    break
                else:
                    legal_captures.append(self.pos + np.array([0, n]))
                    break
            legal_moves.append(self.pos + np.array([0, n]))

        for n in range(1, 7):
            if not inside(self.pos + np.array([0, -n])):
                break
            spot = chess_board.board[tuple(self.pos + np.array([0, -n]))]
            if spot is not None:
                if spot.color == self.color:
                    break
                else:
                    legal_captures.append(self.pos + np.array([0, -n]))
                    break
            legal_moves.append(self.pos + np.array([0, -n]))
        return legal_moves, legal_captures


class Knight(Piece):
    def __init__(self, pos, color):
        super().__init__(pos, color)
        self.text = "Kn"

    def legal_moves(self, chess_board):
        legal_moves = []
        legal_captures = []
        moves = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
        for move in moves:
            new_pos = self.pos + np.array(move)
            if inside(new_pos):
                spot = chess_board.board[tuple(new_pos)]
                if spot is None:
                    legal_moves.append(new_pos)
                elif spot.color != self.color:
                    legal_captures.append(new_pos)

        return legal_moves, legal_captures


class Bishop(Piece):
    def __init__(self, pos, color):
        super().__init__(pos, color)
        self.text = "B"

    def legal_moves(self, chess_board):
        legal_moves = []
        legal_captures = []
        for n in range(1, 7):
            if not inside(self.pos + np.array([n, n])):
                break
            spot = chess_board.board[tuple(self.pos + np.array([n, n]))]
            if spot is not None:
                if spot.color == self.color:
                    break
                else:
                    legal_captures.append(self.pos + np.array([n, n]))
                    break
            legal_moves.append(self.pos + np.array([n, n]))

        for n in range(1, 7):
            if not inside(self.pos + np.array([-n, n])):
                break
            spot = chess_board.board[tuple(self.pos + np.array([-n, n]))]
            if spot is not None:
                if spot.color == self.color:
                    break
                else:
                    legal_captures.append(self.pos + np.array([-n, n]))
                    break
            legal_moves.append(self.pos + np.array([-n, n]))

        for n in range(1, 7):
            if not inside(self.pos + np.array([n, -n])):
                break
            spot = chess_board.board[tuple(self.pos + np.array([n, -n]))]
            if spot is not None:
                if spot.color == self.color:
                    break
                else:
                    legal_captures.append(self.pos + np.array([n, -n]))
                    break
            legal_moves.append(self.pos + np.array([n, -n]))

        for n in range(1, 7):
            if not inside(self.pos + np.array([-n, -n])):
                break
            spot = chess_board.board[tuple(self.pos + np.array([-n, -n]))]
            if spot is not None:
                if spot.color == self.color:
                    break
                else:
                    legal_captures.append(self.pos + np.array([-n, -n]))
                    break
            legal_moves.append(self.pos + np.array([-n, -n]))
        return legal_moves, legal_captures


class Queen(Piece):
    def __init__(self, pos, color):
        super().__init__(pos, color)
        self.text = "Q"

    def legal_moves(self, chess_board):
        legal_moves = []
        legal_captures = []

        for n in range(1, 7):
            if not inside(self.pos + np.array([n, n])):
                break
            spot = chess_board.board[tuple(self.pos + np.array([n, n]))]
            if spot is not None:
                if spot.color == self.color:
                    break
                else:
                    legal_captures.append(self.pos + np.array([n, n]))
                    break
            legal_moves.append(self.pos + np.array([n, n]))

        for n in range(1, 7):
            if not inside(self.pos + np.array([-n, n])):
                break
            spot = chess_board.board[tuple(self.pos + np.array([-n, n]))]
            if spot is not None:
                if spot.color == self.color:
                    break
                else:
                    legal_captures.append(self.pos + np.array([-n, n]))
                    break
            legal_moves.append(self.pos + np.array([-n, n]))

        for n in range(1, 7):
            if not inside(self.pos + np.array([n, -n])):
                break
            spot = chess_board.board[tuple(self.pos + np.array([n, -n]))]
            if spot is not None:
                if spot.color == self.color:
                    break
                else:
                    legal_captures.append(self.pos + np.array([n, -n]))
                    break
            legal_moves.append(self.pos + np.array([n, -n]))

        for n in range(1, 7):
            if not inside(self.pos + np.array([-n, -n])):
                break
            spot = chess_board.board[tuple(self.pos + np.array([-n, -n]))]
            if spot is not None:
                if spot.color == self.color:
                    break
                else:
                    legal_captures.append(self.pos + np.array([-n, -n]))
                    break
            legal_moves.append(self.pos + np.array([-n, -n]))

        for n in range(1, 7):
            if not inside(self.pos + np.array([n, 0])):
                break
            spot = chess_board.board[tuple(self.pos + np.array([n, 0]))]
            if spot is not None:
                if spot.color == self.color:
                    break
                else:
                    legal_captures.append(self.pos + np.array([n, 0]))
                    break
            legal_moves.append(self.pos + np.array([n, 0]))

        for n in range(1, 7):
            if not inside(self.pos + np.array([-n, 0])):
                break
            spot = chess_board.board[tuple(self.pos + np.array([-n, 0]))]
            if spot is not None:
                if spot.color == self.color:
                    break
                else:
                    legal_captures.append(self.pos + np.array([-n, 0]))
                    break
            legal_moves.append(self.pos + np.array([-n, 0]))

        for n in range(1, 7):
            if not inside(self.pos + np.array([0, n])):
                break
            spot = chess_board.board[tuple(self.pos + np.array([0, n]))]
            if spot is not None:
                if spot.color == self.color:
                    break
                else:
                    legal_captures.append(self.pos + np.array([0, n]))
                    break
            legal_moves.append(self.pos + np.array([0, n]))

        for n in range(1, 7):
            if not inside(self.pos + np.array([0, -n])):
                break
            spot = chess_board.board[tuple(self.pos + np.array([0, -n]))]
            if spot is not None:
                if spot.color == self.color:
                    break
                else:
                    legal_captures.append(self.pos + np.array([0, -n]))
                    break
            legal_moves.append(self.pos + np.array([0, -n]))
        return legal_moves, legal_captures


class King(Piece):
    def __init__(self, pos, color):
        super().__init__(pos, color)
        self.text = "K"

    def legal_moves(self, chess_board):
        legal_moves = []
        legal_captures = []
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if x != 0 or y != 0:
                    if inside(self.pos + np.array([x, y])):
                        spot = chess_board.board[tuple(self.pos + np.array([x, y]))]
                        if spot is None:
                            legal_moves.append(self.pos + np.array([x, y]))
                        elif spot.color != self.color:
                            legal_captures.append(self.pos + np.array([x, y]))
        return legal_moves, legal_captures


def inside(pos):
    if pos[0] < 0 or pos[0] > 7 or pos[1] < 0 or pos[1] > 7:
        return False
    else:
        return True
