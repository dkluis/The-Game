"""
    Library to help generate and manage DPG Windows and Widgets
"""

from dearpygui.simple import *
from screeninfo import get_monitors

from Entities import *


class Window:
    """
        Generate a Window
        
    """
    
    def __init__(self, name='', label='', parent='',
                 x_pos=100, y_pos=100,
                 width=1000, height=750,
                 logfile=logging):
        """
            Initialize a Window
            
        :param name:    DPG Name
        :param label:   Window Title
        :param parent:  DPG Parent container
        :param x_pos:  Vertical top left position
        :param y_pos:   Horizontal top right position
        :param width:   Window width
        :param height:  Window height
        :param logfile: The Game Logfile
        """
        self.log = logfile
        self.name = name
        self.label = label
        self.x_pos = x_pos
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
            with window(self.name,
                        width=self.width, height=self.height,
                        x_pos=self.x_pos, y_pos=self.y_pos,
                        label=self.label):
                with menu_bar(f'##MB{self.name}', show=False):
                    pass
        else:
            with window(self.name,
                        width=self.width, height=self.height,
                        x_pos=self.x_pos, y_pos=self.y_pos,
                        label=self.label, parent=self.parent):
                with menu_bar(f'##MB{self.name}', show=False):
                    pass
        set_theme('Gold')
    
    def show(self):
        if does_item_exist(self.name):
            show_item(self.name)
        else:
            self.__create_window__()


class Main_Window(Window):
    def __init__(self, name, label,
                 width=500, height=500,
                 x_pos=100, y_pos=100, center=False,
                 logfile=logging,
                 primary=False,
                 include_main_menu=False):
        """
        
            Make the main window and inherit the Window class
        
        :param name:
        :param label:
        :param width:
        :param height:
        :param x_pos:
        :param y_pos:
        :param center:
        :param logfile:
        :param primary:
        :param include_main_menu:
        """
        super().__init__(name=name, label=label,
                         x_pos=x_pos, y_pos=y_pos,
                         width=width, height=height,
                         logfile=logfile)
        self.primary = primary
        self.include_menu = include_main_menu
        if center:
            self.__center__()
    
    def start(self):
        """
            
            Start DPG
            
        :return:
        """
        # ToDo figure out catching the kill of the main window and gracefully shutdown the app
        # set_exit_callback(callback=self.stop_functions)
        set_log_level(mvINFO)
        set_main_window_size(width=self.width, height=self.height)
        set_main_window_pos(x=self.x_pos, y=self.y_pos)
        set_main_window_title(self.name)
        
        if self.include_menu:
            with menu(name='Developer', parent=f'##MB{self.name}'):
                add_menu_item('DPG Debugger', callback=show_debug)
                add_menu_item(name='DPG Logger', callback=show_logger)
                add_menu_item(name='DPG Doc', callback=show_documentation)
            with menu(name='File', parent=f'##MB{self.name}', before='Developer'):
                add_menu_item(name='Quit', shortcut='ctl Q', callback=self.stop)
            show_item(f'##MB{self.name}')
        
        if self.primary:
            start_dearpygui(primary_window=self.name)
        else:
            start_dearpygui()
    
    def stop(self, sender, data):
        """
        
            Stop DPG
        
        :param sender:
        :param data:
        :return:
        """
        stop_dearpygui()
    
    def stop_functions(self):
        """
        
            Gracefully shutdown the App
        
        :return:
        """
        pass
    
    def __center__(self):
        monitors = get_monitors()
        self.x_pos = int((monitors[0].width - self.width) / 2)
        self.y_pos = int((monitors[0].height - self.height) / 2)


class Crud_Window(Window):
    """
            Creating a maintenance program for a Table
            
    """
    
    def __init__(self, name, label,
                 width=500, height=500,
                 x_pos=100, y_pos=100,
                 logfile=logging,
                 button_label='',
                 table='', fields=[],
                 db=sqliteDB,
                 add_to_menu=False, menu_name=''):
        """
        Inherit the window class
        
        :param name:    DPG Name
        :param label:   Window Title
        :param x_pos:   Vertical top left position
        :param y_pos:   Horizontal top right position
        :param width:   Window width
        :param height:  Window height
        :param logfile: The Game Logfile
        
        :param table:       The table to be maintained
        :param fields:      The fields to use
        :param db:          The sqliteDB object
        :param add_to_menu  Add to the main menu
        :param menu_name    Menu to add it to
        """
        
        super().__init__(name=name, label=label,
                         x_pos=x_pos, y_pos=y_pos,
                         width=width, height=height,
                         logfile=logfile)
        
        self.db = db
        self.table = table
        self.table_button = button_label
        self.entity = self.__get_table_object__()
        self.fields = fields
        self.field_info = list
        if add_to_menu:
            self.__add_to_menu__(menu_name)
        self.__get_field_info__()
        self.__maintain_records__()
    
    def __add_to_menu__(self, menu_name):
        if not does_item_exist('tables'):
            with menu(name='tables', label='Maintain Tables', parent=f'##MB{menu_name}'):
                add_menu_item(name=f'{self.table_button}s##tables')
        else:
            add_menu_item(name=f'{self.table_button}s##tables', parent=f'##MB{menu_name}')
    
    def __maintain_records__(self):
        """
                Building the DPG Info for the screen setup
        :return:
        """
        for field in self.field_info:
            if 'text' in str(field['type']).lower():
                add_input_text(f'{self.table}.{field["name"]}', label=f':{field["name"]} ',
                               width=300, parent=self.name)
            elif str(field['type']).lower() == 'integer':
                add_input_int(f'{self.table}.{field["name"]}', label=f':{field["name"]} ',
                              width=200, step=0, parent=self.name)
        add_button(name=f'Create {self.table_button}##{self.name}', parent=self.name)
        add_same_line(parent=self.name)
        add_button(name=f'Update {self.table_button}##{self.name}', parent=self.name, enabled=False)
        add_same_line(parent=self.name)
        add_button(name=f'Delete {self.table_button}##{self.name}', parent=self.name, enabled=False)
        add_same_line(parent=self.name)
        add_button(name=f'Clear##{self.name}', parent=self.name, callback=self.__reset_inputs__)
        add_separator(name=f'##{self.name}sep1', parent=self.name)
        self.__create_table__()
    
    def __reset_inputs__(self, sender, data):
        self.__toggle_button_enabled__(f'Create {self.table_button}##{self.name}')
        self.__toggle_button_enabled__(f'Update {self.table_button}##{self.name}')
        self.__toggle_button_enabled__(f'Delete {self.table_button}##{self.name}')
        row_cell = get_table_selections(self.table)
        for rc in row_cell:
            set_table_selection(sender, rc[0], rc[1], False)
    
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
        add_table(name=f'table##{self.name}{self.table}', headers=header, parent=self.name, width=0, height=0,
                  callback=self.__table_click__)
    
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
    
    def __table_click__(self, sender, data):
        row_cell = get_table_selections(sender)
        row = row_cell[len(row_cell) - 1][0]
        
        if len(row_cell) > 1:
            for rc in row_cell:
                set_table_selection(sender, rc[0], rc[1], False)
        
        for cell in range(0, int(len(self.field_info))):
            # print(f'R {row}, C {cell}')
            # set_table_selection(sender, row, cell, True)
            if str(self.field_info[cell]['type']).lower() == 'integer':
                set_value(f'{self.table}.{self.field_info[cell]["name"]}', int(get_table_item(sender, row, cell)))
                if self.field_info[cell]['name'][-3:] == '_id':
                    self.__toggle_button_enabled__(f'Create {self.table_button}##{self.name}')
                    self.__toggle_button_enabled__(f'Update {self.table_button}##{self.name}')
                    self.__toggle_button_enabled__(f'Delete {self.table_button}##{self.name}')
                    configure_item(f'{self.table}.{self.field_info[cell]["name"]}', readonly=True)
            else:
                set_value(f'{self.table}.{self.field_info[cell]["name"]}', get_table_item(sender, row, cell))
    
    def __get_table_object__(self):
        print(f'Get Table Object {self.table}')
        if self.table == 'players':
            entity = Player()
        elif self.table == 'table_ids':
            entity = ()
        return entity
    
    def __get_field_info__(self):
        self.field_info = self.db.get_table_info(self.table)
