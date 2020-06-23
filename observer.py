from mcstatus import MinecraftServer
import discord
import os
import json


# SECRETS = json.load(open(os.getcwd() + "/secrets.json"))
class Server:
    def __init__(self):
        self.server = MinecraftServer.lookup('192.168.0.222')#secrets.get('ip'))

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





if __name__ == '__main__':
    # print("bruh")
    # foo = Server()
    # print(foo.info())
    print("Nada")
