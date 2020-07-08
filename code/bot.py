import berserk
from Game import Game

with open("token.txt", 'r') as f:
    token = f.read()

session = berserk.TokenSession(token)
client = berserk.Client(session=session)


a = client.challenges.create('theoleehusky', False, 300, 3, color='white')
# print(client.challenges.create_open(60, 3))

for event in client.bots.stream_incoming_events():
    print(event)
    # if event['type'] == 'challenge':
    #     client.bots.accept_challenge(event['challenge']['id'])
    if event['type'] == 'gameStart':
        game = Game(client, event['game']['id'])

