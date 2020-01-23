import random
import discord
import linecache
from collections import Counter

command_prefix = '$'

class Game(object):
    """Object that manages and contains information about the game state"""

    active_games = {} #keys are channels, values are game instances

    def __init__(self, gamemaster, channel):
        self.players = {}
        self.channel = channel
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
        team = team.capitalize()
        if team != 'Red' and team != 'Blue':
            return 'Invalid team selected.'
        elif self.players.get(player) == team:
            return 'You have already joined this team!'
        elif self.started and (player == self.red_spymaster or player == self.blue_spymaster):
            return 'The spymaster cannot change teams after the game has started.'
        # consider removing the ability to join after the game has started
        # elif self.started:
        #     return 'The game has already started. You may not join a team at this time.'
        else:
            if self.red_spymaster == player:
                self.red_spymaster = None
            elif self.blue_spymaster == player:
                self.blue_spymaster = None
            self.players[player] = team
            return f'{player} has joined the {emojis[team]} {team} team.'

    def start(self, user):
        teams = Counter(self.players.values())
        if self.started:
            return 'The game has already started!'
        elif user != self.gamemaster:
            return f'Only the gamemaster ({self.gamemaster}) may start the game.'
        elif teams['Red'] < 2 or teams['Blue'] < 2:
            return 'There are not enough players to start a game!'
        elif not self.red_spymaster:
            return f'Please select a Spymaster for the {emojis["Red"]} Red team.'
        elif not self.blue_spymaster:
            return f'Please select a Spymaster for the {emojis["Blue"]} Blue team.'
        elif self.started:
            return 'The game has already started!'
        else:
            self.started = True
            self.turn = self.board.starting_team
            return f'{self.get_board()} \n{emojis[self.turn]} {self.turn} team goes first.'

    def make_spymaster(self, player):
        team = self.players.get(player)
        if self.started:
            return 'The game has already started. You may not assign Spymasters at this time.'
        elif team == 'Red':
            if self.red_spymaster:
                return f'There is already a Spymaster for the {emojis["Red"]} Red team ({self.red_spymaster}).'
            else:
                self.red_spymaster = player
                return f'{player} is the Spymaster for the {emojis["Red"]} Red team'
        elif team == 'Blue':
            if self.blue_spymaster:
                return f'There is already a Spymaster for the {emojis["Blue"]} Blue team ({self.blue_spymaster}).'
            else:
                self.blue_spymaster = player
                return f'{player} is the Spymaster for the {emojis["Blue"]} Blue team.'
        else:
            return f'You have not joined a team yet! Use {command_prefix}join [Red/Blue] before using this command.'

    def give_clue(self, player, clue, num):
        if not self.started:
            return f'The game has not started yet. Use {command_prefix}start to start the game.'
        elif self.clue_given:
            return f'The spymaster has already given a clue for this round.'
        elif self.check_word(clue):
            return f'Your clue cannot be one of the words on the board!'
        elif self.turn == 'Red':
            if self.red_spymaster != player:
                return f'Only the {emojis["Red"]} Red Spymaster ({self.red_spymaster}) may give a clue at this time.'
            else:
                self.clue_given = True
                if num == 0:
                    self.guesses_left = float('inf')
                else:
                    self.guesses_left = num + 1
                self.red_clues.append(f'{clue}: {num}')
                return f'The clue is "{clue}": {num}'
        elif self.turn == 'Blue':
            if self.blue_spymaster != player:
                return f'Only the {emojis["Blue"]} Blue Spymaster ({self.blue_spymaster}) may give a clue at this time.'
            else:
                self.clue_given = True
                self.guesses_left = num + 1
                self.blue_clues.append(f'{clue}: {num}')
                return f'The clue is "{clue}": {num}'

    def guess(self, player, guess):
        if not self.started:
            return f'The game has not started yet. Use {command_prefix}start to start the game.'
        elif not self.players.get(player):
            return 'You cannot guess since you have not yet joined a team.'
        elif self.players.get(player) != self.turn:
            return f"It is not your team's turn to guess."
        elif not self.clue_given:
            return f'Wait for a clue to be given before guessing.'
        elif not self.check_word(guess):
            return 'Guess an unrevealed word on the board.'
        else:
            current_team = self.turn
            message = f'{player} has guessed {guess}!'
            self.guesses_left -= 1
            for word in self.board.words:
                if word.text.lower() == guess.lower():
                    word.reveal()
                    message += f'\n{guess} is a(n) {emojis[word.team]} {word.team} word.'
                    if word.team == 'Assassin':
                        self.check_winner(self.other(current_team))
                    else:
                        self.check_winner()
                    message += f'\n{self.get_board()}'
                    if word.team != self.players[player]:
                        self.guesses_left = 0
                        message += f"\nThe {current_team} team's turn is over."
                    else:
                        message += f'\nThe {self.turn} team has {self.guesses_left} guess(es) left.'
            if not self.guesses_left:
                self.turn = self.other(self.turn)
                self.clue_given = False
                message += f"\nIt is now the {self.turn} team's turn to play."
            return message

    def end_turn(self, player):
        if not self.started:
            return f'The game has not started yet. Use {command_prefix}start to start the game.'
        elif not self.players.get(player):
            return 'You cannot use this command since you have not yet joined a team.'
        elif self.players.get(player) != self.turn:
            return f"It is not your team's turn to guess."
        elif not self.clue_given:
            return f'Wait for a clue to be given before ending your turn.'
        else:
            current_team = self.turn
            self.turn = self.other(self.turn)
            self.clue_given = False
            return f"The {emojis[current_team]} {current_team} has ended their turn. It is now the {emojis[self.turn]} {self.turn} team's turn."

    """Returns the opposing team"""
    def other(self, team):
        if team == 'Red':
            return 'Blue'
        else:
            return 'Red'

    """Returns whether a given word is one of the words (unrevealed) on the board"""
    def check_word(self, word):
        words = [word.text.lower() for word in self.board.words]
        return word.lower() in words

    def check_winner(self, winner=None):
        if winner:
            return self.get_board + f'\nThe {emojis[winner]} {winner} team wins!'
        reds = self.board.num_red
        blues = self.board.num_blue
        for word in self.board.words:
            if word.revealed:
                if word.team == 'Red':
                    reds -= 1
                elif word.team == 'Blue':
                    blues -= 1
        if reds == 0:
            Game.active_games.pop(self.channel, None)
            return self.get_board() + f'\nThe {emojis["Red"]} Red team wins!'
        elif blues == 0:
            Game.active_games.pop(self.channel, None)
            return self.get_board() + f'\nThe {emojis["Blue"]} Blue team wins!'

    def list_words(self):
        red_list = []
        blue_list = []
        black_list = []
        for word in self.board.words:
            if word.team == 'Red':
                red_list.append(word.text)
            elif word.team == 'Blue':
                blue_list.append(word.text)
            elif word.team == 'Assassin':
                black_list.append(word.text)
        red_string = ', '.join(red_list)
        final_red_string = 'Red: ' + red_string
        blue_string = ', '.join(blue_list)
        final_blue_string = 'Blue: ' + blue_string
        black_string = ', '.join(black_list)
        final_black_string = 'Assasins: ' + black_string
        return final_red_string + '\n' + final_blue_string + '\n' + final_black_string

    def get_board(self):
        return str(self.board)

    def get_status(self):
        return f'{self.get_board()} \n\
                Red Spymaster: {self.red_spymaster} \n\
                Blue Spymaster: {self.blue_spymaster} \n\
                Red Clues: {self.red_clues} \n\
                Blue Clues: {self.blue_clues} \n\
                Current Turn: {self.turn} \n\
                Guesses left: {self.guesses_left}'

    def end_game(self, channel):
        Game.active_games.pop(channel, None)
        return 'Active game successfully ended.'

class Board(object):
    """Represents a 5x5 grid of words"""

    starting_team = None

    def __init__(self, teams=['Red', 'Blue']):
        self.words = []
        self.starting_team = random.choice(teams)
        with open('words.txt', 'r') as file:
            lines = list(file)
            indices = random.sample(range(len(lines)), 25)
            for i, word in enumerate(lines):
                if i in indices:
                    self.words.append(Word(word.strip()))
        self.num_red = 8
        self.num_blue = 8
        if self.starting_team == 'Red':
            self.num_red += 1
        else:
            self.num_blue += 1
        colors = random.sample(range(0, 25), 18)
        reds = colors[:self.num_red]
        blues = colors[self.num_red:17]
        black = colors[17]
        for red in reds:
            self.words[red].team = 'Red'
        for blue in blues:
            self.words[blue].team = 'Blue'
        self.words[black].team = 'Assassin'

    def __str__(self):
        count = 0
        string_list = []
        for word in self.words:
            count += 1
            if count % 5 == 0:
                string_list.append(word.text + " | \n\n")
            elif count % 5 == 1:
                string_list.append("| " + word.text + " | ")
            else:
                string_list.append(word.text + ' | ')
        string = "".join(string_list)
        return string

class Word(object):
    """Represents a word on the board"""

    revealed = False

    def __init__(self, text, team='Bystander'):
        self.text = text
        self.team = team

    def reveal(self):
        self.revealed = True
        self.text = emojis[self.team] + ' ' + self.text

    def __str__(self):
        return self.text

emojis = {'Red': ':red_circle:', 'Blue': ':blue_circle:', 'Assassin': ':black_circle:', 'Bystander': ':white_circle:'}
