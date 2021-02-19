from GameUI import *
from Utils import sqliteDB, logging

db = sqliteDB()
logfile = logging(caller='tables', filename='tables')

main = Main_Window(name='Main', label='', width=2000, height=1200, center=True, primary=True, include_main_menu=True)
win1 = Window(name='Win1', label='Win1', x_pos=50, y_pos=50, width=500, height=250)

player_crud = Crud_Window(name='crudPlayers', label='Maintain Players', logfile=logfile,
                          x_pos=150, y_pos=150, width=1200, height=500, button_label='Player',
                          table='players', db=db, add_to_menu=True, menu_name='Main')
player_crud.refresh_table()

main.start()
