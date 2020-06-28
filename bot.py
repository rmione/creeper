import discord
import os
from dotenv import load_dotenv
import re
import observer
import socket
import json
from discord.ext import commands
import asyncio
import paramiko 
from comm import WakeOnLAN
from comm import server_shutdown
import logging 

import threading
import multiprocessing

logging.basicConfig(format='%(asctime)-15s s%(message)s', level='INFO', filename=os.getcwd()+'/log/creeper.log')
console = logging.StreamHandler()
console.setLevel(logging.INFO)



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_GUILD')
MACADDRESS = os.getenv('MACADDRESS')
MAP_PORT=os.getenv('PORT')
IP = os.getenv('IP')

creeper = commands.Bot(command_prefix='.')
srv = observer.Server()



@creeper.event
async def on_ready():
    # logging.info(f"{creeper.user} is up and running!")
    pass

@creeper.command()
async def bing(ctx):
    await ctx.send("Bong")


@creeper.command(aliases=['creeper'])
@commands.cooldown(1, 60)
async def speak(ctx, *, argument):
    print()
    logging.info("{0} used the speak command. ".format(ctx.message.author))
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

    # use regex to match id
    # if re.match("<@?!"+SECRETS['id'], ctx.message.content):
    #     await ctx.message.channel.send("I am a bot created by @rmione on github, check me out: https://github.com/rmione/creeper")

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
    
        except Exception as e:
            print(e)
    if argument == 'map':
        quote = """
            The Road goes ever on and on
        Out from the door where it began.
        Now far ahead the Road has gone.
        Let others follow, if they can!
        Let them a journey new begin.
        But I at last with weary feet
        Will turn towards the lighted inn,
        My evening-rest and sleep to meet.
            - J.R.R Tolkien
                """
        await ctx.send("https://"+IP+":"+MAP_PORT +"\n"+ quote)

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

    

@creeper.command(name="wake")
async def Wake(ctx):
    await ctx.message.channel.send("Waking up server...")
    logging.info("{0} used the wake command. ".format(ctx.message.author))
    logging.info("Waking up server...")
    waker = WakeOnLAN()
    packet = WakeOnLAN.magic_packet(waker, MACADDRESS)
    WakeOnLAN.send(waker, packet, 9)
    
creeper.run(TOKEN)
