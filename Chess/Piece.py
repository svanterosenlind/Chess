class Piece:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color


class Pawn(Piece):
    def __init__(self, pos, color):
        super().__init__(pos, color)
        self.text = "P"


class Rook(Piece):
    def __init__(self, pos, color):
        super().__init__(pos, color)
        self.text = "R"


class Knight(Piece):
    def __init__(self, pos, color):
        super().__init__(pos, color)
        self.text = "Kn"


class Bishop(Piece):
    def __init__(self, pos, color):
        super().__init__(pos, color)
        self.text = "B"


class Queen(Piece):
    def __init__(self, pos, color):
        super().__init__(pos, color)
        self.text = "Q"


class King(Piece):
    def __init__(self, pos, color):
        super().__init__(pos, color)
        self.text = "K"
