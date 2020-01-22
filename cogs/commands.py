import discord, random, os
from discord.ext import commands
from .game import Game
from .exceptions import ActiveGameError

command_prefix = '$'

class Commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Codenames Bot is online')

    #Commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong')

    @commands.command()
    async def pong(self, ctx):
        await ctx.send(':blue_circle: \n bye :wave:')

    @commands.command()
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)

    @commands.command()
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#', 1)
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.name}#{user.discriminator}')

    #Codenames commands below this line
    @commands.command()
    async def codenames(self, ctx):
        if ctx.channel in Game.active_games:
            await ctx.send(f'There is already a game in progress! (Use {command_prefix}end_game to terminate this game)')
        else:
            Game.active_games[ctx.channel] = Game(ctx.author, ctx.channel)
            await ctx.send(f'The game has been configured. Use {command_prefix}join [Red/Blue] to join a team.')

    @commands.command()
    async def join(self, ctx, team): #team may need to be casted to str
        try:
            check_game(ctx)
            message = get_game(ctx).add(ctx.author, team)
            await ctx.send(message)
        except ActiveGameError:
            await ctx.send(f'There is not an active game in the channel! Use {command_prefix}codenames to start a new game.')

    @commands.command()
    async def spymaster(self, ctx):
        try:
            check_game(ctx)
            message = get_game(ctx).make_spymaster(ctx.author)
            await ctx.send(message)
        except ActiveGameError:
            await ctx.send(f'There is not an active game in the channel! Use {command_prefix}codenames to start a new game.')

    @commands.command()
    async def start(self, ctx): # need to send words to spymasters
        try:
            check_game(ctx)
            message = get_game(ctx).start(ctx.author)
            await ctx.send(message)
        except ActiveGameError:
            await ctx.send(f'There is not an active game in the channel! Use {command_prefix}codenames to start a new game.')

    @commands.command()
    async def give_clue(self, ctx, clue, number):
        try:
            check_game(ctx)
            if get_game(ctx).clue_given or get_game(ctx).check_word(clue):
                await ctx.message.delete()
            message = get_game(ctx).give_clue(ctx.author, clue, int(number))
            await ctx.send(message)
        except ActiveGameError:
            await ctx.send(f'There is not an active game in the channel! Use {command_prefix}codenames to start a new game.')
        except ValueError:
            await ctx.send('You must give the number as an integer.')

    @commands.command()
    async def guess(self, ctx, word):
        try:
            check_game(ctx)
            message = get_game(ctx).guess(ctx.author, word)
            await ctx.send(message)
        except ActiveGameError:
            await ctx.send(f'There is not an active game in the channel! Use {command_prefix}codenames to start a new game.')

    @commands.command()
    async def end_turn(self, ctx):
        try:
            check_game(ctx)
            message = get_game(ctx).guess(ctx.author)
            await ctx.send(message)
        except ActiveGameError:
            await ctx.send(f'There is not an active game in the channel! Use {command_prefix}codenames to start a new game.')

    @commands.command()
    async def rules(self, ctx):
        pass

    @commands.command()
    async def status(self, ctx):
        try:
            check_game(ctx)
            message = get_game(ctx).get_status()
            await ctx.send(message)
        except ActiveGameError:
            await ctx.send(f'There is not an active game in the channel! Use {command_prefix}codenames to start a new game.')

    @commands.command()
    async def end_game(self, ctx):
        try:
            check_game(ctx)
            message = get_game(ctx).end_game(ctx.channel)
            await ctx.send(message)
        except ActiveGameError:
            await ctx.send(f'There is not an active game in the channel! Use {command_prefix}codenames to start a new game.')


"""Checks for an active game in the current channel"""
def check_game(ctx):
    if not Game.active_games.get(ctx.channel):
        raise ActiveGameError

"""Returns the active game within the ctx channel"""
def get_game(ctx):
    return Game.active_games.get(ctx.channel)

def setup(client):
    client.add_cog(Commands(client))
