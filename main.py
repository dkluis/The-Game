# This is a sample Python script.

# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from Entities import Player
from Entities import Race


def play_the_game():
    print(f'Hi, The game is starting')
    dick = Player()
    dick.restore('Dick', 'Kluis', 'DK', 3, 1001, '10000')
    dick.return_all()
    dick.update_score(-50)
    dick.return_all()
    dick.reset_score(100)
    dick.return_all()
    
    robin = Player()
    robin.initialize('Robin', 'Kluis', 'RK')
    robin.return_all()
    robin.update_race(10003)
    robin.return_all()
    
    race = Race()
    race.restore(100)
    race.return_all()
    race.initialize("Elf")
    race.return_all()


if __name__ == '__main__':
    play_the_game()
