from Utils import logging
# from Utils import mariaDB

from dearpygui.core import *
from dearpygui.simple import *


def stop_ui_exit(sender, data):
    log.write(f'Stop Program: Sender {sender}, Data {data}')
    log.end()
    
        
def stop_ui(sender, data):
    stop_dearpygui()


def start_ui():
    database_window()
    set_exit_callback(callback=stop_ui_exit)
    start_dearpygui(primary_window='Database Window')


def database_window():
    with window(name='Database Window'):
        with menu_bar(name='Menu Bar'):
            add_menu_item(name='Quit', callback=stop_ui)
            add_menu_item(name='Players')
    
    show_debug()


if __name__ == '__main__':
    log = logging(caller='Database', filename='TheGame')
    log.start()
    log.write(f'Opening the Database Maintenance window')
    start_ui()
