import paramiko 
from observer import SECRETS
from dotenv import load_dotenv
import os
load_dotenv()

USER = os.getenv('SSH_USER') 
PASS = os.getenv('SSH_PASS')


def server_shutdown():
    client = paramiko.SSHClient() # instantiate class
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(SECRETS['ip'], username=USER, password=PASS) # Get IP from secrets file


    stdin_, stdout_, stderr_ = client.exec_command("screen -r -X eval 'stuff \"stop\"\\\\015'")

    lines = stdout_.readlines()
    for line in lines:
        print(line)
