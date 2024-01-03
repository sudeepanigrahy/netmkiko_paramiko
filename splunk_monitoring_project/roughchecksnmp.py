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

switch = 'sg209-b1mr4d-cs2-vsn-vpc'
try:
    kwargs = {
        'device_type': 'cisco_ios','ip': switch,'username': 'spanigrahy','password': 'Sueme@0125','port':'22'
        }
    connection = ConnectHandler(**kwargs)
except:
    kwargs = {
        'device_type': 'cisco_ios','ip': switch,'username': 'spanigrahy','password': 'Sueme@0125','port':'23'
        }
    connection = ConnectHandler(**kwargs)
    
test_string1 = connection.send_command("sh run")
#test_string2 = connection.send_command("show vlan br")
test_list1 = test_string1.splitlines()
#test_list2 = test_string2.splitlines()

if "sg209" in switch:
    ip1 = "10.160.20.60"
    ip2 = "10.160.21.9"
    if "rc4sing" in test_string1 and "wc4sing" in test_string1 and ip1 in test_string1 and ip2 in test_string1:
        discrepancy = "no"
        remark = ""
    else:
        discrepancy = "yes"
        remark = "SNMP server missing"
elif "sg624" in switch:
    ip1 = "10.193.189.120"
    ip2 = "10.193.189.26"
    if "rc4sing" in test_string1 and "wc4sing" in test_string1 and ip1 in test_string1 and ip2 in test_string1:
        discrepancy = "no"
        remark = ""
    else:
        discrepancy = "yes"
        remark = "SNMP server missing"
elif "sg211" in switch:
    ip1 = "172.25.243.229"
    ip2 = "172.25.243.230"
    if "rc4sing" in test_string1 and "wc4sing" in test_string1 and ip1 in test_string1 and ip2 in test_string1:
        discrepancy = "no"
        remark = ""
    else:
        discrepancy = "yes"
        remark = "SNMP server missing"
else:
    pass


res_dict = {
    'timestamp': formatted_time,
    'switch name': switch,
    'discrepancy': discrepancy,
    'remarks': remark
    }
res_list.append(res_dict)
        
print(res_list)
#print(test_string1)