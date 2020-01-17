import random
from collections import Counter

class Game(object):
    """Object that manages and contains information about the game state"""

    active_games = {} #keys are channels, values are game instances
    started = False

    def __init__(self, gamemaster):
        self.players = {}
        self.turn = None
        self.gamemaster = gamemaster
        self.board = Board()
        self.red_spymaster = None
        self.blue_spymaster = None

    """Add player to a team"""
    def add(self, player, team): #figure out what player is
        if team != 'red' and team != 'blue':
            return 'Invalid team selected.'
        if self.players.get(player) == team:
            return 'You have already joined this team!'
        if self.started:
            return 'The game has already started. You may not join a team at this time.'
        else:
            self.players[player] = team
            return f'{player} has joined the {team} team.'

    def start(self, user):
        teams = Counter(self.players.values())
        if user != self.gamemaster:
            return f'Only the gamemaster ({self.gamemaster}) may start the game.'
        elif teams['red'] < 2 or teams['blue'] < 2:
            return 'There are not enough players to start a game!'
        elif not self.red_spymaster:
            return 'Please select a Spymaster for the red team.'
        elif not self.blue_spymaster:
            return 'Please select a Spymaster for the blue team.'
        elif self.started:
            return 'The game has already started!'
        else:
            self.started = True

    def make_spymaster(self, player): #account for case where player has not yet joined a team
        team = self.players.get(player)
        if team == 'red':
            if self.red_spymaster:
                return 'There is already a Spymaster for the Red team.'
            else:
                self.red_spymaster = player
                return f'{player} is the Spymaster for the Red team'
        elif team == 'blue':
            if self.blue_spymaster:
                return 'There is already a Spymaster for the Blue team.'
            else:
                self.blue_spymaster = player
                return f'{player} is the Spymaster for the Blue team.'
        else:
            return 'You have not joined a team yet!'

    def end_game(self, channel):
        Game.active_games.pop(channel, None)

class Board(object):
    """Represents a 5x5 grid of letters"""

    starting_team = None

    def __init__(self, teams=['red', 'blue']):
        self.words = []
        with open('words.txt', 'r') as file:
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
                self.words.append(Word(file.readline(num), None))

        num_red = 8
        num_blue = 8
        self.starting_team = random.choice(teams)
        if self.starting_team == 'red':
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

emojis = {'red': ':red_circle:', 'blue': ':blue_circle:', 'assassin': ':black_circle:', 'bystander': ':white_circle:'}
