from GameUI import *
from Entities import Player, restore_all_players, store_all_players
from Utils import logging
from dearpygui.core import *
from dearpygui.simple import *

'''UI Section'''


def list_players(sender, data):
    with window(name='Players List'):
        add_table('Players List')


def start_ui():
    start_dearpygui(primary_window='Game Window')


def stop_ui(sender, data):
    stop_dearpygui()
    break_down_the_game(sender, data)


def game_window():
    with window(name='Game Window', on_close=break_down_the_game):
        with menu_bar(name='Menu Bar'):
            add_menu_item(name='End Game', callback=stop_ui)
            add_menu_item(name='List Players', callback=list_players)


def set_up_the_game():
    game_window()
    

def break_down_the_game(sender, data):
    log.write(f'Closed the game window')
    store_all_players(players)
    log.end()
    quit()
    
    
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
    set_up_the_game()
    start_ui()


