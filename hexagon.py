from dearpygui.core import *
from dearpygui.simple import *
from math import sqrt

# Init the program
add_value('size', 100)
add_value('vertical_move', 200)
add_value('horizontal_move', 500)
add_value('New Size', 100)
add_value('New Vertical Offset', 200)
add_value('New Horizontal Offset', 500)
add_value('Fill Color', [255, 255, 255, 255])
add_value('Thickness', 1)


def change_thickness(sender, data):
    input_thickness = get_value('Thickness')
    print(input_thickness)
    set_value('Thickness', input_thickness)
    draw_the_hexagon()
    

def change_size(sender, data):
    input_size = get_value('New Size')
    print(input_size)
    set_value('size', input_size)
    draw_the_hexagon()


def change_vertical(sender, data):
    input_vertical = get_value('New Vertical Offset')
    print(input_vertical)
    set_value('vertical_move', input_vertical)
    draw_the_hexagon()


def change_horizontal(sender, data):
    input_vertical = get_value('New Horizontal Offset')
    print(input_vertical)
    set_value('horizontal_move', input_vertical)
    draw_the_hexagon()


def change_fill_color(sender, data):
    color = get_value('Hexagon Fill')
    set_value('Fill Color', color)
    print(color, get_value('Fill Color'))
    draw_the_hexagon()


def draw_the_hexagon():
    if does_item_exist('hexagon'):
        delete_item('hexagon')
    
    # set up the hexagon info
    size = get_value('size')
    vertical_factor = size
    vertical_move = get_value('vertical_move')
    horizontal_move = get_value('horizontal_move')
    fill_color = get_value('Hexagon Fill')
    thickness = get_value('Thickness')
    print(fill_color)
    # Rule the horizontal move needs to bigger than a
    
    ca = size + horizontal_move, vertical_factor + vertical_move
    cb = size / 2 + horizontal_move, sqrt(3 * size) / 2 + vertical_move
    cc = -size / 2 + horizontal_move, sqrt(3 * size) / 2 + vertical_move
    cd = -size + horizontal_move, vertical_factor + vertical_move
    ce = -size / 2 + horizontal_move, vertical_factor + size - sqrt(3 * size) / 2 + vertical_move
    cf = size / 2 + horizontal_move, vertical_factor + size - sqrt(3 * size) / 2 + vertical_move
    print(ca, cb, cc, cd, ce, cf, ca)
    
    add_drawing('hexagon', width=1000, height=1000, parent='main')
    draw_polygon("hexagon", [ca, cb, cc, cd, ce, cf, ca],
                 [255, 255, 255, 255], thickness=thickness)


with window('main'):
    draw_the_hexagon()

with window('Adjustments', autosize=True, x_pos=200, y_pos=800):
    add_input_int('Thickness', default_value=3)
    add_same_line()
    add_button('Implement Thickness', callback=change_thickness)
    add_input_int('New Size', default_value=50)
    add_same_line()
    add_button('Implement Size', callback=change_size)
    add_input_int('New Vertical Offset', default_value=100)
    add_same_line()
    add_button('Implement Vertical Offset', callback=change_vertical)
    add_input_int('New Horizontal Offset', default_value=250)
    add_same_line()
    add_button('Implement Horizontal Offset', callback=change_horizontal)
    add_color_picker3('Hexagon Fill', display_hsv=False, no_inputs=True)
    add_same_line()
    add_button('Implement Fill Color', callback=change_fill_color)

set_main_window_size(1200, 1200)
start_dearpygui(primary_window='main')
