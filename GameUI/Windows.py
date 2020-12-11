"""
    Library to help generate and manage DPG Windows and Widgets
"""

from dearpygui.core import *
from Utils import logging
from Utils import sqliteDB


class Window:
    def __init__(self, name='', label='',
                 x_poss=100, y_pos=100,
                 width=1000, height=750,
                 logfile=logging):
        
        self.log = logfile
        self.name = name
        self.label = label
        self.x_pos = x_poss
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.__create_window()
        
    def __create_window(self):
        if not does_item_exist(self.name):
            add_window(self.name,
                       width=self.width, height=self.height,
                       x_pos=self.x_pos, y_pos=self.y_pos,
                       label=self.label)
            end()
            set_main_window_title('The Game')


class Crud_Window(Window):
    def __init__(self, name, label,
                 width=500, height=500,
                 x_poss=100, y_pos=100,
                 logfile=logging,
                 table='', fields=[], db=sqliteDB):

        super().__init__(name=name, label=label,
                         x_poss=x_poss, y_pos=y_pos,
                         width=width, height=height,
                         logfile=logfile)

        self.table = table
        self.fields = fields
        self.__maintain_records__()
        self.__create_table__()
        self.db = db
        
    def __maintain_records__(self):
        add_button(name=f'Create Player##{self.name}', parent=self.name)
        add_same_line(parent=self.name)
        add_button(name=f'Update Player##{self.name}', parent=self.name)
        add_same_line(parent=self.name)
        add_button(name=f'Delete Player##{self.name}', parent=self.name)
        add_separator(name=f'##{self.name}sep1', parent=self.name)
        
    def __create_table__(self):
        add_button(name=f'refresh##{self.name}{self.table}', callback=self.refresh_table, parent=self.name)
        add_separator(name=f'##{self.name}{self.table}sep1', parent=self.name)
        add_table(name=f'table##{self.name}{self.table}', headers=self.fields, parent=self.name, width=0, height=0)

    def refresh_table(self, sender, data):
        sql = f'select * from {self.table}'
        result = self.db.execute_sql(sql)
        self.log.write(f'Result is {result}')
        table_data = []
        for result_rec in result:
            table_row = []
            for field in result_rec:
                table_row.append(field)
            table_data.append(table_row)
        set_table_data(f'table##{self.name}{self.table}', table_data)
