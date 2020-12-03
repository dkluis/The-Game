# This is a sample Python script.

# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from Entities import Player, restore_all_players, store_all_players
from Utils import logging


def play_the_game():
    print(f'Welcome to the Players')
    for player in players:
        print(f'Hi, {player.get_nick_name()}, your current score is: {player.get_score()} '
              f'and your entity is a {player.get_race()}')
    
    
if __name__ == '__main__':
    log = logging(caller='The Game', filename='TheGame')
    log.start()
    players = restore_all_players()
    play_the_game()
    store_all_players(players)
    log.end()
