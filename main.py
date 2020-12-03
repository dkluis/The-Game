from Entities import Player, restore_all_players, store_all_players
from Utils import logging
from dearpygui.core import *
from dearpygui.simple import *

import os


def play_the_game():
    print(f'Welcome to the Players')
    for player in players:
        print(f'Good to have you back, {player.get_nick_name()}, your current score is: {player.get_score()} '
              f'and your entity is a {player.get_race()}')
    
    
if __name__ == '__main__':
    log = logging(caller='The Game', filename='TheGame')
    log.start()
    players = restore_all_players()
    log.write(f'Opening in the game window')

    # ToDo set_up_the_game()
    start_dearpygui(primary_window="Game Window")
    # Playing the game is within the Game Window

    log.write(f'Closed the game window')
    store_all_players(players)
    stop_dearpygui()
    log.end()
    quit()
