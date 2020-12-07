from Entities import *
from Utils import logging
from dearpygui.core import *
from dearpygui.simple import *

log = logging(caller='board.py', filename='board')


def do_hexagon_draw(sender, data):
    board_array = []
    hex_size = 30
    hexagon_info = Hexagon('info', 'Main', 'Board', log, size=hex_size)
    top_bot_dist = hexagon_info.top_bot_dist
    left_right_dist = (hex_size + hex_size / 2) / 2
    row_height = int(1000/top_bot_dist)
    row_len = int(1000/(left_right_dist * 2))
    col_len = int(1000/top_bot_dist)

    for idx in range(0, row_height):
        vo = top_bot_dist * idx
        ho = left_right_dist * 0
        board_array.append(Hexagon(f'A{idx}', 'Main', 'Board', log, size=hex_size,
                                   ver_offset=vo, hor_offset=ho, thickness=1))
        board_array[idx].draw()
    print(len(board_array))

    for idx in range(0, row_height):
        vo = top_bot_dist * idx
        ho = left_right_dist * 2
        board_array.append(Hexagon(f'B{idx}', 'Main', 'Board', log, size=hex_size,
                                   ver_offset=vo + top_bot_dist / 2, hor_offset=ho, thickness=1))
        board_array[idx + row_height].draw()
    print(len(board_array))

    for idx in range(0, row_height):
        vo = top_bot_dist * idx
        ho = left_right_dist * 4
        board_array.append(Hexagon(f'C{idx}', 'Main', 'Board', log, size=hex_size,
                                   ver_offset=vo, hor_offset=ho, thickness=1))
        board_array[idx + row_height * 2].draw()
    print(len(board_array))

    for idx in range(0, row_height):
        vo = top_bot_dist * idx
        ho = left_right_dist * 6
        board_array.append(Hexagon(f'D{idx}', 'Main', 'Board', log, size=hex_size,
                                   ver_offset=vo + top_bot_dist / 2, hor_offset=ho, thickness=1))
        board_array[idx + row_height * 3].draw()
    print(len(board_array))
    
    for idx in range(0, row_height):
        vo = top_bot_dist * idx
        ho = left_right_dist * 8
        board_array.append(Hexagon(f'E{idx}', 'Main', 'Board', log, size=hex_size,
                                   ver_offset=vo, hor_offset=ho, thickness=1))
        board_array[idx + row_height * 4].draw()
    print(len(board_array))
    
    print(f'row len {row_len}, column len {col_len}')
    

with window('Main', width=1000, height=1000, horizontal_scrollbar=True, x_pos=0, y_pos=0,
            label='The Board'):
    log_info(f'Main')
    do_hexagon_draw('', 'Main')

set_main_window_title('The Game')
set_main_window_size(1500, 1500)
# show_logger()
# set_log_level(mvINFO)

start_dearpygui()
