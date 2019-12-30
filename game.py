
class Word(object):
    """Represents a word on the board"""

    revealed = False

    def __init__(self, text, team):
        self.text = text
        self.team = team

    def reveal(self):
        self.revealed = True
        self.text = emojis[self.team] + ' ' + self.text

emojis = {'red': ':red_circle:', 'blue': 'blue_circle', 'assassin': ':black_circle:', 'bystander': ':white_circle:' }
