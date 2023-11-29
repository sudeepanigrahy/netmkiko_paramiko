"""
A script to push the AAA config onto switches
"""

from netmiko import ConnectHandler
from paramiko.ssh_exception import SSHException 
from netmiko import NetmikoTimeoutException
import csv
import sys 
import datetime
import time

with open("unconnectables.csv", "w", newline='') as filetypeobject: 
    header = ["switchname"]
    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
    dictwritertypeobject.writeheader()

def pusher(connection, switch):
    commands_list = ["aaa group server tacacs+ ******", "server-private *.*.*.* key 7 ***************", "end", "wr"]
    output = connection.send_config_set(commands_list)
    print(output)

def reachability(switchlist):
    global connection
    for switch in switchlist:
        try:
            kwargs = {
                'device_type': 'cisco_ios', 'ip': switch, 'username': '*******', 'password': '********', 'port':"22"
            }
            connection = ConnectHandler(**kwargs)
            pusher(connection, switch)
        except:
            try:
                kwargs = {
                'device_type': 'cisco_ios', 'ip': switch, 'username': '*******', 'password': '*********', 'port' : 22
                }
                connection = ConnectHandler(**kwargs)
                pusher(connection, switch)
            except:
                print("AIN'T HAPPENING FOR", switch)
                with open("unconnectables.csv", "a", newline='') as filetypeobject:
                    header = ["switchname"]
                    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
                    dictwritertypeobject.writerow({'switchname': switch})
                    connection.disconnect()

with open("input.csv", "r") as filetypeobject:
    header = ["switchname"]
    dictreadertypeobject = csv.DictReader(filetypeobject, fieldnames = header)
    inputswitchlist = []
    for i in dictreadertypeobject:
        inputswitchlist.append(i["switchname"])
    inputswitchlist.pop(0)
    reachability(inputswitchlist)

