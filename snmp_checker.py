from netmiko import ConnectHandler
import time
import os
import csv

with open("right_config.csv", "w", newline='') as filetypeobject:
    header = ["switchname"]
    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
    dictwritertypeobject.writeheader()

with open("wrong_config.csv", "w", newline='') as filetypeobject:
    header = ["switchname"]
    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
    dictwritertypeobject.writeheader()

with open("cant_connect.csv", "w", newline='') as filetypeobject:
    header = ["switchname"]
    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
    dictwritertypeobject.writeheader()

def config_checker(switch, connection):
    running_config = connection.send_command("sh run")
    if "10.x.x.x" in running_config and "10.x.x.x" in running_config:
        with open("right_config.csv", "a", newline='') as filetypeobject:
            header = ['switchname']
            dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
            dictwritertypeobject.writerow({"switchname": switch})
            connection.disconnect()

    else:
        with open("wrong_config.csv", "a", newline='') as filetypeobject:
            header = ['switchname']
            dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
            dictwritertypeobject.writerow({"switchname": switch})
            connection.disconnect()

def reachability(inputlist):
    global connection
    for switch in inputlist:
        try:
            kwargs = {
                'device_type': 'cisco_ios', 'ip': switch, 'username': '*******', 'password': '********', 'port':"22"
            }
            connection = ConnectHandler(**kwargs)
            config_checker(switch, connection)

        except:
            try:
                kwargs = {
                'device_type': 'cisco_ios', 'ip': switch, 'username': '*******', 'password': '********', 'port':"23"
            } 
                connection = ConnectHandler(**kwargs)
                config_checker(switch, connection)

            except:
                with open("cant_connect.csv", "a", newline='') as filetypeobject:
                    header = ["switchname"]
                    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
                    dictwritertypeobject.writerow({"switchname": switch})
                    filetypeobject.close()

