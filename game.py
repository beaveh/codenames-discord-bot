import random

class Game(object):
    """Object that manages game state"""

    channels = []
    turn = None

    def __init__(self, channel):
        self.players = {}
        self.channel = channel

    """Add player to a team"""
    def add(self, player, team): #figure out what player is (discord id, string, etc.)
        if player in self.players:
            return False
        else:
            self.players[player] = team
            return True

    def end_game(self): #must remove the channel from channels list
        pass

class Board(object):
    def __init__(self, teams=['red', 'blue']):

        num_red = 8
        num_blue = 8
        starting_team = random.choice(teams)
        if starting_team == 'red':
            num_red += 1
        else:
            num_blue += 1
        for _ in range(num_red):




class Word(object):
    """Represents a word on the board"""

    revealed = False
    team = 'bystander'

    def __init__(self, text, team='bystander'):
        self.text = text
        self.team = team

    def reveal(self):
        self.revealed = True
        self.text = emojis[self.team] + ' ' + self.text

    def __str__(self):
        return self.text

emojis = {'red': ':red_circle:', 'blue': ':blue_circle:', 'assassin': ':black_circle:', 'bystander': ':white_circle:' }
