from Utils import logging
from Utils import mariaDB

from dearpygui.core import *
from dearpygui.simple import *
from dearpygui.demo import show_demo


def start_ui():
    database_window()
    set_exit_callback(callback=stop_ui_exit)
    set_log_level(mvINFO)
    set_main_window_size(width=1600, height=1200)
    start_dearpygui(primary_window='Database Window')


def stop_ui(sender, data):
    stop_dearpygui()


def stop_ui_exit(sender, data):
    logfile.end()
    

def database_window():
    with window(name='Database Window'):
        with menu_bar(name='Menu Bar'):
            with menu(name='File'):
                add_menu_item(name='Quit', shortcut='ctl Q', callback=stop_ui)
            with menu(name='Tables'):
                add_menu_item(name='Players', callback=players)
                add_menu_item(name='Races', callback=races)
                add_menu_item(name='Classes', callback=classes)
                add_menu_item(name='Abilities', callback=abilities)
                add_menu_item(name='And More')
                add_popup()
            with menu(name='Views'):
                add_menu_item(name='Players##View')
            with menu(name='Developer'):
                add_menu_item('DPG Debugger', callback=dpg)
                add_menu_item(name='DPG Logger', callback=dpg)
                add_menu_item(name='DPG Doc', callback=dpg)
                add_menu_item(name='DPG Demo', callback=dpg)
                
                
def dpg(sender, data):
    log_info(f'DPG: Sender {sender}, Data {data}')
    if sender == 'DPG Demo':
        show_demo()
    elif sender == 'DPG Doc':
        show_documentation(sender, data)
    elif sender == 'DPG Logger':
        show_logger()
    elif sender == 'DPG Debugger':
        show_debug(sender, data)
    

def players(sender, data):
    log_info(f'players: Sender {sender}, Data {data}')
    
    
def races(sender, data):
    log_info(f'races: Sender {sender}, Data {data}')
    
    
def classes(sender, data):
    log_info(f'classes: Sender {sender}, Data {data}')
    
    
def abilities(sender, data):
    log_info(f'abilities: Sender {sender}, Data {data}')


if __name__ == '__main__':
    logfile = logging(caller='Database', filename='TheGame')
    logfile.start()
    logfile.write(f'Opening the Database Maintenance window')
    start_ui()
