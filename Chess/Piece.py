import numpy as np
import ChessBoard
import copy


class Piece:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

    def legal_moves(self, chess_board):
        pass

    def __repr__(self):
        return self.text + str(self.pos)

    def __eq__(self, other):
        if other is None:
            return False
        if np.array_equal(other.pos, self.pos) and isinstance(self, type(other)) and other.color == self.color:
            return True
        else:
            return False


class Pawn(Piece):
    text = "P"

    def __init__(self, pos, color):
        super().__init__(pos, color)

    def legal_moves(self, chess_board, legal=True):
        boards = []
        if self.color == "white":
            d = 1
            start = 1
        else:
            start = 6
            d = -1
        # Move straight forward
        if inside(self.pos + np.array([0, d])) and not chess_board.is_p(self.pos + np.array([0, d])):
            # If it will move to a promotion square
            if not inside(self.pos + np.array([0, 2 * d])):
                b = copy.deepcopy(chess_board.board)
                b[tuple(self.pos + np.array([0, d]))] = b[tuple(self.pos)]
                b[tuple(self.pos)] = None
                new_board = chess_board.make_move(b, self.pos + np.array([0, d]), "move", "promotion")
                new_board.player_to_move = ChessBoard.n(new_board.player_to_move)
                if legal:
                    if new_board.is_legal():
                        boards.append(new_board)
                else:
                    boards.append(new_board)
            # If it won't move to a promotion square
            else:
                b = copy.deepcopy(chess_board.board)
                b[tuple(self.pos + np.array([0, d]))] = b[tuple(self.pos)]
                b[tuple(self.pos + np.array([0, d]))].pos = self.pos + np.array([0, d])
                b[tuple(self.pos)] = None
                new_board = chess_board.make_move(b, self.pos + np.array([0, d]), "move", None)
                if legal:
                    if new_board.is_legal():
                        boards.append(new_board)
                else:
                    boards.append(new_board)

            # Move two steps forward
            if self.pos[1] == start and not chess_board.is_p(self.pos + np.array([0, 2 * d])):
                b = copy.deepcopy(chess_board.board)
                b[tuple(self.pos + np.array([0, 2 * d]))] = b[tuple(self.pos)]
                b[tuple(self.pos + np.array([0, 2 * d]))].pos = self.pos + np.array([0, 2 * d])
                b[tuple(self.pos)] = None
                new_board = chess_board.make_move(b, self.pos + np.array([0, 2*d]), "move", None)
                if legal:
                    if new_board.is_legal():
                        boards.append(new_board)
                else:
                    boards.append(new_board)

        # Regular captures in both directions
        for xdir in [-1, 1]:
            if inside(self.pos + np.array([xdir, d])) and \
                    chess_board.is_p(self.pos + np.array([xdir, d]), color=ChessBoard.n(self.color)):
                # If it will move to a promotion square with the capture
                if not inside(self.pos + np.array([0, 2 * d])):
                    b = copy.deepcopy(chess_board.board)
                    b[tuple(self.pos + np.array([xdir, d]))] = b[tuple(self.pos)]
                    b[tuple(self.pos)] = None
                    new_board = chess_board.make_move(b, self.pos + np.array([xdir, d]), "capture", "promotion")
                    new_board.player_to_move = ChessBoard.n(new_board.player_to_move)
                    if legal:
                        if new_board.is_legal():
                            boards.append(new_board)
                    else:
                        boards.append(new_board)
                # If it won't move to a promotion square with its capture
                else:
                    b = copy.deepcopy(chess_board.board)
                    b[tuple(self.pos + np.array([xdir, d]))] = b[tuple(self.pos)]
                    b[tuple(self.pos + np.array([xdir, d]))].pos = self.pos + np.array([xdir, d])
                    b[tuple(self.pos)] = None
                    new_board = chess_board.make_move(b, self.pos + np.array([xdir, d]), "capture", None)
                    if legal:
                        if new_board.is_legal():
                            boards.append(new_board)
                    else:
                        boards.append(new_board)

        # En-passant in both directions
        for xdir in [-1, 1]:
            if self.pos[1] == start + 3 * d and inside(self.pos + [xdir, d]):
                if chess_board.is_p(self.pos + np.array([xdir, 0]), color=ChessBoard.n(self.color), piece=Pawn) and \
                        chess_board.is_p(self.pos + np.array([xdir, 2 * d]),
                                         color=ChessBoard.n(self.color), piece=Pawn, b="previous"):
                    b = copy.deepcopy(chess_board.board)
                    b[tuple(self.pos + np.array([xdir, d]))] = b[tuple(self.pos)]
                    b[tuple(self.pos + np.array([xdir, d]))].pos = self.pos + np.array([xdir, d])
                    b[tuple(self.pos + np.array([xdir, 0]))] = None
                    b[tuple(self.pos)] = None
                    new_board = chess_board.make_move(b, self.pos + np.array([xdir, d]), "capture", None)
                    if legal:
                        if new_board.is_legal():
                            boards.append(new_board)
                    else:
                        boards.append(new_board)
        return boards


class Rook(Piece):
    text = "R"

    def __init__(self, pos, color):
        super().__init__(pos, color)

    def legal_moves(self, chess_board, legal=True):
        boards = []
        dirs = [np.array([1, 0]), np.array([0, 1]), np.array([-1, 0]), np.array([0, -1])]
        for d in dirs:
            for n in range(1, 7):
                if not inside(self.pos + n * d):
                    break   # Only out of the inner loop

                # If the square is empty or has a piece of opposite color
                if not chess_board.is_p(self.pos + n * d, color=self.color):
                    b = copy.deepcopy(chess_board.board)
                    b[tuple(self.pos + n * d)] = b[tuple(self.pos)]
                    b[tuple(self.pos + n * d)].pos = self.pos + n * d
                    b[tuple(self.pos)] = None

                    # If it was an one of the opponent's pieces
                    if chess_board.board[tuple(self.pos + n * d)] is not None:
                        new_board = chess_board.make_move(b, self.pos + n * d, "capture", None)
                        if legal:
                            if new_board.is_legal():
                                boards.append(new_board)
                        else:
                            boards.append(new_board)
                        break
                    else:
                        new_board = chess_board.make_move(b, self.pos + n * d, "move", None)
                        if legal:
                            if new_board.is_legal():
                                boards.append(new_board)
                        else:
                            boards.append(new_board)
                else:
                    break
        return boards


class Knight(Piece):
    text = "Kn"

    def __init__(self, pos, color):
        super().__init__(pos, color)

    def legal_moves(self, chess_board, legal=True):
        boards = []
        moves = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
        for move in moves:
            new_pos = self.pos + np.array(move)
            if inside(new_pos) and not chess_board.is_p(new_pos, color=self.color):
                b = copy.deepcopy(chess_board.board)
                b[tuple(new_pos)] = b[tuple(self.pos)]
                b[tuple(new_pos)].pos = new_pos
                b[tuple(self.pos)] = None
                # It is a capture
                if chess_board.is_p(new_pos, color=ChessBoard.n(self.color)):
                    move_type = "capture"
                # Just a regular old move
                else:
                    move_type = "move"
                new_board = chess_board.make_move(b, new_pos, move_type, None)
                if legal:
                    if new_board.is_legal():
                        boards.append(new_board)
                else:
                    boards.append(new_board)
        return boards


class Bishop(Piece):
    text = "B"

    def __init__(self, pos, color):
        super().__init__(pos, color)

    def legal_moves(self, chess_board, legal=True):
        boards = []
        dirs = [np.array([1, 1]), np.array([-1, 1]), np.array([-1, -1]), np.array([1, -1])]
        for d in dirs:
            for n in range(1, 7):
                if not inside(self.pos + n * d):
                    break
                # If the square is empty or has a piece of opposite color
                if not chess_board.is_p(self.pos + n * d, color=self.color):
                    b = copy.deepcopy(chess_board.board)
                    b[tuple(self.pos + n * d)] = b[tuple(self.pos)]
                    b[tuple(self.pos + n * d)].pos = self.pos + n * d
                    b[tuple(self.pos)] = None
                    # If it was a capture
                    if chess_board.board[tuple(self.pos + n * d)] is not None:
                        new_board = chess_board.make_move(b, self.pos + n * d, "capture", None)
                        if legal:
                            if new_board.is_legal():
                                boards.append(new_board)
                        else:
                            boards.append(new_board)
                        break
                    else:
                        new_board = chess_board.make_move(b, self.pos + n * d, "move", None)
                        if legal:
                            if new_board.is_legal():
                                boards.append(new_board)
                        else:
                            boards.append(new_board)
                else:
                    break
        return boards


class Queen(Piece):
    text = "Q"

    def __init__(self, pos, color):
        super().__init__(pos, color)

    def legal_moves(self, chess_board, legal=True):
        boards = []
        dirs = [np.array([1, 0]), np.array([0, 1]), np.array([-1, 0]), np.array([0, -1]),
                np.array([1, 1]), np.array([-1, 1]), np.array([-1, -1]), np.array([1, -1])]
        for d in dirs:
            for n in range(1, 7):
                new_pos = self.pos + n * d
                if not inside(new_pos):
                    break   # Only out of the inner loop
                if not chess_board.is_p(new_pos, color=self.color):
                    # If the square is empty or has a piece of opposite color
                    b = copy.deepcopy(chess_board.board)
                    b[tuple(new_pos)] = b[tuple(self.pos)]
                    b[tuple(new_pos)].pos = new_pos
                    b[tuple(self.pos)] = None
                    # If it was a capture
                    if chess_board.board[tuple(new_pos)] is not None:
                        new_board = chess_board.make_move(b, new_pos, "capture", None)
                        if legal:
                            if new_board.is_legal():
                                boards.append(new_board)
                        else:
                            boards.append(new_board)
                        break
                    else:
                        new_board = chess_board.make_move(b, new_pos, "move", None)
                        if legal:
                            if new_board.is_legal():
                                boards.append(new_board)
                        else:
                            boards.append(new_board)
                else:
                    break
        return boards


class King(Piece):
    text = "K"

    def __init__(self, pos, color):
        super().__init__(pos, color)

    def legal_moves(self, chess_board, legal=True):
        boards = []
        dirs = [np.array([1, 0]), np.array([0, 1]), np.array([-1, 0]), np.array([0, -1]),
                np.array([1, 1]), np.array([-1, 1]), np.array([-1, -1]), np.array([1, -1])]
        for d in dirs:

            if not inside(self.pos + d):
                continue
            if not chess_board.is_p(self.pos + d, color=self.color):
                # If the square is empty or has a piece of opposite color
                b = copy.deepcopy(chess_board.board)
                b[tuple(self.pos + d)] = b[tuple(self.pos)]
                b[tuple(self.pos + d)].pos = self.pos + d
                b[tuple(self.pos)] = None
                # If it was a capture
                if chess_board.board[tuple(self.pos + d)] is not None:
                    new_board = chess_board.make_move(b, self.pos + d, "capture", None)
                    if legal:
                        if new_board.is_legal():
                            boards.append(new_board)
                    else:
                        boards.append(new_board)
                else:
                    new_board = chess_board.make_move(b, self.pos + d, "move", None)
                    if legal:
                        if new_board.is_legal():
                            boards.append(new_board)
                    else:
                        boards.append(new_board)
        return boards


def inside(pos):
    if pos[0] < 0 or pos[0] > 7 or pos[1] < 0 or pos[1] > 7:
        return False
    else:
        return True

