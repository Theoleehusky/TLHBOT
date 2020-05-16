import berserk
from Game import Game

session = berserk.TokenSession('rwerWlJJoAuY1Wug')
client = berserk.Client(session=session)


client.challenges.create('theoleehusky', False, 3000, 3, color='white')

for event in client.bots.stream_incoming_events():
    print(event)
    # if event['type'] == 'challenge':
    #     if should_accept(event):
    #         client.bots.accept_challenge(event['challenge']['id'])
    #     elif is_polite:
    #         client.bots.decline_challenge(event['id'])
    if event['type'] == 'gameStart':
        game = Game(client, event['game']['id'])

