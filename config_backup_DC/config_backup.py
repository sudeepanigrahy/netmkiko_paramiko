from netmiko import ConnectHandler
from paramiko.ssh_exception import SSHException
from netmiko import NetmikoTimeoutException
import csv
import sys
import re
#import datetime
from datetime import datetime
import time
import pandas as pd

with open("unconnectables.csv", "w", newline='') as filetypeobject:
    header = ["switchname"]
    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
    dictwritertypeobject.writeheader()

def work(connection, switch):
    
    running_config = connection.send_command("sh env power")
    #commands = ["do sh env all", "do sh env status"]
    #running_config = connection.send_config_set(commands)
    connection.send_command("wr", read_timeout=50)
    #sh_ip_route = connection.send_command("sh ip route")
    #sh_ip_eigrp_topology = connection.send_command("sh ip eigrp topology")
    #sh_ip_access_lists = connection.send_command("sh ip access-lists")
    
    conf_file = f"{switch}.csv"
    print(f"Saving the output to file: {conf_file} \n")
    with open(conf_file, "w") as filetypeobject:
        #filetypeobject.write("show running-config"+"\n")
        filetypeobject.write(running_config)
        #filetypeobject.write(3*"\n")
        #filetypeobject.write("show ip route"+"\n")
        #filetypeobject.write(sh_ip_route)
        #filetypeobject.write(3*"\n")
        #filetypeobject.write("sh ip eigrp topology"+"\n")
        #filetypeobject.write(sh_ip_eigrp_topology)
        #filetypeobject.write(sh_ip_access_lists)
            

with open("input1.csv", "r") as filetypeobject:
    header = ["switchname"]
    dictreadertypeobject = csv.DictReader(filetypeobject, fieldnames = header)
    inputswitchlist = []
    for i in dictreadertypeobject:
        inputswitchlist.append(i["switchname"])
    inputswitchlist.pop(0)
    #reachability(inputswitchlist)    
    
for i in inputswitchlist:
    print(f"working on {i}...")
    try:
        kwargs = {
            'device_type': 'arista_eos','ip': i,'username': 'spanigrahy','password': 'Sueme@0129','port':'22'
            }
        connection = ConnectHandler(**kwargs)
    except:
        try:
            kwargs = {
                'device_type': 'arista_eos_telnet','ip': i,'username': 'spanigrahy','password': 'Sueme@0129','port':'23'
                }
            connection = ConnectHandler(**kwargs)
        except:
            print("AIN'T HAPPENING FOR", i)
            with open("unconnectables.csv", "a", newline='') as filetypeobject:
                header = ["switchname"]
                dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
                dictwritertypeobject.writerow({'switchname': i})
                connection.disconnect()
            continue
    work(connection, i)
