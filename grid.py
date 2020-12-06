from dearpygui.core import *
from dearpygui.simple import *

set_main_window_size(width=550, height=550)
set_main_window_title('The Game')


def grid(sender, data):
    win_size = get_main_window_size()
    canvas_height = win_size[1]
    canvas_width = win_size[0]
    if win_size[0] < 550:
        canvas_width = 550
    if win_size[1] < 550:
        canvas_height = 550
    # set_main_window_size(width=canvas_width, height=canvas_height)
    
    cell_width = 32
    cell_height = 32
    
    cells_wanted = get_value('no_cells')
    
    cell_size = int(win_size[0]/cells_wanted)
    cell_height = cell_size
    cell_width = cell_size
    
    n_cells_x = canvas_width / cell_width
    n_cells_y = canvas_height / cell_height
    
    if n_cells_y >= n_cells_x:
        n_cells = int(n_cells_x) - 1
    else:
        n_cells = int(n_cells_y) - 1
        
    draw_width = cell_width * n_cells
    draw_height = cell_height * n_cells
    
    # draw_width = cell_width * int(n_cells_x)
    # draw_height = cell_width * int(n_cells_y)
    
    # Create a window that holds the canvas
    if does_item_exist("GridWindow"):
        delete_item('GridWindow')
        
    with window("GridWindow", autosize=True, no_title_bar=True, no_scrollbar=True, x_pos=3, y_pos=3):
        set_style_window_border_size(0)
        print(canvas_width, canvas_height)
        # Create the canvas item to draw in
        add_drawing("GridCanvas", width=draw_width + 1, height=draw_height + 1)
    
        # cell_height = canvas_height/n_cells
        # cell_width = canvas_width/n_cells
    
        print(n_cells_x, n_cells_y, n_cells, cell_width, cell_height, draw_width, draw_height)
    
        # Draw all horizontal lines
        # Every line should start with the x coordinate being 0 on the far left, to the x coordinate on the far right,
        # in this case canvas_width.
        # Y coordinates are increased by cell_height in every step.
        # for y_idx in range(n_cells+1):
        for y_idx in range(n_cells + 1):
            draw_line("GridCanvas", [0, y_idx * cell_height], [draw_height, y_idx * cell_height], [255, 255, 255, 255], 1)
        
        # Vertical lines
        for x_idx in range(n_cells + 1):
            draw_line("GridCanvas", [x_idx * cell_width, 0], [x_idx * cell_width, draw_width], [0, 255, 0, 255], 1)
            
        print(get_style_window_padding())
        pad_y = int((win_size[1] - draw_height) / 2)
        pad_x = int((win_size[0] - draw_width) / 2)
        set_style_window_padding(pad_x -2, pad_y)
        print(get_style_window_padding())

    if does_item_exist('Cells'):
        delete_item('Cells')
    with window('Cells', width=375, height=100, x_pos=25, y_pos=50):
        add_input_int('Number of Cells')
        add_button('Update', callback=update_no_cells)
        

def update_no_cells(sender, data):
    set_value('no_cells', get_value('Number of Cells') + 1)
    grid(sender, data)
    
 
with window('Blank'):
    add_label_text('')
    

add_value('no_cells', 25)

set_resize_callback(grid, 'Blank')
start_dearpygui(primary_window='Blank')
