from netmiko import ConnectHandler
from paramiko.ssh_exception import SSHException
from netmiko import NetmikoTimeoutException
import csv
import sys
import re
#import datetime
from datetime import datetime
import time


def work(connection, switch):
    #return ['timestamp', 'switch name', 'uptime']
    #once this function is called, it'll return the above dict inside a list, to the caller.
    
    current_time = time.time()
    formatted_time = datetime.fromtimestamp(current_time).strftime("%m-%d-%Y %H:%M:%S") 
    res_list = []
    
    #switch = "***********"

    test_string1 = connection.send_command("sh version")
    
    
    #test_string2 = connection.send_command("show int trunk")
    #test_list1 = test_string1.splitlines()
    #test_list2 = test_string2.splitlines()
    """
    dtpo = pd.DataFrame(test_list1)
    list1 = dtpo.values[0][0].split()
    dtpo1 = pd.DataFrame(list1).T

    for i in range(1,len(test_list1)):
        xx = dtpo.values[i][0].split()
        
        for j in range(len(xx)):
            dtpo1.loc[i, j] = xx[j]
            
    dtpo2 = pd.DataFrame(test_list2)
    list2 = dtpo2.values[0][0].split()
    dtpo3 = pd.DataFrame(list2).T

    for i in range(1,len(test_list2)):
        xx = dtpo2.values[i][0].split()
        
        for j in range(len(xx)):
            dtpo3.loc[i, j] = xx[j]      
    """

    
    list_version = test_string1.splitlines()
    uptime_line = []
    for line in list_version:
        if 'Uptime' in line:
            uptime_line.append(line)    
    uptime_line_elements = uptime_line[0].split()
    x = {"years":"0","weeks":"0", "days":"0", "hours":"0", "minutes":"0"}   
        
    for i in range(2, len(uptime_line_elements) + 1):
        
        if uptime_line_elements[i-1] == "year," or uptime_line_elements[i-1] == "years,":
            x["years"] = uptime_line_elements[i-2]
            continue
        elif uptime_line_elements[i-1] == "week," or uptime_line_elements[i-1] == "weeks,":
            x["weeks"] = uptime_line_elements[i-2]
            continue
        elif uptime_line_elements[i-1] == "day," or uptime_line_elements[i-1] == "days," or uptime_line_elements[i-1] == "day(s),":
            x["days"] = uptime_line_elements[i-2]
            continue
        elif uptime_line_elements[i-1] == "hour" or uptime_line_elements[i-1] == "hours" or uptime_line_elements[i-1] == "hour(s),":
            x["hours"] = uptime_line_elements[i-2]
            continue
        elif uptime_line_elements[i-1] == "minute" or uptime_line_elements[i-1] == "minutes" or uptime_line_elements[i-1] == "minute(s),":
            x["minutes"] = uptime_line_elements[i-2]
            continue	 	  
    
    w=(int(x["weeks"])*7)/365
    d=(int(x["days"])/365)
    h=(int(x["hours"])/(365*24))
    m=(int(x["minutes"])/(365*24*60))
    result=int(x["years"])+w+d+h+m
    up_time = "%0.3f"%result
    
    res_dict = {
        'timestamp': formatted_time,
        'switch name': switch,
        'uptime': up_time
        }
    res_list.append(res_dict)
    
    print(res_list)    

    #return res_list



with open("input2.csv", "r") as filetypeobject:
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
            'device_type': 'cisco_nxos','ip': i,'username': '***********','password': '***********','port':'22'
            }
        connection = ConnectHandler(**kwargs)
    except:
        try:
            kwargs = {
                'device_type': 'cisco_ios_telnet','ip': i,'username': '***********','password': '***********','port':'23'
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

