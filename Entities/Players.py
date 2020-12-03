from Utils import *


class Player:
    def __init__(self):
        self.__first_name = ''
        self.__last_name = ''
        self.__nick_name = ''
        self.__id = ''
        self.__score = ''
        self.__race = ''
        self.__race_name = ''
    
    def initialize(self, first, last, nick):
        self.__first_name = first
        self.__last_name = last
        self.__nick_name = nick
        self.__id = get_next_id('player')
        self.__score = 1000
        self.__race = 0
    
    def restore(self, first, last, nick, player_id, score, race):
        self.__first_name = first
        self.__last_name = last
        self.__nick_name = nick
        self.__id = player_id
        self.__score = score
        self.__race = race

    def get_score(self):
        return self.__score
    
    def update_score(self, delta):
        self.__score += delta
    
    def reset_score(self, value):
        self.__score = value
        
    def get_race(self):
        return self.__race
    
    def update_race(self, race, race_name):
        # ToDo might need a rule to not allow race to be changed
        self.__race = race
        self.__race_name = race_name
    
    def return_all(self):
        print(self.__id, self.__first_name, self.__last_name, self.__nick_name,
              self.__race, self.__race_name, self.__score)
