from Entities import *
from Utils import logging
from dearpygui.core import *
from dearpygui.simple import *

log = logging(caller='board.py', filename='TheGame')


def do_hexagon_draw(sender, data):
    board_array = []
    hex_size = 30
    hexagon_info = Hexagon('info', 'Main', 'Board', log, size=hex_size)
    top_bot_dist = hexagon_info.top_bot_dist
    left_right_dist = (hex_size + hex_size / 2) / 2
    row_height = int(1000 / top_bot_dist)
    row_len = int(1000 / (left_right_dist * 2))
    col_len = int(1000 / top_bot_dist)
    
    print(top_bot_dist, left_right_dist)
    
    for idx in range(0, row_height):
        vo = top_bot_dist * idx
        ho = left_right_dist * 0 + hexagon_info.vertical_offset
        board_array.append(Hexagon(f'A{idx}', 'Main', 'Board', log, size=hex_size,
                                   ver_offset=vo, hor_offset=ho, thickness=1))
        board_array[idx].draw()
    print(len(board_array))
    
    for idx in range(0, row_height):
        vo = top_bot_dist * idx
        ho = left_right_dist * 2 + hexagon_info.vertical_offset
        board_array.append(Hexagon(f'B{idx}', 'Main', 'Board', log, size=hex_size,
                                   ver_offset=vo + top_bot_dist / 2, hor_offset=ho, thickness=1))
        board_array[idx + row_height].draw()
    print(len(board_array))
    
    for idx in range(0, row_height):
        vo = top_bot_dist * idx
        ho = left_right_dist * 4 + hexagon_info.vertical_offset
        board_array.append(Hexagon(f'C{idx}', 'Main', 'Board', log, size=hex_size,
                                   ver_offset=vo, hor_offset=ho, thickness=1))
        board_array[idx + row_height * 2].draw()
    print(len(board_array))
    
    for idx in range(0, row_height):
        vo = top_bot_dist * idx
        ho = left_right_dist * 6 + hexagon_info.vertical_offset
        board_array.append(Hexagon(f'D{idx}', 'Main', 'Board', log, size=hex_size,
                                   ver_offset=vo + top_bot_dist / 2, hor_offset=ho, thickness=1))
        board_array[idx + row_height * 3].draw()
    print(len(board_array))
    
    for idx in range(0, row_height):
        vo = top_bot_dist * idx
        ho = left_right_dist * 8 + hexagon_info.vertical_offset
        board_array.append(Hexagon(f'E{idx}', 'Main', 'Board', log, size=hex_size,
                                   ver_offset=vo, hor_offset=ho, thickness=1))
        board_array[idx + row_height * 4].draw()
    print(len(board_array))
    
    print(f'row len {row_len}, column len {col_len}')


def do_board_draw_example(sender, data):
    board = Board(log)
    hex_size = 30
    
    hexagon_info = Hexagon('info', '', '', log, size=hex_size, thickness=1)
    top_bot_dist = hexagon_info.top_bot_dist
    left_right_dist = hexagon_info.left_right_dist
    vertical_offset = hexagon_info.vertical_offset
    horizontal_offset = hexagon_info.horizontal_offset
    log.write(f'Top Bottom distance {top_bot_dist} and Left Right distance {left_right_dist}')
    log.write(f'Vertical offset {vertical_offset}, Horizontal offset {horizontal_offset}')
    del hexagon_info
    
    clear_drawing('Example')
    hexagon_1 = Hexagon('00#00', 'Main', 'Example', log, size=hex_size, thickness=1,
                        hor_offset=get_value('h1_h'), ver_offset=get_value('h1_v'))
    hexagon_2 = Hexagon('01#12', 'Main', 'Example', log, size=hex_size, thickness=2, hor_offset=300, ver_offset=300)
    board.add('info', hexagon_1)
    board.add('info2', hexagon_2)
    result = board.items()
    for hexagon in result:
        hexagon.draw()
        
    hexagon_1.fill(get_value('c_f'))
    hexagon_2.draw_cirle(get_value('c_c'))
    hexagon_1.draw_cirle(get_value('c_c'))
    hexagon_1.report()
    hexagon_2.report()


def do_board_draw():
    board = Board(log)
    hex_size = 30
    hexagon_info = Hexagon('info', '', '', log, size=hex_size, thickness=1)
    top_bot_dist = hexagon_info.top_bot_dist
    left_right_dist = (hex_size + hex_size / 2) / 2
    vertical_offset = hexagon_info.vertical_offset
    horizontal_offset = hexagon_info.horizontal_offset
    log.write(f'Top Bottom distance {top_bot_dist} and Left Right distance {left_right_dist}')
    log.write(f'Vertical offset {vertical_offset}, Horizontal offset {horizontal_offset}')
    # del hexagon_info
    
    for row in range(0, 5):
        ho = (left_right_dist + hex_size) * (row + 1) + hex_size
        for col in range(0, 5):
            k = f'{row}##{col}'
            vo = top_bot_dist * (col + 1) + top_bot_dist
            board.add(k,
                      Hexagon(k, 'Main', 'Board', log,
                              size=hex_size, thickness=1, hor_offset=ho, ver_offset=vo))
            board.get(k).draw()
            board.get(k).report()
            print(row, col, k, vo, ho)
            
            
with window('Main', width=1000, height=1000, horizontal_scrollbar=True, x_pos=0, y_pos=0,
            label='The Board'):
    log_info(f'Main')
    

with window('Draw Example', label='Draw Example', x_pos=1010, y_pos=500, autosize=True):
    add_color_picker4('c_c', source='c_c', no_inputs=True, label='Circle Both', callback=do_board_draw_example)
    add_color_picker4('c_f', source='c_f', no_inputs=True, default_value=[255, 255, 255, 255], label='Fill Hex 1',
                      callback=do_board_draw_example)
    add_slider_int('h1', default_value=100, max_value=1000, min_value=30, source='h1_h', label='Horizontal Hex 1',
                   callback=do_board_draw_example)
    add_slider_int('v1', default_value=100, max_value=1000, min_value=0, source='h1_v', label='Vertical Hex 1',
                   callback=do_board_draw_example)
    add_button('Draw Them', callback=do_board_draw_example)
    
    
    #do_hexagon_draw('', 'Main')
    #do_board_draw()
    #do_board_draw_example()
    
    
    
set_main_window_title('The Game')
set_main_window_size(1500, 1500)
# show_logger()
# set_log_level(mvINFO)

start_dearpygui()
