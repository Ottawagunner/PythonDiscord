import discord
import asyncio
import random

token = ''
client = discord.Client()
def is_me(m):
    return m.author == client.user
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    
    if message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

    if message.content.startswith('ping'):
        await client.send_message(message.channel, 'pong')
        
    if message.content.startswith('!rolld20'):
        roll = random.randint(1,20)
        await client.send_message(message.channel, 'You rolled a {}'.format(roll))

    if message.content.startswith('!flipcoin'):
        roll = random.randint(1,2)
        if roll == 1:
            coin = 'Heads'
        else:
            coin = 'Tails'
        await client.send_message(message.channel, coin)
        
    if message.content.startswith('!botclean'):
        deleted = await client.purge_from(message.channel, limit=100, check=is_me)
        await client.send_message(channel, 'Deleted {} message(s)'.format(len(deleted)))
        
client.run(token)
