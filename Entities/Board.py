from math import sqrt
from dearpygui.core import does_item_exist, draw_polygon, add_drawing, \
    draw_text, draw_circle, add_value, set_value, get_value

from Utils import logging


class Hexagon:
    def __init__(self,
                 id_handle=int,
                 window_handle=str,
                 drawing_handle=str,
                 logfile=logging,
                 size=20,
                 thickness=1,
                 hor_offset=0.0,
                 ver_offset=0.0,
                 outline_color=[255, 0, 0, 255]):
        self.id = id_handle
        self.window = window_handle
        self.drawing = drawing_handle
        self.size = size
        self.thickness = thickness
        self.horizontal_offset = hor_offset
        self.vertical_offset = ver_offset
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
        self.filled = False
        self.circled = False
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
        # self.logfile.write(self.coordinate_a, self.coordinate_b, self.coordinate_c,
        #      self.coordinate_d, self.coordinate_e, self.coordinate_f, self.coordinate_a)
        self.top_bot_dist = sqrt(pow(self.coordinate_b[0] - self.coordinate_f[0], 2) +
                                 pow(self.coordinate_b[1] - self.coordinate_f[1], 2))
        self.left_right_dist = (self.size + self.size / 2) / 2
        self.center = (self.coordinate_a[0] - self.coordinate_d[0]) / 2 + self.coordinate_d[0], \
                      (self.coordinate_e[1] - self.coordinate_c[1]) / 2 + self.coordinate_c[1]
        # self.logfile.write(self.top_bot_dist, self.left_right_dist, self.center)
    
    def draw(self):
        self.__calc_parameters()
        if not does_item_exist(self.drawing) and self.id != 0:
            self.logfile.write(f'The Drawing Handle does not exist', 0)
            add_drawing(self.drawing, parent=self.window, width=1100, height=1100)
        draw_polygon(self.drawing, [self.coordinate_a, self.coordinate_b, self.coordinate_c, self.coordinate_d,
                                    self.coordinate_e, self.coordinate_f, self.coordinate_a],
                     self.outline_color, thickness=self.thickness, tag=self.id)
        self.logfile.write(f'Drawing Hexagon {self.id} with tag {self.id}')
        
    def fill(self, fillcolor=[255, 255, 255, 255]):
        draw_polygon(self.drawing, [self.coordinate_a, self.coordinate_b, self.coordinate_c, self.coordinate_d,
                                    self.coordinate_e, self.coordinate_f, self.coordinate_a],
                     self.outline_color, thickness=0, fill=fillcolor, tag=self.id)
        self.filled = True
        self.logfile.write(f'Filling Hexagon {self.id} with tag {self.id} and color {fillcolor}')
        
    def draw_cirle(self, circle_color=[]):
        if len(circle_color) == 0:
            circle_color = self.outline_color
        draw_circle(self.drawing, self.center, radius=5.0, color=circle_color, tag=f'C{self.id}')
        self.circled = True
        self.logfile.write(f'Circle in middle of Hexagon {self.id} with tag {self.id} and color {circle_color}')
        
    def report(self):
        self.logfile.write(f'Reporting all coordinate on {self.id} starting with center: {self.center}, '
                           f'{self.coordinate_a}, {self.coordinate_b}, {self.coordinate_c}, '
                           f'{self.coordinate_d}, {self.coordinate_e}, {self.coordinate_f}, '
                           f'Circled: {self.circled} and Filled {self.filled}')


class Board:
    def __init__(self, log=logging):
        self.dict = {}
        self.logfile = log
        self.logfile.write('Created Board Dictionary')
    
    def add(self, k, v):
        kv = {f"{k}": v}
        self.dict.update(kv)
        self.logfile.write(f'Added {kv} and dict is now {len(self.dict)} long')
        
    def get(self, k):
        entry = self.dict.get(k)
        self.logfile.write(f'Getting {k} and found {entry}')
        return entry
    
    def items(self):
        result = []
        for k, v in self.dict.items():
            result.append(v)
        self.logfile.write(f'Returning all items of the Board Dictionary: {len(result)}')
        return result

