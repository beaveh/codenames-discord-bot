import discord
from discord.ext import commands
from .game import Game

class Commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is online')

    #Commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(':red_circle: \n hi')

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
            Game.active_games[ctx.channel] = Game()

    @commands.command()
    async def join(self, ctx, team): #team may need to be casted to str
        check_game(ctx)
        if team != 'red' or team != 'blue':
            await ctx.send('Invalid team selected.')
        else:
            get_game(ctx).players[ctx.author] = team
            await ctx.send(f'{ctx.author} has joined the {team} team.')

    @commands.command()
    async def end_game(self, ctx):
        if Game.active_games.pop(ctx.channel, None):
            await ctx.send('Active game successfully ended.')
        else:
            await ctx.send('There is no active game currently in this channel.')

    """Checks for an active game in the current channel"""
    async def check_game(ctx):
        if not Game.active_games.get(ctx.channel):
            await ctx.send(f'There is not an active game in the channel! Use {comand_prefix}codenames to start a new game.')

    """Returns the active game within the ctx channel"""
    def get_game(ctx):
        return Game.active_games.get(ctx.channel)

def setup(client):
    client.add_cog(Commands(client))
