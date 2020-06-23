import discord
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_GUILD')
client = discord.Client()
import observer
srv = observer.Server()
@client.event

async def on_ready():
    print(f'{client.user} has connected to Discord!')
@client.event
async def when_mentioned(message):
    print("yooo")


@client.event
async def on_message(message):
    # Below protects against an inf loop
    if message.author == client.user:
        return
    if '@creeper' in message.content:
        await message.channel.send("I am a bot created by @rmione on github, check me out: https://github.com/rmione/creeper")

    if 'where server' in message.content:
        data = srv.info()
        await message.channel.send("Ding Dong! There is " + str(data.get('players')) +" players currently online. The server's latency is " + str(data.get('ping')) +" milliseconds")



client.run(TOKEN)