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
        self.__logfile = ''
    
    def initialize(self, first, last, nick):
        self.__first_name = first
        self.__last_name = last
        self.__nick_name = nick
        self.__id = get_next_id('player')
        self.__score = 1000
        self.__race = 0
        self.__logfile = logging(caller=f'{self.__nick_name}', filename='TheGame')
        self.__logfile.write(f'Initialize New Player {first}, {last}', 2)
    
    def restore(self, first, last, nick, player_id, score, race):
        self.__first_name = first
        self.__last_name = last
        self.__nick_name = nick
        self.__id = player_id
        self.__score = score
        self.__race = race
        self.__logfile = logging(caller=f'{self.__nick_name}', filename='TheGame')
        self.__logfile.write(f'Restored Player', 2)
        
    def get_nick_name(self):
        return self.__nick_name
    
    def get_score(self):
        return self.__score
    
    def update_score(self, delta):
        self.__score += delta
        self.__logfile.write(f'Updated score to: {self.__score}')
    
    def reset_score(self, value):
        self.__score = value
        self.__logfile.write(f'Reset score to: {self.__score}')
    
    def get_race(self):
        return self.__race
    
    def update_race(self, race, race_name):
        # ToDo might need a rule to not allow race to be changed
        self.__race = race
        self.__race_name = race_name
        self.__logfile.write(f'Updated race to: {self.__race_name}')
    
    def return_all(self):
        return self.__first_name, self.__last_name, self.__nick_name, self.__id, self.__score, self.__race
    

def restore_all_players():
    players_file = open('.thegame/players', 'r')
    restore_players = players_file.readlines()
    players = []
    for rest_player in restore_players:
        play_temp = Player()
        rest_player = ast.literal_eval(rest_player)
        play_temp.restore(rest_player[0], rest_player[1], rest_player[2], rest_player[3], rest_player[4],
                          rest_player[5])
        players.append(play_temp)
        del play_temp
    players_file.close()
    return players


def store_all_players(players):
    players_file = open('.thegame/players', 'w')
    for player in players:
        info = player.return_all()
        store_players = str(info) + '\n'
        players_file.write(store_players)
    players_file.close()
