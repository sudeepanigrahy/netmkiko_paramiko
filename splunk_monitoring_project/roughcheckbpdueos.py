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

global h
h = ['timestamp', 'switch name','interface name','configuration','remarks']

with open("output.csv", "w", newline='') as filetypeobject:
    header = h
    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
    dictwritertypeobject.writeheader()

def work(connection, switch):
    #['Timestamp','Switch Name', 'Interface Name', 'Configuration', 'Comments']
    current_time = time.time()
    formatted_time = datetime.fromtimestamp(current_time).strftime("%m-%d-%Y %H:%M:%S") 
        
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

    #===========================================================

    list4 = []
    for i in range(0, len(dtpo1)):
        list3 = list(dtpo1.iloc[i].values)
        if 'trunk' in list3 or 'routed' in list3 or 'MLAG' in list3:
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
                elif 'Et' in str(dtpo1.iloc[i][j]):
                    dtpo1.iloc[i][j] = str(dtpo1.iloc[i][j]).replace("Et", "Ethernet")
                    list4.append(dtpo1.iloc[i][j])
                    

    res_list = []
    for i in list4:
        for j in range(0, len(dtpo3)):
            if i in list(dtpo3.iloc[j].values):
                if j == len(dtpo3)-1:
                    res_list.append({'timestamp': formatted_time,
                                  'switch name': switch, 
                                  'interface name': i, 
                                  'configuration': 'no', 
                                  'remarks': 'bpdu configuration missing'
                                  })
                    break
                    
                elif 'bpduguard' in list(dtpo3.iloc[j+1].values):
                    res_list.append({'timestamp': formatted_time,
                                  'switch name': switch, 
                                  'interface name': i, 
                                  'configuration': 'yes', 
                                  'remarks': ''
                                  })
                    break
                elif 'bpduguard' not in list(dtpo3.iloc[j+1].values):
                    res_list.append({'timestamp': formatted_time,
                                  'switch name': switch, 
                                  'interface name': i, 
                                  'configuration': 'no', 
                                  'remarks': 'bpdu configuration missing'
                                  })
            else: continue
        
    for i in res_list:
        with open("output.csv", "a", newline='') as filetypeobject:
            header = h
            dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
            dictwritertypeobject.writerow({h[0]: i[h[0]] , h[1]: i[h[1]], h[2]: i[h[2]], h[3]:i[h[3]], h[4]: i[h[4]]})
            connection.disconnect()
    
    
    #print(res_list, dtpo1, 4*'\n', dtpo3)
    #print(res_list)

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
            'device_type': 'arista_eos','ip': i,'username': '**********','password': '**********','port':'22'
            }
        connection = ConnectHandler(**kwargs)
    except:
        try:
            kwargs = {
                'device_type': 'arista_eos_telnet','ip': i,'username': '**********','password': '**********','port':'23'
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

