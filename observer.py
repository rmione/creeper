from mcstatus import MinecraftServer
import os
import json
import asyncio
import comm 
import socket
import time
"""
Secrets file hides sensitive info, also will probably be filled in by a command line version of the setup. 
For now, just this though
"""
SECRETS = json.load(open(os.getcwd() + "/secrets.json"))
count  = 0 
class Server:
    def __init__(self):
        self.server = MinecraftServer.lookup(SECRETS['ip'])

    def info(self):
        """
        Sends a request to the desired server, and returns the JSON object returned by mcstatus's status method.
        We may want to do more later.

        :return:
        """
        status = self.server.status()
        ping = int(self.server.ping())
        # players = self.server.query() # Returns playerlist
        data = {'players': status.players.online, 'ping': ping}
        return data


    def watch(self, previous=None):
        # try:
        #     data = self.info()

        #     # count += 1 # This means that the server response was good. 
        #     # asyncio.sleep(5*60) # Wait 5min 
        #     # self.watch() # Recurse 
        # except socket.timeout: 
        #     # Server is off or can't connect...
        #     asyncio.sleep(5*60)
        print(previous)
        try:
            data = self.info() # check the info, get players, etc... 
            if data['players'] != 0:
                current = 'Active'
            else: 
                current = 'Inactive'
            time.sleep(5*60) # Sleep 5 mins.. we wait

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

            # if previous == 'Inactive' and current == 'Active': 
            #     self.watch(previous=current) 
            # if previous == 'Active' and current == 'Inactive':
            #     self.watch(previous=current) 
            # if




        except socket.timeout:
            print("The server is down! ")
            self.watch()
        except ConnectionRefusedError: 
            time.sleep(60)
            self.watch()

if __name__ == "__main__":
    srv = Server()
    srv.watch()