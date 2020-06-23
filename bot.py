import discord
import os
from dotenv import load_dotenv
import re
import observer
import socket
from observer import SECRETS
import mcstatus

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

    if message.author == client.user:
        return

    if re.match("<@?!"+SECRETS['id'], message.content):
        await message.channel.send("I am a bot created by @rmione on github, check me out: https://github.com/rmione/creeper")

    if 'where server' in message.content:

        try:
            data = srv.info()
            if data['players'] == 1:
                await message.channel.send(
                    "Ding Dong! There is {players} player currently online. The server's latency is {ping} milliseconds.".format(
                        players=str(data.get('players')), ping=str(data.get('ping'))))

            else:
                await message.channel.send(
                    "Ding Dong! There are {players} players currently online. The server's latency is {ping} milliseconds.".format(
                        players=str(data.get('players')), ping=str(data.get('ping'))))
        except ConnectionRefusedError:
            await message.channel.send("This address doesn't want me connecting to it.")
        except socket.timeout:
            # The server is down
            await message.channel.send("This server is down. Sorry for the inconvenience!")


client.run(TOKEN)