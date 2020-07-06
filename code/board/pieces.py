class Piece:
    def __init__(self, color):
        self.color = color

    def value(self):
        pass

    def moves(self, board):
        pass


class Pawn(Piece):
    def value(self):
        return self.color


class Knight(Piece):
    def value(self):
        return self.color * 3


class Bishop(Piece):
    def value(self):
        return self.color * 3


class Rook(Piece):
    def value(self):
        return self.color * 5

    def __str__(self):
        if self.color == 1:
            return 'R'
        return 'r'


class Queen(Piece):
    def value(self):
        return self.color * 9


class King(Piece):
    def value(self):
        return 0