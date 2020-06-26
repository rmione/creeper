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
    Speak handles all of the basic functionality of the bot.
    It has a basic decision structure to let it respond to different messages.
    It takes the context parameter, and then an additional argument.
    :return:
    """

    if ctx.message.author == creeper.user:
        return
    if argument == ' ': 
        await ctx.message.channel.send("Aw man")

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
@creeper.command(name="shutdown")
async def shutdown(ctx):
    # Logs out and resets the internal state of the bot 
    await creeper.close()
    creeper.clear()
    

creeper.run(TOKEN)