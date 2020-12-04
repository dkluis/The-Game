from Entities import restore_all_players, store_all_players
from Utils import logging
from dearpygui.core import *
from dearpygui.simple import *


def list_players(sender, data):
    log.write(f'List Players Sender {sender} Data {data}')
    if not does_item_exist('Players List'):
        with window(name='Players List'):
            add_table('Players Table', headers=['First', 'Last', 'Nick', 'Id'])
            

def do_something(sender, data):
    player = str(sender).split('##')[1]
    log.write(f'Do Something clicked by {player}')


def start_ui():
    start_dearpygui(primary_window='Game Window')


def stop_ui(sender, data):
    log_warning(f'Stop UI Sender {sender} Data {data}')
    stop_dearpygui()
    break_down_the_game(sender, data)


def game_window():
    with window(name='Game Window', on_close=break_down_the_game):
        with menu_bar(name='Menu Bar'):
            add_menu_item(name='End Game', callback=stop_ui)
            add_menu_item(name='List Players', callback=list_players)

    play_the_game()
    

def set_up_the_game():
    game_window()
    show_debug()
    

def break_down_the_game(sender, data):
    log.write(f'Closed the game window.  Sender {sender}, Data {data}')
    store_all_players(players)
    log.end()
    quit()
    
    
def play_the_game():
    print(f'Welcome to the Players')
    for player in players:
        nick = player.get_nick_name()
        with window(name=f'{nick}##window'):
            with tab_bar(name=f'Tabs##{nick}'):
                add_tab(name=f'Actions##{nick}')
                add_button(f'Do Something##{nick}', callback=do_something)
                end()
                add_tab(name=f'Config##{nick}')
                add_button(name=f'Change Entity##{nick}')
                end()


if __name__ == '__main__':
    log = logging(caller='The Game', filename='TheGame')
    log.start()
    players = restore_all_players()
    log.write(f'Opening in the game window')
    set_up_the_game()
    start_ui()
