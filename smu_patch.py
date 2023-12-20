"""
A script to parse the SMU-PATCHED
"""

from netmiko import ConnectHandler
import csv
import sys
import re
import datetime
import time
from netmiko.exceptions import NetMikoAuthenticationException
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import SSHException

 
with open("okay.csv", "w", newline='') as filetypeobject:
    header = ["switchname"]
    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
    dictwritertypeobject.writeheader()
    
with open("not-okay.csv", "w", newline='') as filetypeobject:
    header = ["switchname"]
    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
    dictwritertypeobject.writeheader()

def pusher(connection, switch):
    print(f"Inside parser for {switch}'s operations")
    sh_ver = connection.send_command("show version")
    lines = sh_ver.splitlines()
    counter = []
    for i in lines:
        words = i.split(" ")
        if "SMU-PATCHED" in words:
            counter.append('1')
            with open("okay.csv", "a", newline='') as filetypeobject:
                header = ["switchname"]
                dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
                dictwritertypeobject.writerow({'switchname': switch})
                connection.disconnect()            
            break
        else: continue
    
    if len(counter)==0:
        with open("not-okay.csv", "a", newline='') as filetypeobject:
            header = ["switchname"]
            dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
            dictwritertypeobject.writerow({'switchname': switch})
            connection.disconnect()
    else: pass
        
    
   
def reachability(switchlist):        
    global connection
    for switch in switchlist:
        try:
            kwargs = {
                'device_type': 'cisco_ios','ip': switch,'username': '**********','password': '**********','port':'22'
                }
            connection = ConnectHandler(**kwargs)
            pusher(connection, switch)
            continue            
        except:
            try:
                kwargs = {
                    'device_type': 'cisco_ios_telnet','ip': switch,'username': '***********','password': '***********','port':'23'
                    }
                connection = ConnectHandler(**kwargs)
                pusher(connection, switch)
                continue
            
            except NetMikoAuthenticationException:
                print(sys.exc_info()[0])
                print("Authentication Failed")
                
            except NetMikoTimeoutException:
                print(sys.exc_info()[0])
                print("Timeout Exception, so possibly wrong hostname")
            
            except SSHException:
                print(sys.exc_info()[0])
                print("Something wrong with the SSH Connection")
            
            except:
                print(sys.exc_info()[0])
                print("Exception Occurred")
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
    
                       

        
