from netmiko import ConnectHandler
from paramiko.ssh_exception import SSHException
from netmiko import NetmikoTimeoutException
import csv
import sys
import re
import datetime
import time

with open("outputdatafile_sg.csv", "w", newline='') as filetypeobject:
    header = ["switchname", "version", "serial", "model", "uptime"]
    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
    dictwritertypeobject.writeheader()

with open("unconnectables_sg.csv", "w", newline='') as filetypeobject:
    header = ["switchname"]
    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
    dictwritertypeobject.writeheader()

def ios(connection, switch, version, up):  
    ver = version
    uptime = up
    
    fetch_model = connection.send_command("show version | i Model number")
    list_model = fetch_model.split()
    model = list_model[3]

    fetch_serial = connection.send_command("show version | i System serial number")
    list_serial = fetch_serial.split()
    serial = list_serial[4]
        
    with open("outputdatafile_sg.csv", "a", newline='') as filetypeobject:
        header = ["switchname", "version", "serial", "model", "uptime"]
        dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
        dictwritertypeobject.writerow({'switchname': switch , 'version': ver, 'serial': serial, 'model': model, 'uptime':uptime})
        connection.disconnect()
        
    
def iosxe(connection, switch, version, up):
    ver = version
    uptime = up

    fetch_model = connection.send_command("show version | i Model Number")
    list_model = fetch_model.split()
    model = list_model[3]

    fetch_serial = connection.send_command("show version | i System Serial Number")
    list_serial = fetch_serial.split()
    serial = list_serial[4]  
    
    with open("outputdatafile_sg.csv", "a", newline='') as filetypeobject:
        header = ["switchname", "version", "serial", "model", "uptime"]
        dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
        dictwritertypeobject.writerow({'switchname': switch , 'version': ver, 'serial': serial, 'model': model, 'uptime':uptime})
        connection.disconnect()


def iosandiosxe(connection, switch, variety, version, up):
    ver = version
    uptime = up
    
    if variety == 1:
        fetch_model = connection.send_command("show version | i physical memory")
        list_model = fetch_model.split()
        model = list_model[1]

        fetch_serial = connection.send_command("show version | i Processor board ID")
        list_serial = fetch_serial.split()
        serial = list_serial[3]
       
        with open("outputdatafile_sg.csv", "a", newline='') as filetypeobject:            
            header = ["switchname", "version", "serial", "model", "uptime"]
            dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)            
            dictwritertypeobject.writerow({'switchname': switch , 'version': ver, 'serial': serial, 'model': model, 'uptime':uptime})
            connection.disconnect()
       
    elif variety == 2:
        fetch_model = connection.send_command("show version | i Model Number")
        list_model = fetch_model.split()
        model = list_model[3]

        fetch_serial = connection.send_command("show version | i System Serial Number")
        list_serial = fetch_serial.split()
        serial = list_serial[4]
       
        with open("outputdatafile_sg.csv", "a", newline='') as filetypeobject:          
            header = ["switchname", "version", "serial", "model", "uptime"]
            dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)           
            dictwritertypeobject.writerow({'switchname': switch , 'version': ver, 'serial': serial, 'model': model, 'uptime':uptime})
            connection.disconnect()


def differentiator(connection, switch):
    
    fetch_version = connection.send_command("show version | i Version")
    list_version = fetch_version.splitlines()
    first_line = list_version[0]
    first_line_elements = first_line.split()

    for i in range(1, len(first_line_elements) + 1):
        if first_line_elements[i] == "Version":
            ver = first_line_elements[i+1]
            break
    version = ver.replace(",", "")
 
    s = connection.send_command("show version | i uptime")
    y = s.split()    
    x = {"years":"0","weeks":"0", "days":"0", "hours":"0", "minutes":"0"}   
        
    for i in range(4, len(y) + 1):
        
        if y[i-1] == "year," or y[i-1] == "years,":
            x["years"] = y[i-2]
            continue
        elif y[i-1] == "week," or y[i-1] == "weeks,":
            x["weeks"] = y[i-2]
            continue
        elif y[i-1] == "day," or y[i-1] == "days,":
            x["days"] = y[i-2]
            continue
        elif y[i-1] == "hour," or y[i-1] == "hours,":
            x["hours"] = y[i-2]
            continue
        elif y[i-1] == "minute" or y[i-1] == "minutes":
            x["minutes"] = y[i-2]
            continue	 	 
     
    w=(int(x["weeks"])*7)/365
    d=(int(x["days"])/365)
    h=(int(x["hours"])/(365*24))
    m=(int(x["minutes"])/(365*24*60))
    result=int(x["years"])+w+d+h+m
    up_time = "%0.6f"%result

    
    yy = connection.send_command("show version")
    if "Cisco IOS Software" in yy and "System serial number" in yy and "System Serial Number" not in yy:
        ios(connection, switch, version, up_time)       
    elif "Cisco IOS XE Software" in yy and "System Serial Number" in yy:
        iosxe(connection, switch, version, up_time)
    elif "Cisco IOS Software, IOS-XE Software" in yy:        
        if "Processor board ID" in yy and "System Serial Number" not in yy:
            iosandiosxe(connection, switch, 1, version, up_time)
        elif "System Serial Number" in yy and "Assembly" in yy:
            iosandiosxe(connection, switch, 2, version, up_time)
        else:
            print("THERE IS ANOTHER VARIETY FOR IOSANDIOS-XE", switch )
            #if there's another type of iosandios-xe, create logic for that
    else:
        print("THIS IS A NEW SOFTWARE",switch)
  



def reachability(switchlist):        
    global connection
    for switch in switchlist:
        try:
            kwargs = {
                'device_type': 'cisco_ios','ip': switch,'username': '**********','password': '**********','port':'22'
                }
            connection = ConnectHandler(**kwargs)
            differentiator(connection, switch)                        
        except:
            try:
                kwargs = {
                    'device_type': 'cisco_ios','ip': switch,'username': '**********','password': '**********','port':'23'
                    }
                connection = ConnectHandler(**kwargs)
                differentiator(connection, switch)
            except:
                print("AIN'T HAPPENING FOR", switch)
                with open("unconnectables_sg.csv", "a", newline='') as filetypeobject:
                    header = ["switchname"]
                    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
                    dictwritertypeobject.writerow({'switchname': switch})
                    connection.disconnect()

                
with open("sg.csv", "r") as filetypeobject:
    header = ["switchname"]
    dictreadertypeobject = csv.DictReader(filetypeobject, fieldnames = header)
    inputswitchlist = []
    for i in dictreadertypeobject:
        inputswitchlist.append(i["switchname"])
    inputswitchlist.pop(0)
    reachability(inputswitchlist)                
    
    
    
    
    
    
    
    
    
    
