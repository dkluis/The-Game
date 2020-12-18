"""

    Library to handle DPG Tables

"""

from dearpygui.core import *
from Utils import logging


class Table:
    """
    
        Handle DPG Table functions
    
    """
    def __init__(self, name='', header=[], parent='', selection_list=False, click_callback='', logfile=logging):
        self.name = name
        self.parent = parent
        self.header = header
        self.selection_list = selection_list
        self.last_selection = []
        self.click_callback = click_callback
        self.logfile = logfile
        self.__initialize__()
     
    def __initialize__(self):
        if not self.header and not self.field_info:
            self.logfile.write(f'Table Init Failed:  No Header and Field Info value were given', 0)
            return False
        elif not self.header:
            #  ToDo build the header from the field_info
            pass
        add_table(self.name, self.header, parent=self.parent, height=0, callback=self.click)
        
    def get_field_names(self):
        return self.header
    
    def get_row_cell_value(self, row_cell=[]):
        return get_table_item(self.name, row_cell[0], row_cell[1])
        
    def get_row_values(self, row):
        row_values = []
        for idx in range(0, len(self.header)):
            row_values.append(self.get_row_cell_value([row, idx]))
        return row_values
    
    def refresh(self, table_data):
        set_table_data(self.name, table_data)
        
    def click(self, sender, data):
        self.click_callback()
        selected_row_cell = get_table_selections(self.name)
        if not self.selection_list and selected_row_cell:
            self.clear_previous_selections()
        return selected_row_cell
    
    def clear_previous_selections(self):
        rows_cells = get_table_selections(self.name)
        if len(rows_cells) < 2:
            self.last_selection = rows_cells[0]
            return
        if self.selection_list:
            pass
        else:
            for row_cell in rows_cells:
                if row_cell != self.last_selection:
                    self.last_selection = row_cell
                    break
        rows_cells = get_table_selections(self.name)
        for row_cell in rows_cells:
            set_table_selection(self.name, row_cell[0], row_cell[1], False)
        set_table_selection(self.name, self.last_selection[0], self.last_selection[1], True)

    
class crudTable(Table):
    """
    
        Handle all crudWindow table functions
    
    """
    def __init__(self):
        pass