from dearpygui.core import *
from dearpygui.simple import *


class Board:
    def __init__(self, window_handle: str, drawing_handle: str, width: int, height: int):
        self.window = window_handle
        self.drawing = drawing_handle
        self.width = width
        self.height = height
        self.background_color = [150, 0, 0, 150]
        self.outline_color = [255, 255, 150, 150]
        self.rows = 10
        self.columns = 10

        # recommend taking tile into it's own class maybe?
        self.__tile_width = self.width / self.columns
        self.__tile_height = self.height / self.rows
        self.__tile_center_pos = [self.__tile_width/2, self.__tile_height/2]
            
    def update(self) -> None:
        # updating drawing and background size
        if does_item_exist(self.drawing):
            delete_item(self.drawing)

        self.width = get_item_width(self.window)
        self.height = get_item_height(self.window)
        
        # set_drawing_size(self.drawing, self.width, self.height)
        add_drawing(self.drawing, width=self.width, height=self.height, parent='Main')
        # Could not get the modify to work so, delete the drawing and also took out render and only call update now.
        # modify_draw_command(self.drawing, pmin=[0, 0], pmax=[self.width, self.height])
        
        # No code duplication anymore
        # code duplication below, def recommend to put into tile class so we can just call tile.render() and tile.update
        # here and above
        self.__tile_width = self.width / self.columns
        self.__tile_height = self.height / self.rows
        self.__tile_center_pos = [self.__tile_width / 2, self.__tile_height / 2]
        
        for row in range(0, self.rows):
            for column in range(0, self.columns):
                p_min = [self.__tile_center_pos[0] - self.__tile_width/2, self.__tile_center_pos[1] + self.__tile_height/2]
                p_max = [self.__tile_center_pos[0] + self.__tile_width/2, self.__tile_center_pos[1] - self.__tile_height/2]
                draw_rectangle(self.drawing, p_min, p_max, self.outline_color)
                self.__tile_center_pos[0] = self.__tile_center_pos[0] + self.__tile_width
            self.__tile_center_pos = [self.__tile_width/2, self.__tile_center_pos[1] + self.__tile_height]
            
# GUI window layouts


with window("Main", width=500, height=500):
    board = Board("Main", "game board", 500, 500)
    board.update()


# fixing style boarders and stuff to be 0
set_item_style_var("Main", mvGuiStyleVar_WindowPadding, [0, 0])
set_item_style_var("Main", mvGuiStyleVar_ItemSpacing, [0, 0])
set_item_style_var("Main", mvGuiStyleVar_ItemInnerSpacing, [0, 0])
set_item_style_var("Main", mvGuiStyleVar_WindowBorderSize, [0])


def resize_callback(sender, data):
    board.update()
    

set_resize_callback(handler="Main", callback=resize_callback)

# Not sure what this does and what it's purpose is????
enable_docking(dock_space=True)

start_dearpygui()