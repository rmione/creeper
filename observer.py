from mcstatus import MinecraftServer
import os
import json

"""
Secrets file hides sensitive info, also will probably be filled in by a command line version of the setup. 
For now, just this though
"""
SECRETS = json.load(open(os.getcwd() + "/secrets.json"))

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


