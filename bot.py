import os
import sys
import discord
import aiofiles
import aiofiles.os
import random

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents, activity=discord.Game(name='Microsoft Excel'))

playerQueue = []
numTeams = 2
teams = []
for i in range(numTeams):
    teams.append([])

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    if await aiofiles.os.path.isfile('reset.txt'):
        async with aiofiles.open('reset.txt', 'r') as f:
            await client.get_channel(int(await f.read())).send('I\'m back')
        await aiofiles.os.remove('reset.txt')
    else:
        for guild in client.guilds:
            channel = guild.system_channel
            await channel.send('Sup bitches? I made it.')


@client.event
async def on_message(message):
    global playerQueue, teams, numTeams
    if message.author == client.user:
        return

    if not (message.content.lower().startswith('teams-chan ') \
    or message.content.lower().startswith('teamschan ') \
    or message.content.lower().startswith('!tc')):
        return

    command = message.content.split(' ', 1)[1].lower()

    if command == ('create a new player queue from my voice channel') \
    or command == ('newqueuevoice'):
        if message.author.voice == None:
            await message.channel.send('Hop in a vc and then I can help')
        else:
            playerQueue = []
            vc = message.author.voice.channel
            for member in vc.members:
                playerQueue.append(member)
            if (len(playerQueue) == 1):
                await message.channel.send('Looks like youre the only one in the vc, but I\'ll go ahead and create the queue anyways i guess...')
            else:
                await message.channel.send('Alrighty let\'s see here...')
                playerListString = ""
                for member in playerQueue:
                    playerListString += "\n- "+member.display_name
                await message.channel.send('Okay '+str(len(playerQueue))+' players from your vc have been added to the queue:'+playerListString)

    if command == ('create a new empty player queue') \
    or  command == ('newqueue'):
        playerQueue = []
        await message.channel.send('One piping hot (and empty) player queue coming your way.')

    #if command

    if command == ('whos in the queue') \
    or command == ('listqueue'):
        if (len(playerQueue) == 0):
            await message.channel.send('No one is in the queue right now')
        else:
            playerListString = ""
            for member in playerQueue:
                playerListString += "\n- "+member.display_name
            await message.channel.send('The following players are in the queue right now:'+playerListString)

    if command == ('increase the number of teams') \
    or command == ('addteam'):
        numTeams += 1
        teams = []
        for i in range(numTeams):
            teams.append([])
        await message.channel.send('Okay you now have '+str(numTeams)+' team(s)')

    if command == ('decrease the number of teams') \
    or command == ('delteam'):
        if (numTeams > 1):
            numTeams -= 1
            teams = []
            for i in range(numTeams):
                teams.append([])
            await message.channel.send('Okay you now have '+str(numTeams)+' team(s)')
        else:
            await message.channel.send('You can\'t have less than 1 team lol')

    if command == ('how many teams are there') \
    or command == ('teamcount'):
        await message.channel.send('You have '+str(numTeams)+' team(s)')

    if command == ('create some random teams') \
    or command == ('randomteams'):
        if len(playerQueue) > 0:
            teams = []
            for i in range(numTeams):
                teams.append([])
            random.shuffle(playerQueue)
            workingListIndex = 0
            for member in playerQueue:
                teams[workingListIndex].append(member)
                workingListIndex += 1
                if (workingListIndex == numTeams):
                    workingListIndex = 0
            for teamIndex in range(len(teams)):
                playerListString = ""
                for member in teams[teamIndex]:
                    playerListString += "\n- "+member.display_name
                await message.channel.send("Here's team "+str(teamIndex+1)+":"+playerListString)
        else:
            await message.channel.send("How about you add some players to the queue first?")


    if command == 'take a walk' \
    or command == "restart":
        await message.channel.send('Fine... I\'ll brb')
        async with aiofiles.open('reset.txt', 'w') as f:
            await f.write(str(message.channel.id))
            await f.close()
        os.execv(sys.executable, ['python'] + sys.argv)

client.run('########')
