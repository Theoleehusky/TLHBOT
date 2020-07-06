from board.Board import Board

board = Board()


while True:
    move = input()
    board.move(move)
    print(board)
    print(board.fen())

