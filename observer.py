from mcstatus import MinecraftServer
import os
import json
import asyncio
import comm 
import socket
import time
from dotenv import load_dotenv

load_dotenv()

"""
Secrets file hides sensitive info, also will probably be filled in by a command line version of the setup. 
For now, just this though
"""
IP = os.getenv('IP')
count  = 0 
class Server:
    """
    Server class has a couple objects.
    It creates a server object by looking up the IP in the .env file.
    Also there is the maintenance flag. This is only changed in the event that Maintenance mode is needed.
    
    """

    def __init__(self, flag=False):
        self.server = MinecraftServer.lookup(IP)
        self.maintenance = flag # Maintenace flag will be used to make sure that observer stops running when I want it to, otherwise bad stuff will happen. 
    def info(self):
        """
        Sends a request to the desired server, and returns the JSON object returned by mcstatus's status method.
        We may want to do more later.

        :return:
        """
        status = self.server.status()
        ping = int(self.server.ping())
        data = {'players': status.players.online, 'ping': ping}
        return data


    def watch(self, previous=None):
        """
        The watch() function takes one parameter. Due to the function being called recursively, it is useful for it to know
        the previous status of the server. This way it can know if it has exceeded the x-minute time period that is allowed before
        shutting down the server.
        There is a fairly basic logic that is followed each time it is called to figure this out. 
        """
        print(previous)
        if not self.maintenance:
            # Maintenance mode is not on here.
            try:
                data = self.info() # check the info, get players, etc...  
                if data['players'] != 0:
                    current = 'Active'
                else: 
                    current = 'Inactive'
                time.sleep(5*60)

                if previous is None: 
                    """
                    This is the first time it was called. 
                    In this case, we just want to call it again, to get more data, this time with the current value as the previous. 
                    """
                    self.watch(previous=current)
                if previous == 'Inactive' and current == 'Inactive': 
                    # Server has been inactive for 10 mins, so it must be shut down! 
                    comm.server_shutdown()

                else: 
                    # All of the other different cases are covered by this. The logic handles itself, really! 
                    self.watch(previous=current)
            # todo: this could be better for sure... fix it later.
            except socket.timeout:
                print("The server is down! ")
                self.watch()
            except ConnectionRefusedError: 
                time.sleep(60)
                self.watch()
        if self.maintenance: 
            # Maintenance mode is on in this case.
            print("Maintenance is ongoing")
            self.watch()
            
if __name__ == "__main__":
    srv = Server()
    try:
        srv.watch()
    except socket.timeout:
        print("The server is down! ")
        srv.watch()
    except ConnectionRefusedError: 
        time.sleep(60)
        srv.watch()
    except OSError:
        print("No route to host, trying again")
        