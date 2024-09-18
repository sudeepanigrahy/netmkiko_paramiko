from netmiko import ConnectHandler
import pandas as pd
import csv
import time
from datetime import datetime


#return ['timestamp', 'switch name', 'discrepancy', 'remarks']
#once this function is called, it'll return the above dict inside a list, to the caller.


current_time = time.time()
formatted_time = datetime.fromtimestamp(current_time).strftime("%m-%d-%Y %H:%M:%S")        
res_list = []

switch = 'sg624-aamr0-aep10-isilon51-as1-sn-vpc403'

try:
    kwargs = {
        'device_type': 'cisco_nxos','host': switch,'username': ********,'password': ********
        }
    connection = ConnectHandler(**kwargs)
except:
    kwargs = {
        'device_type': 'cisco_ios_telnet','host': switch,'username': ********,'password': ********
        }
    connection = ConnectHandler(**kwargs)
    
test_string1 = connection.send_command("sh ver")
#test_string2 = connection.send_command("show vlan br")
test_list1 = test_string1.splitlines()
#test_list2 = test_string2.splitlines()

#return ['timestamp', 'switch name', 'uptime']
#once this function is called, it'll return the above dict inside a list, to the caller.

current_time = time.time()
formatted_time = datetime.fromtimestamp(current_time).strftime("%m-%d-%Y %H:%M:%S") 
res_list = []

list_version = test_string1.splitlines()
uptime_line = []
for line in list_version:
    if 'uptime' in line:
        uptime_line.append(line)    
uptime_line_elements = uptime_line[0].split()
x = {"years":"0","weeks":"0", "days":"0", "hours":"0", "minutes":"0"}   
    
for i in range(4, len(uptime_line_elements) + 1):
    
    if uptime_line_elements[i-1] == "year," or uptime_line_elements[i-1] == "years,":
        x["years"] = uptime_line_elements[i-2]
        continue
    elif uptime_line_elements[i-1] == "week," or uptime_line_elements[i-1] == "weeks,":
        x["weeks"] = uptime_line_elements[i-2]
        continue
    elif uptime_line_elements[i-1] == "day," or uptime_line_elements[i-1] == "days," or uptime_line_elements[i-1] == "day(s),":
        x["days"] = uptime_line_elements[i-2]
        continue
    elif uptime_line_elements[i-1] == "hour," or uptime_line_elements[i-1] == "hours," or uptime_line_elements[i-1] == "hour(s),":
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
up_time = "%0.6f"%result

res_dict = {
    'timestamp': formatted_time,
    'switch name': switch,
    'uptime': up_time
    }
res_list.append(res_dict)

print(res_list)
