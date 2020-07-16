# Creeper Setup Guide
### This is a brief guide telling you how to get a creeper bot set up on your system. It is worth noting that some of the features are particular to my own setup, such as Wake on LAN, etc., due to the server platform I am using, et cetera. Nevertheless: 

## Prerequisites 
- A working Minecraft server instance with internet access, that can be publically polled by mcstatus. 
- A computer or server with internet access, that will be able to run Python, in order to actually run the bot off of. This can be your own PC, if you like. However, if you want the bot to run all the time, make sure to have a seprate machine, virtual or not, to do this.
  
## Setting up a Discord Bot 
Log in with a Discord account on the discord developer website, and create a new Application. https://discord.com/developers/applications 
There are plenty of good guides on this on the web, so find one of those. Make sure to get your application token as that will be needed later! 

## Setting up the Environment
This application uses dotenv to securely load environment variables which are used for sensitive things. Make sure to set up your .env file with this sort of format: 
### .env file
```bash
DISCORD_TOKEN=foo
DISCORD_GUILD=foo 
SSH_USER=bar
SSH_PASS=bar
MACADDRESS=blah
MAP=blah
IP=blah
POWERUSERS=blah#1234,blah#4567,blah#7890
```
| Parameter      | Description | Required    |
| :---        |    :----   |          ---: |
| DISCORD_TOKEN    | The bot account's token      | Yes  |
| DISCORD_GUILD  | The name of the discord server       | Yes     |
| SSH_USER | The server's SSH username | Yes
| SSH_PASS | The server's SSH password | Yes
| MACADDRESS | The MAC address of the server machine | Yes
| MAP | The map plugin's URL | No
| IP | The IP address of the server | Yes
| POWERUSERS | Comma separated sequence of discord names of whom you want to have access to sensitive commands. | Yes


## Setting up the Bot on a Host Machine
The bot will also need to run on a host machine. However you choose to do this is up to your own discretion. Anything that has internet access, and is also capable of running Python files should work fine. 