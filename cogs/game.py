import random
from collections import Counter
from .commands import command_prefix

class Game(object):
    """Object that manages and contains information about the game state"""

    active_games = {} #keys are channels, values are game instances

    def __init__(self, gamemaster):
        self.players = {}
        self.started = False
        self.turn = None
        self.gamemaster = gamemaster
        self.board = Board()
        self.red_spymaster = None
        self.blue_spymaster = None
        self.red_clues = []
        self.blue_clues = []
        self.clue_given = False
        self.guesses_left = 0

    """Add player to a team"""
    def add(self, player, team):
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
            self.turn = self.board.starting_team

    def make_spymaster(self, player):
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

    def give_clue(self, player, clue, num):
        if not self.started:
            return f'The game has not started yet. Use {command_prefix}start to start the game.'
        elif self.clue_given:
            return f'The spymaster has already given a clue for this round.'
        elif self.check_word(clue):
            return f'Your clue cannot be one of the words on the board!'
        elif self.turn == 'red':
            if self.red_spymaster != player:
                return f'Only the Red Spymaster ({self.red_spymaster}) may give a clue at this time.'
            else:
                self.clue_given = True
                self.red_clues.append(f'{clue}: {num}')
                return f'The clue is {clue}: {num}'
        elif self.turn == 'blue':
            if self.blue_spymaster != player:
                return f'Only the Blue Spymaster ({self.blue_spymaster}) may give a clue at this time.'
            else:
                self.clue_given = True
                self.blue_clues.append(f'{clue}: {num}')
                return f'The clue is {clue}: {num}'

    """Returns whether a given word is one of the words (unrevealed) on the board"""
    def check_word(self, word):
        words = [word.text for word in self.board.words]
        return word in words

    def get_board(self):
        return str(self.board)

    def get_status(self):
        return f'{self.get_board()} \n
                Red Spymaster: {self.red_spymaster} \n
                Blue Spymaster: {self.blue_spymaster} \n
                Red Clues: {self.red_clues} \n
                Blue Clues: {self.blue_clues} \n
                Current Turn: {self.turn} \n
                Guesses left: {self.guesses_left}'

    def end_game(self, channel):
        Game.active_games.pop(channel, None)

class Board(object):
    """Represents a 5x5 grid of words"""

    starting_team = None

    def __init__(self, teams=['red', 'blue']):
        self.words = []
        self.starting_team = random.choice(teams)
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

    def __str__(self):
        pass

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
