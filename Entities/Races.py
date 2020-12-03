from Utils import *


class Race:
    def __init__(self):
        self.__id = 0
        self.__name = ''
    
    def restore(self, race_id):
        self.__id = race_id
        # ToDo retrieve the race name based on the ID
        self.__name = 'Some Race'
        
    def initialize(self, name):
        self.__id = get_next_id('race')
        self.__name = name
        
    def get_race_name(self):
        return self.__name
    
    def return_all(self):
        print(self.__id, self.__name)

