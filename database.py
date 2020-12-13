from GameUI import *

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
    game_db.close()
    logfile.end()
    

def database_window():
    with window(name='Database Window'):
        with menu_bar(name='Menu Bar'):
            with menu(name='File'):
                add_menu_item(name='Quit', shortcut='ctl Q', callback=stop_ui)
            with menu(name='Tables'):
                add_menu_item(name='Players', callback=players)
                add_menu_item(name='Nick Names', callback=nick_names)
                add_menu_item(name="Table Id's", callback=table_ids)
                add_menu_item(name='Games', callback=games)
                add_menu_item(name='...')
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
    if not does_item_exist('crudPlayers'):
        player_crud = Crud_Window(name='crudPlayers', label='Maintain Players', logfile=logfile,
                                  x_poss=50, y_pos=50, width=1200, height=500,
                                  table='players', db=game_db)
        player_crud.refresh_table()
        
    
def nick_names(sender, data):
    log_info(f'nick names: Sender {sender}, Data {data}')
    if not does_item_exist('crudNickNames'):
        nick_names_crud = Crud_Window(name='crudNickNames', label='Maintain Nick Names', logfile=logfile,
                                      x_poss=100, y_pos=100, width=1200, height=500,
                                      table='nick_names', fields=[('Nick Name', 'str'), ('Id', 'int')], db=game_db)
        nick_names_crud.refresh_table()
    
    
def table_ids(sender, data):
    log_info(f'table_ids: Sender {sender}, Data {data}')
    if not does_item_exist('crudTableIds'):
        table_ids_crud = Crud_Window(name='crudTableIds', label="Maintain Table Id's", logfile=logfile,
                                     x_poss=150, y_pos=150, width=1200, height=500,
                                     table='table_ids', fields=[('Table Name', 'str'), ('Last Id', 'int')], db=game_db)
        table_ids_crud.refresh_table()

    
def games(sender, data):
    log_info(f'abilities: Sender {sender}, Data {data}')
    if not does_item_exist('crudGames'):
        games_crud = Crud_Window(name='crudGames', label='Maintain Games', logfile=logfile,
                                 x_poss=250, y_pos=250, width=1200, height=500,
                                 table='games', fields=[('Game Id', 'int'), ('Name', 'str')], db=game_db)
        games_crud.refresh_table()
        

if __name__ == '__main__':
    logfile = logging(caller='Database', filename='TheGame')
    logfile.start()
    logfile.write(f'Opening the Database Maintenance window')
    game_db = sqliteDB()
    
    start_ui()
