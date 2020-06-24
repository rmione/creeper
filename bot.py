import discord
import os
from dotenv import load_dotenv
import re
import observer
import socket
from observer import SECRETS
from discord.ext import commands
import asyncio


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_GUILD')


# client = discord.Client()
creeper = commands.Bot(command_prefix='.')
srv = observer.Server()



@creeper.event
async def on_ready():
    print(f'{creeper.user} is up and running!')


@creeper.command()
async def bing(ctx):
    await ctx.send("Bong")

@creeper.command(aliases=['creeper'])
@commands.cooldown(1, 60)
async def speak(ctx, *, argument):
    """
    On message it checks for it being mentioned, as well as if the keyword "where server" is mentioned.
    This is the bot's main functionality as of yet.
    Also there is  infinite loop protection!

    :param message:
    :return:
    """

    if ctx.message.author == creeper.user:
        return

    if re.match("<@?!"+SECRETS['id'], ctx.message.content):
        await ctx.message.channel.send("I am a bot created by @rmione on github, check me out: https://github.com/rmione/creeper")

    if argument == 'where server':

        try:
            data = srv.info()
            if data['players'] == 1:
                await ctx.message.channel.send(
                    "Ding Dong! There is {players} player currently online. The server's latency is {ping} milliseconds.".format(
                        players=str(data.get('players')), ping=str(data.get('ping'))))

            else:
                await ctx.message.channel.send(
                    "Ding Dong! There are {players} players currently online. The server's latency is {ping} milliseconds.".format(
                        players=str(data.get('players')), ping=str(data.get('ping'))))
        except ConnectionRefusedError:
            await ctx.message.channel.send("This address doesn't want me connecting to it.")
        except socket.timeout:
            # The server is down
            await ctx.message.channel.send("This server is down. Sorry for the inconvenience!")


    if argument == 'help':
        await ctx.message.channel.send(

        """
        :boom: 
        
        
        creeper alpha 
        A handy Minecraft-related discord bot
        Commands
        .creeper help
        .creeper where server
        
        :boom:
        """)



creeper.run(TOKEN)