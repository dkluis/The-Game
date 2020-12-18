"""

    Testing the table class

"""
from dearpygui.core import *
from Utils import Table
from GameUI import Window


class click_callback:
    #  function to show a function pass to a the class table for the click event
    def __init__(self):
        print(f'Here is the call back function passed in')


click = click_callback
table_header = ['Cell 0', 'Cell 1', 'Cell 2']
table_content = []
for row in range(0, 10):
    row_cell = []
    for cell in range(0, 3):
        row_cell.append(f'Cell Value {cell} in Row {row}')
    table_content.append(row_cell)
# print(table_content)

window = Window(name='test_table', label='Test Table')
test_table = Table(name='table1', parent='test_table', header=table_header,
                   click_callback=click, selection_list=False)
test_table.refresh(table_content)

print('get value for 0, 0 -->', test_table.get_row_cell_value([0, 0]))
print('get value for 3, 2 -->', test_table.get_row_cell_value([3, 2]))
print('get field names -->', test_table.get_field_names())
print('get all values for row 5', test_table.get_row_values(5))

start_dearpygui()
