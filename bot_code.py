import discord
import random

print("Loading...")

token = "MjUxMTY1NDE5MjQxNjAzMDgz.Cxppdw.2stvBMJvXv8cF0FlspngRmZ62cY"
client = discord.Client()
client.login(token)

#echo command, used only for testing purposes
async def echo(author, message):
    await client.send_message(message.channel, message.content[6:len(message.content)])

#helper command, accesses the help document
async def helper(author, message):
    with open("help.txt") as h:
        helpdoc = h.read()
    await client.send_message(message.channel, helpdoc)

#roll command, rolls a die 
async def roll(author, message):
    message_cont = message.content.split()
    message_cont[1] = int(message_cont[1])
    await client.send_message(message.channel, random.randrange(1, message_cont[1] + 1))

#smash command, plays All Star by Smashmouth in the voice channel  
async def smash(author, message):
    try:
        await leave(author, message)
    except AttributeError:
        print()
    author_voice = author.voice.voice_channel
    if(not (author_voice == None)):
        await client.send_message(message.channel, "Now playing All Star by Smashmouth.")
        voice = await client.join_voice_channel(author_voice)
        player = await voice.create_ytdl_player('https://www.youtube.com/watch?annotation_id=annotation_837391&feature=iv&src_vid=5xxQs34UMx4&v=Z22uzDDBRsc')
        player.start()
    else:
        await client.send_message(message.channel, "You are not in a voice channel.")

#play command, plays a song in the voice channel
async def play(author, message):
    try:
        await leave(author, message)
    except AttributeError:
        print()
    author_voice = author.voice.voice_channel
    url = message.content[6:len(message.content)]
    if(not (author_voice == None)):
        await client.send_message(message.channel, "Now playing {urlw}.".format(urlw = url))
        #if(not (client.user.voice.voice_channel == None)):
            #voice = channel.server.voice_client
        voice = await client.join_voice_channel(author_voice)
        player = await voice.create_ytdl_player(url)
        player.start()
    else:
        await client.send_message(message.channel, "You are not in a voice channel.")

#leave command, makes the bot leave the voice channel        
async def leave(author, message):
    await client.voice_client_in(message.server).disconnect()

#automatically disconnects the bot from voice after there is no one left in the voice channel
@client.event
async def on_voice_state_update(before, after):
    voice = after.server.voice_client
    if voice is None or not voice.is_connected():
        return
    if len(voice.channel.voice_members) == 1:
        await voice.disconnect()

#when the bot recieves a message
@client.event
async def on_message(message):
    author = message.author
    if(author == client.user):
        return
    if(message.content.startswith("=")):
        if(message.content.startswith("=echo")):
            await echo(author, message)
        elif(message.content.startswith("=help")):
            await helper(author, message)
        elif(message.content.startswith("=roll")):
            await roll(author, message)
        elif(message.content.startswith("=smash")):
            await smash(author, message)
        elif(message.content.startswith("=play")):
            await play(author, message)
        elif(message.content.startswith("=leave")):
            await leave(author, message)
        else:
            await client.send_message(message.channel, "Command \"" + message.content + "\" not recognized.")
        
print("Online!")

#run the client
client.run(token)


print("Ready!")
