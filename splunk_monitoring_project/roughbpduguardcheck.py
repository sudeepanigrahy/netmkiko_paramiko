from netmiko import ConnectHandler
import pandas as pd
import csv
import time
from datetime import datetime

#['Timestamp','Switch Name', 'Interface Name', 'Configuration', 'Comments']
current_time = time.time()
formatted_time = datetime.fromtimestamp(current_time).strftime("%m-%d-%Y %H:%M:%S") 


#switch = "sg209-b1rm5x-as6-cn240"
switch = 'sg624-aamr0-aep10-isilon51-as1-sn-vpc403'
#switch = "sg211-frm4-as3-fbmn.wlsg.micron.com"
#switch = "sg211-frm7-as2-fbmn.wlsg.micron.com"
#switch = "sg211-cr2-as1-fbmn.wlsg.micron.com"
#switch = "sg211-frm7-as1-fbmn.wlsg.micron.com"

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
    
test_string1 = connection.send_command("sh int status")
test_string2 = connection.send_command("show run")
test_list1 = test_string1.splitlines()
test_list2 = test_string2.splitlines()

test_list3= []
for i in test_list2:
    if 'Ethernet' in i or 'bpdu' in i:
        test_list3.append(i)
        
dtpo = pd.DataFrame(test_list1)
list1 = dtpo.values[0][0].split()
dtpo1 = pd.DataFrame(list1).T
for i in range(1,len(test_list1)):
    xx = dtpo.values[i][0].split()
    
    for j in range(len(xx)):
        dtpo1.loc[i, j] = xx[j]

        
dtpo2 = pd.DataFrame(test_list3)
list2 = dtpo2.values[0][0].split()
dtpo3 = pd.DataFrame(list2).T

for i in range(1,len(test_list3)):
    xx = dtpo2.values[i][0].split()
    
    for j in range(len(xx)):
        dtpo3.loc[i, j] = xx[j]

#print(dtpo1[0].values)
#dtpo1.to_csv('dtpo1bpdu.csv')
#===========================================================

list4 = []
for i in range(0, len(dtpo1)):
    list3 = list(dtpo1.iloc[i].values)
    if 'trunk' in list3 or 'routed' in list3:
        continue
    else:
        for j in range(0, len(list3)):            
            if 'Gi' in str(dtpo1.iloc[i][j]):
                dtpo1.iloc[i][j] = str(dtpo1.iloc[i][j]).replace("Gi", "GigabitEthernet")
                list4.append(dtpo1.iloc[i][j]) 
            elif 'Fa' in str(dtpo1.iloc[i][j]):
                dtpo1.iloc[i][j] = str(dtpo1.iloc[i][j]).replace("Fa", "FastEthernet")
                list4.append(dtpo1.iloc[i][j])
            elif 'Te' in str(dtpo1.iloc[i][j]):
                dtpo1.iloc[i][j] = str(dtpo1.iloc[i][j]).replace("Te", "TenGigabitEthernet")
                list4.append(dtpo1.iloc[i][j])   
            elif 'Eth' in str(dtpo1.iloc[i][j]):
                dtpo1.iloc[i][j] = str(dtpo1.iloc[i][j]).replace("Eth", "Ethernet")
                list4.append(dtpo1.iloc[i][j])
                

list5 = []
for i in list4:
    for j in range(0, len(dtpo3)):
        if i in list(dtpo3.iloc[j].values):
            if j == len(dtpo3)-1:
                list5.append({'timestamp': formatted_time,
                              'switch Name': switch, 
                              'interface Name': i, 
                              'configuration': 'no', 
                              'remarks': 'bpdu configuration missing'
                              })
                break
                
            elif 'bpduguard' in list(dtpo3.iloc[j+1].values):
                list5.append({'timestamp': formatted_time,
                              'switch Name': switch, 
                              'interface Name': i, 
                              'configuration': 'yes', 
                              'remarks': ''
                              })
                break
            elif 'bpduguard' not in list(dtpo3.iloc[j+1].values):
                list5.append({'timestamp': formatted_time,
                              'switch Name': switch, 
                              'interface Name': i, 
                              'configuration': 'no', 
                              'remarks': 'bpdu configuration missing'
                              })
        else: continue

print(list5)
