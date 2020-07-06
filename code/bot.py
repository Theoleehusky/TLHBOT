import berserk
from Game import Game
import time

session = berserk.TokenSession('rwerWlJJoAuY1Wug')
client = berserk.Client(session=session)

#
client.challenges.create('theoleehusky', False, 300, 3, color='white')
# print(client.challenges.create_open(60, 3))

for event in client.bots.stream_incoming_events():
    time.sleep(1)
    print(event)
    # if event['type'] == 'challenge':
    #     client.bots.accept_challenge(event['challenge']['id'])
    if event['type'] == 'gameStart':
        game = Game(client, event['game']['id'])

