import random

class Game(object):
    """Object that manages and contains information about the game state"""

    active_games = {} #keys are channels, values are game instances

    def __init__(self, server):
        self.players = {}
        self.channel = channel
        self.turn = None
        self.started = False

    """Add player to a team"""
    def add(self, player, team): #figure out what player is
        if team != 'red' or team != 'blue':
            raise TeamError
        if self.players.get(player) == team:
            raise SameTeamError
        else:
            self.players[player] = team

class Board(object):
    def __init__(self, teams=['red', 'blue']):
        with open('words.txt', 'r') as file:
            self.words = []
            count = 0
            lines = []
            for line in file:
                count += 1
            while len(lines) < 25:
                a = random.randrange(0, count)
                if a in lines:
                    pass
                else:
                    lines.append(a)
            for num in lines:
                self.words.append(Word(file.readline(num)))

        num_red = 8
        num_blue = 8
        starting_team = random.choice(teams)
        if starting_team == 'red':
            num_red += 1
        else:
            num_blue += 1
        colors = random.sample(range(0, 25), 18)
        reds = colors[:num_red]
        blues = colors[num_red:17]
        black = colors[17]
        for red in reds:
            self.words[red].team = 'red'
        for blue in blues:
            self.words[blue].team = 'blue'
        self.words[black].team = 'black'

class Word(object):
    """Represents a word on the board"""

    revealed = False
    team = 'bystander'

    def __init__(self, text, team):
        self.text = text
        self.team = team

    def reveal(self):
        self.revealed = True
        self.text = emojis[self.team] + ' ' + self.text

    def __str__(self):
        return self.text

emojis = {'red': ':red_circle:', 'blue': ':blue_circle:', 'assassin': ':black_circle:', 'bystander': ':white_circle:' }
