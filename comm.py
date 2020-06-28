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
        sock.sendto(packet, (SECRETS['ip'], port))
        print("sent")
    
def server_shutdown():
    client = paramiko.SSHClient() # instantiate class
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(SECRETS['ip'], username=USER, password=PASS) # Get IP from secrets file


    stdin_, stdout_, stderr_ = client.exec_command("screen -r -X eval 'stuff \"stop\"\\\\015'")
    time.sleep(30) # we want the script to stop execution entirely (I think)
    
    # Then run the shutdown function on actual linux
    client.exec_command("shutdown -h now")
    print("Running shutdown...")
    
    lines = stdout_.readlines()
    for line in lines:
        print(line)


if __name__ == "__main__":
    bruh = WakeOnLAN()
    packet = WakeOnLAN.magic_packet(bruh, MACADDRESS)
    WakeOnLAN.send(bruh, packet, 9)