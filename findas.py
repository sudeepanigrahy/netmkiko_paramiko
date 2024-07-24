from netmiko import ConnectHandler
from paramiko.ssh_exception import SSHException
from netmiko import NetmikoTimeoutException
import csv
import sys
import re
import datetime
import time



def findas(connection, switch):
    x = connection.send_command("sh cdp nei")
    y = x.splitlines()
    z = []
    for i in y:
        if 'as' in i:
            z.append(i)
    for i in z:
        print(i)

            


def reachability(switchlist):        
    global connection
    for switch in switchlist:
        try:
            kwargs = {
                'device_type': 'cisco_ios','ip': switch,'username': 'spanigrahy','password': 'Sueme@0125','port':'22'
                }
            connection = ConnectHandler(**kwargs)
            findas(connection, switch)                        
        except:
            try:
                kwargs = {
                    'device_type': 'cisco_ios','ip': switch,'username': 'spanigrahy','password': 'Sueme@0125','port':'23'
                    }
                connection = ConnectHandler(**kwargs)
                findas(connection, switch)
            except:
                print("AIN'T HAPPENING FOR", switch)
                

                
with open("one.csv", "r") as filetypeobject:
    header = ["switchname"]
    dictreadertypeobject = csv.DictReader(filetypeobject, fieldnames = header)
    inputswitchlist = []
    for i in dictreadertypeobject:
        inputswitchlist.append(i["switchname"])
    inputswitchlist.pop(0)
    reachability(inputswitchlist)  

