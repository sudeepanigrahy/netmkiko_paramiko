from netmiko import ConnectHandler
import pandas as pd
import csv
import time
from datetime import datetime

#return ['timestamp', 'switch name', 'vlan', 'discrepancy', 'mac'
current_time = time.time()
formatted_time = datetime.fromtimestamp(current_time).strftime("%m-%d-%Y %H:%M:%S") 


switch = "sg209-b1rm5x-as6-cn240"

try:
    kwargs = {
        'device_type': 'cisco_nxos','ip': switch,'username': 'nwtools','password': '!1Jst4Tls7!'
        }
    connection = ConnectHandler(**kwargs)
except:
    kwargs = {
        'device_type': 'cisco_ios_telnet','ip': switch,'username': 'nwtools','password': '!1Jst4Tls7!'
        }
    connection = ConnectHandler(**kwargs)
    

test_string1 = connection.send_command("sh cdp nei")
test_string2 = connection.send_command("show spanning-tree root")
test_list1 = test_string1.splitlines()
test_list2 = test_string2.splitlines()
 
dtpo = pd.DataFrame(test_list1)
list1 = dtpo.values[0][0].split()
dtpo1 = pd.DataFrame(list1).T

for i in range(1,len(test_list1)):
    xx = dtpo.values[i][0].split()
    
    for j in range(len(xx)):
        dtpo1.loc[i, j] = xx[j]

uplinks = {}
for i in range(0,dtpo1[0].size):
    if "as" in switch:
        if "ds" in dtpo1.iloc[i, 0]:
            #print('yes')
            uplinks[dtpo1.iloc[i,0]] = dtpo1.iloc[i+1,0] + dtpo1.iloc[i+1,1]
    elif "ds" in switch:
        if "cs" in dtpo1.iloc[i, 0]:
            #print('yes')
            uplinks[dtpo1.iloc[i,0]] = dtpo1.iloc[i+1,0] + dtpo1.iloc[i+1,1]
    else: pass    
        
#-------------------------------------------------------------------


dtpo2 = pd.DataFrame(test_list2)
list2 = dtpo2.values[0][0].split()
dtpo3 = pd.DataFrame(list2).T

for i in range(1,len(test_list2)):
    xx = dtpo2.values[i][0].split()
    
    for j in range(len(xx)):
        dtpo3.loc[i, j] = xx[j]
        
vlan_dict = {}
mac_dict = {}
for i in range(0,len(dtpo3[0].values)):
    if "VLAN0" in dtpo3[0].values[i]:
        vlan_dict[dtpo3[0].values[i]] = dtpo3.iloc[i, 7]
        mac_dict[dtpo3[0].values[i]] = dtpo3.iloc[i, 2]
    else: pass

#print(vlan_dict)   
#print("uplinks: ", uplinks)

#---------------------------------------------------------------------
root_port = ''
for i, j in uplinks.items():
    if "ds1" in i or "ds3" in i or "ds5" in i:
        root_port = j
    elif "cs1" in i:
        root_port = j
    else: pass
        
        
if 'Te' in root_port:
    #print(root_port)
    root_port = root_port.replace("Ten", "Te")
elif 'Gi' in root_port:
    root_port = root_port.replace("Gig", "Gi")


"""
#---------------------------------------------------------------------
#print(root_port, 10*"\n")
#print(vlan_dict)
#print(vlan_dict, dtpo3)
#print(mac_dict)
for i, j in vlan_dict.items():
    if j == root_port:
        print({'timestamp' : formatted_time,
                'switch name' : switch,
                'vlan' : i,
                'discrepancy': 'no',
                'mac': mac_dict[i]               
                })
    
    elif j != root_port:
        print({'timestamp' : formatted_time,
                'switch name' : switch,
                'vlan' : i,
                'discrepancy': 'yes',
                'mac': mac_dict[i]               
                })
"""   
checker_list=[]
for i,j in vlan_dict.items():
    if j == root_port:
        checker_list.append('no')
    else: checker_list.append('yes')
checker_listt = list(set(checker_list))

if 'no' in checker_listt and 'yes' not in checker_listt:
    return 'no'
elif 'no' in checker_listt and 'yes' in checker_listt:
    return 'yes'
elif 'yes' in checker_listt and 'no' not in checker_listt:
    return 'yes'
    
        
