"""
    Library to help generate and manage DPG Windows and Widgets
"""

from dearpygui.core import *
from Utils import logging
from Utils import sqliteDB


class Window:
    """
        Generate a Window
        
    """
    
    def __init__(self, name='', label='', parent='',
                 x_poss=100, y_pos=100,
                 width=1000, height=750,
                 logfile=logging):
        """
            Initialze a Window
            
        :param name:    DPG Name
        :param label:   Window Title
        :param parent:  DPG Parent container
        :param x_poss:  Vertical top left position
        :param y_pos:   Horizontal top right position
        :param width:   Window width
        :param height:  Window height
        :param logfile: The Game Logfile
        """
        self.log = logfile
        self.name = name
        self.label = label
        self.x_pos = x_poss
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.parent = parent
        self.__create_window__()
    
    def __create_window__(self):
        """
                Defining the DPG info and creating the window
                
        :return:
        """
        if self.parent == '':
            add_window(self.name,
                       width=self.width, height=self.height,
                       x_pos=self.x_pos, y_pos=self.y_pos,
                       label=self.label)
            end()
        else:
            add_window(self.name,
                       width=self.width, height=self.height,
                       x_pos=self.x_pos, y_pos=self.y_pos,
                       label=self.label, parent=self.parent)
            end()
        set_main_window_title(self.name)


class Crud_Window(Window):
    """
            Creating a maintenance program for a Table
            
    """
    
    def __init__(self, name, label,
                 width=500, height=500,
                 x_poss=100, y_pos=100,
                 logfile=logging,
                 table='', fields=[], db=sqliteDB):
        """
        Inherit the window class
        
        :param name:    DPG Name
        :param label:   Window Title
        :param x_poss:  Vertical top left position
        :param y_pos:   Horizontal top right position
        :param width:   Window width
        :param height:  Window height
        :param logfile: The Game Logfile
        
        :param table:   The table to be maintained
        :param fields:  The fields to use
        :param db:      The sqliteDB object
        """
        
        super().__init__(name=name, label=label,
                         x_poss=x_poss, y_pos=y_pos,
                         width=width, height=height,
                         logfile=logfile)
        
        self.db = db
        self.table = table
        self.fields = fields
        self.field_info = list
        self.__get_field_info__()
        self.__maintain_records__()
    
    def __maintain_records__(self):
        """
                Building the DPG Info for the screen setup
        :return:
        """
        for field in self.field_info:
            if 'text' in str(field['type']).lower():
                add_input_text(f'input_str##{self.table}.{field["name"]}', label=f':{field["name"]} ',
                               width=300, parent=self.name)
            elif str(field['type']).lower() == 'integer':
                add_input_int(f'input_int##{self.table}.{field["name"]}', label=f':{field["name"]} ',
                              width=200, step=0, parent=self.name)
        add_button(name=f'Create Player##{self.name}', parent=self.name)
        add_same_line(parent=self.name)
        add_button(name=f'Update Player##{self.name}', parent=self.name, enabled=False)
        add_same_line(parent=self.name)
        add_button(name=f'Delete Player##{self.name}', parent=self.name, enabled=False)
        add_separator(name=f'##{self.name}sep1', parent=self.name)
        self.__create_table__()
    
    def __toggle_button_enabled__(self, button):
        config = get_item_configuration(button)
        if config['enabled']:
            configure_item(button, enabled=False)
        else:
            configure_item(button, enabled=True)
    
    def __create_table__(self):
        """
                Building the view of the table for the records to be shown
        :return:
        """
        add_button(name=f'refresh##{self.name}{self.table}', callback=self.refresh_table, parent=self.name)
        add_separator(name=f'##{self.name}{self.table}sep1', parent=self.name)
        header = []
        for head in self.field_info:
            header.append(head['name'])
        add_table(name=f'table##{self.name}{self.table}', headers=header, parent=self.name, width=0, height=0)
    
    def refresh_table(self, sender='', data=''):
        """
                Get the data from the database and show in the table view
        :param sender: DPG Info - not used
        :param data:   DPG Info - not used
        :return:
        """
        sql = f'select * from {self.table}'
        result = self.db.execute_sql(sql)
        self.log.write(f'Result is {result}')
        table_data = []
        for result_rec in result:
            table_row = []
            for field in result_rec:
                if not field:
                    field = ''
                table_row.append(field)
            table_data.append(table_row)
        set_table_data(f'table##{self.name}{self.table}', table_data)
        
    def __get_field_info__(self):
        self.field_info = self.db.get_table_info(self.table)

