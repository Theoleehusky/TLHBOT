import chess
import requests
from berserk.exceptions import ApiError


class Game:
    value = {'p': 1, 'b': 3, 'n': 3, 'r': 5, 'q': 9, 'k': 0}
    deep = 2
    board = chess.Board()

    def __init__(self, client, game_id):
        self.opening = True
        self.board.reset()

        self.game_id = game_id
        self.client = client
        self.stream = client.bots.stream_game_state(game_id)

        game = next(self.stream)
        if 'id' in game['white'] and game['white']['id'] == 'tlhbot':
            self.color = 1
        else:
            self.color = -1
        print("Game", self.game_id)
        self.play()

    def play(self):
        if self.color == 1:
            self.board.push_uci('e2e4')
            self.client.bots.make_move(self.game_id, 'e2e4')

            for event in self.stream:
                if event['type'] == 'gameState':
                    if event['status'] == 'mate' or event['status'] == 'resigned':
                        print('game ended')
                        break
                    elif event['status'] == 'started' and (len(event['moves']) - 4) / 5 % 2 == 1:
                        self.move(event)
                elif event['type'] == 'chatLine':
                    print(event)

        else:
            for event in self.stream:
                if event['type'] == 'gameState':
                    if event['status'] == 'mate' or event['status'] == 'resigned':
                        print('game ended')
                        break
                    elif event['status'] == 'started' and (len(event['moves']) - 4) / 5 % 2 == 0:
                        self.move(event)
                elif event['type'] == 'chatLine':
                    print(event)

    def move(self, game_state):
        self.board.push_uci(game_state['moves'][-4:])
        if self.opening:
            move = requests.get('https://explorer.lichess.ovh/master?moves=1&topGames=0&fen=' + self.board.fen()).json()['moves']
            if len(move) == 0:
                self.opening = False
                print("Opening over")
                move = self.minimax(self.deep, True, -1000, 1000, True)
            else:
                move = move[0]['uci']
        elif len(self.board.piece_map()) <= 7:
            print("Endgame")
            move = requests.get('http://tablebase.lichess.ovh/standard?fen=' + self.board.fen()).json()['moves']['uci']
        else:
            move = self.minimax(self.deep, True, -1000, 1000, True)

        self.board.push_uci(move)

        while True:
            try:
                self.client.bots.make_move(self.game_id, move)
            except ApiError:
                print('APIError')
                continue
            else:
                break

    def minimax(self, n, maxmin, alpha, beta, move):
        if self.board.is_game_over():
            result = self.board.result()
            if result == '0-1':
                return -100 * self.color
            elif result == '1-0':
                return 100 * self.color
            return 0
        if self.board.is_repetition():
            return 0
        if n == 0:
            return self.advantage()

        if move:
            ans = None
            best = -1000
            for move in (str(x) for x in self.board.legal_moves):
                print(move, end=', ')
                # x = chess.Move(0, 0).from_uci(move)
                # if self.board.is_capture(x) or self.board.gives_check(x):
                #     self.board.push_uci(move)
                #     value = self.minimax(n, False, alpha, beta, False)
                # else:
                self.board.push_uci(move)
                value = self.minimax(n - 1, False, alpha, beta, False)
                self.board.pop()
                if value > best:
                    best = value
                    ans = move
                    if best > alpha:
                        alpha = best
                        if beta <= alpha:
                            break
            print()
            print(best, '!!!!')
            return ans
        if maxmin:
            best = -1000
            for move in (str(x) for x in self.board.legal_moves):
                # x = chess.Move(0, 0).from_uci(move)
                # if self.board.is_capture(x) or self.board.gives_check(x):
                #     self.board.push_uci(move)
                #     value = self.minimax(n, False, alpha, beta, False)
                # else:
                self.board.push_uci(move)
                value = self.minimax(n - 1, False, alpha, beta, False)
                self.board.pop()
                if value > best:
                    best = value
                    if best > alpha:
                        alpha = best
                        if beta <= alpha:
                            break
            return best
        else:
            worst = 1000
            for move in (str(x) for x in self.board.legal_moves):
                # x = chess.Move(0, 0).from_uci(move)
                # if self.board.is_capture(x) or self.board.gives_check(x):
                #     self.board.push_uci(move)
                #     value = self.minimax(n, True, alpha, beta, False)
                # else:
                self.board.push_uci(move)
                value = self.minimax(n - 1, True, alpha, beta, False)
                self.board.pop()
                if value < worst:
                    worst = value
                    if worst < beta:
                        beta = min(beta, worst)
                        if beta <= alpha:
                            break
            return worst

    def advantage(self):
        n = 0
        for piece in self.board.piece_map().values():
            if piece.color:
                n += self.value[piece.symbol().lower()]
            else:
                n -= self.value[piece.symbol().lower()]
        return n * self.color
