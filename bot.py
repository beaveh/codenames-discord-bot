import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('NjM3NDY5NTMwNzgzODc1MDky.XbOqTA.hDTgayoDbr6aTx8Ei1TLBjK9USE')
