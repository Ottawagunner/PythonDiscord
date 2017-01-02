import discord
import asyncio
import random
import requests
import json
import pickle


pollVoters = []
pollActive = 0
pollYes = 0
pollNo = 0
pollResult = ""

token = 'MjYxMTU3ODkxMTI4NDI2NDk3.CzxAVA.J527zyVIjfmAVNU0_RFaXKe2zYU'
            
with open("memelist.txt","r") as f:
    Memes = f.read().splitlines()
f.close()

client = discord.Client()
superadmins = ['188426558376116224']

def is_me(m):
    return m.author == client.user

def is_Rank(z):
    return (z.author.id in superadmins)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    for x in client.servers:
        print(x.name)
        print('------')
        for y in x.members:
            print(y.name + " "+y.id)
            for j in y.roles:
                print("     " + j.name + " "+j.id)
                if (j.id =="193152276662059010"):
                    superadmins.append(y.id)

    

@client.event
async def on_message(message):
    global pollVoters
    global pollActive
    global pollYes
    global pollNo
    global pollResult

    #commands
    if message.content.startswith('!'):

        if message.content.startswith('!sleep') & is_Rank(message):
            await asyncio.sleep(5)
            await client.send_message(message.channel, 'Done sleeping')
    #poll
        if message.content.startswith('!poll') & is_Rank(message):
            if pollActive == 0:
                pollActive = 1
                title = message.content.split(' ',1)
                print (title[1])
                await client.send_message(message.channel, 'Poll Started: "'+title[1]+'" \nVote with !yes or !no')
            else:
                await client.send_message(message.channel, 'Poll Already Active')
    #poll
        if message.content.startswith('!yes'):
            if (pollActive == 1) & (message.author.id not in pollVoters):
                pollYes = pollYes + 1
                pollVoters.append(message.author.id)
                await client.send_message(message.channel, 'Voted Yes')

            elif (pollActive == 1 )&(message.author.id in pollVoters):
                await client.send_message(message.channel, 'Already Voted')
            else:
                await client.send_message(message.channel, 'No Active Poll')
    #poll
        if message.content.startswith('!no'):
            if (pollActive == 1) & (message.author.id not in pollVoters):
                pollNo = pollNo + 1
                pollVoters.append(message.author.id)
                await client.send_message(message.channel, 'Voted No')

            elif (pollActive == 1) & (message.author.id in pollVoters):
                await client.send_message(message.channel, 'Already Voted')
            else:
                await client.send_message(message.channel, 'No Active Poll')
    #poll
        if message.content.startswith('!results') & is_Rank(message):
            if pollActive == 1 :
                if pollYes > pollNo:
                    pollResult = "Yes Wins"
                elif pollYes < pollNo:
                    pollResult = "No Wins"
                else:
                    pollResult = "Tie"

                await client.send_message(message.channel, 'Results: '+ pollResult)

                pollVoters = []
                pollActive = 0
                pollYes = 0
                pollNo = 0
                pollResult = ""

            else:
                await client.send_message(message.channel, 'No Active Poll')

        if message.content.startswith('ping') & is_Rank(message):
            await client.send_message(message.channel, 'pong')

        if message.content.startswith('!add'):
            Memes.append(message.content.split(' ',1)[1])

            with open("memelist.txt","a") as f:
                f.write("%s\n" % message.content.split(' ',1)[1])
            f.close()

            await client.send_message(message.channel, 'Added')

        if message.content.startswith('!mememe') & (is_Rank(message) or (message.channel.id =='192805195032428545')):
            await client.send_message(message.channel,random.choice(Memes))

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

        if message.content.startswith('!botclean') & is_Rank(message):
            deleted = await client.purge_from(message.channel, limit=100, check=is_me)
            await client.send_message(message.channel, 'Deleted {} message(s)'.format(len(deleted)))

        if message.content.startswith('!joke'):

            r = requests.get('http://tambal.azurewebsites.net/joke/random')        
            await client.send_message(message.channel, r.json()['joke'])
    #passive
    else:

        if (len(client.messages)>=2):
            if(client.messages[-2].author.id != '261157891128426497') & (client.messages[-1].author.id != '261157891128426497') :
                message1 = client.messages[-2].content
                if (message1 == message.content):
                    if (message1 == "what"):
                        await client.send_message(message.channel, 'In the butt')
                    else:
                        await client.send_message(message.channel, message.content)

        if (x for x in message.mentions if x.id == '261157891128426497'):
            if (message.author.id !='261157891128426497') & message.content.startswith('That right'):
                await client.send_message(message.channel, 'Damn right')

client.run(token)
