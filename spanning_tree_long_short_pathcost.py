from netmiko import ConnectHandler
from paramiko.ssh_exception import SSHException
from netmiko import NetmikoTimeoutException
import csv
import sys
import re
import datetime
import time

with open("no_login_through_ssh_or_telnet.csv", "w", newline='') as filetypeobject:
    header = ["switchname"]
    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
    dictwritertypeobject.writeheader()

with open("pathcosts.csv", "w", newline='') as filetypeobject:
    header = ["switchname", "pathcosts"]
    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
    dictwritertypeobject.writeheader()


def pusher(connection, switch):
    print(f"working on {switch}....")
    x = connection.send_command("sh run all | sec method")
    y = x.splitlines()
    for i in y:
        z = i.split()
        if 'spanning-tree' in z and 'pathcost' in z:
            with open("pathcosts.csv", "a", newline='') as filetypeobject:
                header = ["switchname", "pathcosts"]
                dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
                dictwritertypeobject.writerow({'switchname':switch, 'pathcosts':z[-1]})
                connection.disconnect()
        else: pass

    
    
def reachability(switchlist):        
    global connection
    for switch in switchlist:
        try:
            kwargs = {
                'device_type': 'cisco_ios','ip': switch,'username': '*********','password': '********','port':'22'
                }
            connection = ConnectHandler(**kwargs)
            pusher(connection, switch)                        
        except:
            try:
                kwargs = {
                    'device_type': 'cisco_ios_telnet','ip': switch,'username': '**********','password': '*********','port':'23'
                    }
                connection = ConnectHandler(**kwargs)
                pusher(connection, switch)
            except:
                print("can't login through ssh or telnet", switch)
                with open("no_login_through_ssh_or_telnet.csv", "a", newline='') as filetypeobject:
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
        
