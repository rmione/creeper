import discord
import os
from dotenv import load_dotenv
import re
import observer
from observer import SECRETS


# Dotenv stuff for security
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_GUILD')
client = discord.Client()

srv = observer.Server()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    """
    On message it checks for it being mentioned, as well as if the keyword "where server" is mentioned.
    This is the bot's main functionality as of yet.
    Also there is  infinite loop protection!

    :param message:
    :return:
    """
    print(message.raw_mentions)
    if message.author == client.user:
        return

    if re.match("<@?!"+SECRETS['id'], message.content):
        await message.channel.send("I am a bot created by @rmione on github, check me out: https://github.com/rmione/creeper")

    if 'where server' in message.content:
        data = srv.info()
        await message.channel.send("Ding Dong! There is " + str(data.get('players')) +" players currently online. The server's latency is " + str(data.get('ping')) +" milliseconds")



client.run(TOKEN)