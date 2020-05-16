import chess
import requests

board = chess.Board()

print(board.is_capture(chess.Move(0, 0).from_uci('e2e4')))