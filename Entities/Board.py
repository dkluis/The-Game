from math import sqrt
from dearpygui.core import does_item_exist, draw_polygon, add_drawing

from Utils import logging


class Hexagon:
    def __init__(self,
                 id_handle,
                 window_handle,
                 drawing_handle,
                 logfile=logging,
                 size=20,
                 thickness=13,
                 hor_offset=100.0,
                 ver_offset=50.0,
                 outline_color=[255, 0, 0, 255],
                 background_color=[]):
        self.id = id_handle
        self.window = window_handle
        self.drawing = drawing_handle
        self.size = size
        self.thickness = thickness
        self.horizontal_offset = hor_offset
        self.vertical_offset = ver_offset
        if len(background_color) == 0:
            self.use_background_color = False
        else:
            self.use_background_color = True
        self.background_color = background_color
        self.outline_color = outline_color
        self.coordinate_a = [0.0, 0.0]
        self.coordinate_b = [0.0, 0.0]
        self.coordinate_c = [0.0, 0.0]
        self.coordinate_d = [0.0, 0.0]
        self.coordinate_e = [0.0, 0.0]
        self.coordinate_f = [0.0, 0.0]
        self.center = [0.0, 0.0]
        self.top_bot_dist = 0.0
        self.left_right_dist = 0.0
        self.__calc_parameters()
        self.logfile = logfile
    
    def __calc_parameters(self):
        self.coordinate_a = self.size + self.horizontal_offset, self.size + self.vertical_offset
        self.coordinate_b = self.size / 2 + self.horizontal_offset, sqrt(3 * self.size) / 2 + self.vertical_offset
        self.coordinate_c = -self.size / 2 + self.horizontal_offset, sqrt(3 * self.size) / 2 + self.vertical_offset
        self.coordinate_d = -self.size + self.horizontal_offset, self.size + self.vertical_offset
        self.coordinate_e = -self.size / 2 + self.horizontal_offset, self.size + self.size - sqrt(
            3 * self.size) / 2 + self.vertical_offset
        self.coordinate_f = self.size / 2 + self.horizontal_offset, self.size + self.size - sqrt(
            3 * self.size) / 2 + self.vertical_offset
        # print(self.coordinate_a, self.coordinate_b, self.coordinate_c,
        #      self.coordinate_d, self.coordinate_e, self.coordinate_f, self.coordinate_a)
        # ToDo calc center
        self.top_bot_dist = sqrt(pow(self.coordinate_b[0] - self.coordinate_f[0], 2) +
                                 pow(self.coordinate_b[1] - self.coordinate_f[1], 2))
        self.left_right_dist = sqrt(pow(self.coordinate_f[0] - self.coordinate_e[0], 2) +
                                    pow(self.coordinate_f[1] - self.coordinate_e[1], 2))
        # print(f'tb {self.top_bot_dist}, lr {self.left_right_dist}')
    
    def draw(self):
        self.__calc_parameters()
        print('Draw', self.id, self.drawing)
        if not does_item_exist(self.drawing):
            print("Does not exit", self.drawing)
            self.logfile.write(f'The Drawing Handle does not exist', 0)
            add_drawing(self.drawing, parent=self.window, width=1100, height=1100)
        draw_polygon(self.drawing, [self.coordinate_a, self.coordinate_b, self.coordinate_c, self.coordinate_d,
                                    self.coordinate_e, self.coordinate_f, self.coordinate_a],
                     self.outline_color, thickness=self.thickness, tag=self.id)
