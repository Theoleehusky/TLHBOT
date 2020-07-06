from board.pieces import *


class Board:
    value = {'P': 1, 'B': 3, 'N': 3, 'R': 5, 'Q': 9, 'K': 0, 'p': -1, 'b': -3, 'n': -3, 'r': -5, 'q': -9, 'k': 0, }

    def __init__(self):
        self.board = [
                [Rook(-1), 'n', 'b', 'q', 'k', 'b', 'n', Rook(-1)],
                ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                [Rook(1), 'N', 'B', 'Q', 'K', 'B', 'N', Rook(1)]]
        self.turn = 1
        self.castle = self.K = self.Q = self.k = self.q = True
        self.en = None

    def __repr__(self):
        out = ''
        for row in self.board:
            for piece in row:
                if piece is None:
                    out += '*'
                else:
                    out += str(piece)
            out += '\n'
        return out

    def moves(self):
        moves = []
        if self.turn == 1:
            pass
        else:
            pass
        return moves

    def move(self, move):
        a, b, c, d = ord(move[0]) - 97, 8 - int(move[1]), ord(move[2]) - 97, 8 - int(move[3])
        piece = self.board[b][a]

        if self.en:
            self.enpassant(piece, move)

        self.en = None

        if piece == 'p' and move[1] == '2' and move[3] == '4':
            self.en = move[0] + '3'
        elif piece == 'P' and move[1] == '7' and move[3] == '5':
            self.en = move[1] + '6'

        elif self.castle and (piece == 'k' or piece == 'K'):
            self.castling(move)

        elif len(move) == 5:
            if piece.isupper():
                piece = move[4].upper()
            else:
                piece = move[4]

        self.board[b][a] = None
        self.board[d][c] = piece
        self.turn *= -1

    def enpassant(self, piece, move):
        if piece == 'P' and self.en == move[2:3]:
            a, b = ord(self.en[0]) - 97, 8 - int(self.en[1])
            self.board[b-1][a] = None
        if piece == 'p' and self.en == move[2:3]:
            a, b = ord(self.en[0]) - 97, 8 - int(self.en[1])
            self.board[b+1][a] = None

    def castling(self, move):
        if move == 'e1g1':
            self.k, self.q = False
            self.board[7][7] = None
            self.board[7][5] = 'R'
        elif move == 'e1c1':
            self.k, self.q = False
            self.board[7][0] = None
            self.board[7][3] = 'R'
        elif move == 'e8g8':
            self.K, self.Q = False
            self.board[0][7] = None
            self.board[0][5] = 'r'
        elif move == 'e8c8':
            self.K, self.Q = False
            self.board[0][0] = None
            self.board[0][3] = 'r'
        if not (self.k or self.q or self.K or self.Q):
            self.castle = False

    def eval(self):
        ans = 0
        for row in self.board:
            for piece in row:
                if piece is not None:
                    ans += piece.value()
        return ans

    def fen(self):
        fen = ''
        for row in self.board:
            for piece in row:
                if piece is None:
                    fen += '*'
                else:
                    fen += str(piece)
            fen += '/'
        fen = fen[:-1]

        for n in range(8, 0, -1):
            fen = fen.replace('*' * n, str(n))

        if self.turn == 1:
            fen += ' w '
        else:
            fen += ' b '

        if not self.castle:
            fen += '-'
        else:
            if self.K:
                fen += 'K'
            if self.Q:
                fen += 'Q'
            if self.k:
                fen += 'k'
            if self.q:
                fen += 'q'

        if self.en is None:
            fen += '-'
        else:
            fen += self.en

        fen += ' 0 0'

        return fen

    def three_fold(self):
        pass

    def gameover(self):
        # checkmate or stalemate
        pass

    def is_capture(self):
        pass

    def gives_check(self):
        pass

    def count(self):
        ans = 0
        for row in self.board:
            for piece in row:
                if piece is not None:
                    ans += 1
        return ans
