import paramiko 
import json
from dotenv import load_dotenv
import os
import socket
import time
import asyncio

load_dotenv()

USER = os.getenv('SSH_USER') 
PASS = os.getenv('SSH_PASS')
IP = os.getenv('IP')
MACADDRESS = os.getenv('MACADDRESS')



class WakeOnLAN():
    """
    the WakeOnLAN class deals with functions that wake the server. 
    specifically formulating the magic packet and se--html nding it! 
    """
    def __init__(self):
        pass
    def magic_packet(self, mac_address):
        """
        This function creates the magic packet. 
        A bytes object, from hex that is FFF... and then sixteen of the MAC address desired.
        Should work fine...

        """
        mac_address = mac_address.replace(':', "")
        return bytes.fromhex("F"*12 + mac_address*16)
    def send(self, packet, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(packet, (IP, port))
        print("sent")
    
def server_shutdown():
    """
    Server shutdown fxn is to be called in observer. 
    This function is what is used to shut down the server after it reaches the inactivity period.

    
    """
    client = paramiko.SSHClient() # instantiate class
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(IP, username=USER, password=PASS) 


    stdin_, stdout_, stderr_ = client.exec_command("screen -r -X eval 'stuff \"stop\"\\\\015'")
    time.sleep(30) # we want the script to stop execution entirely (I think)
    
    # Then run the shutdown function on actual linux
    client.exec_command("shutdown -h now")
    print("Running shutdown...")
    
    lines = stdout_.readlines()
    for line in lines:
        print(line)
