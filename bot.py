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

# @client.command()
# async def ping(ctx):
#     await ctx.send(f'Pong! {round(client.latency * 1000)} ms')

@client.command(aliases=['8ball', 'test'])
async def _8ball(ctx, *, question): # *, question allows us to take several arguments as just 1
    responses = ['Yes', 'No', 'Uncertain']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

#temporary command to kill the bot
@client.command()
async def stop(ctx):
    await client.logout()

client.run('NjM3NDY5NTMwNzgzODc1MDky.XbOqTA.hDTgayoDbr6aTx8Ei1TLBjK9USE')
# client = discord.Client()
#
# @client.event
# async def on_ready():
#     print('We have logged in as {0.user}'.format(client))
#
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')
#
# client.run('NjM3NDY5NTMwNzgzODc1MDky.XbOqTA.hDTgayoDbr6aTx8Ei1TLBjK9USE')
