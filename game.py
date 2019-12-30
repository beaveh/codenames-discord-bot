class Game(object):
    """Object that manages game state"""

    def __init__(self):
        self.players = {}

    """Add player to a team"""
    def add(self, player, team): #figure out what player is (discord id, string, etc.)
        if player in self.players:
            return False
        else:
            self.players[player] = team
            return True

class Word(object):
    """Represents a word on the board"""

    revealed = False

    def __init__(self, text, team):
        self.text = text
        self.team = team

    def reveal(self):
        self.revealed = True
        self.text = emojis[self.team] + ' ' + self.text

    def __str__(self):
        return self.text

emojis = {'red': ':red_circle:', 'blue': 'blue_circle', 'assassin': ':black_circle:', 'bystander': ':white_circle:' }
