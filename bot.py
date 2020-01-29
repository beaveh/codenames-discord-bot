import discord, random, os
from discord.ext import commands

client = commands.Bot(command_prefix = '$')

# @client.event
# async def on_ready():
#     print('Bot is ready.')

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left a server')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)} ms')

@client.command(aliases=['8ball', 'test'])
async def _8ball(ctx, *, question): # *, question allows us to take several arguments as just 1
    responses = ['Yes', 'No', 'Uncertain']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(extension + 'loaded')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(extension + 'unloaded')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(extension + 'reloaded')

client.load_extension(f'cogs.commands')

# for filename in os.listdir('./cogs'):
#     if filename.endswith('.py'):
#         client.load_extension(f'cogs.{filename[:-3]}')

#Command to kill the bot
@client.command()
async def stop(ctx):
    await client.logout()

client.run(#insert bot token here)
