from netmiko import ConnectHandler
import pandas as pd
import csv
import time
from datetime import datetime

def usedvlans(string1):
    test_string1 = string1
    test_list1 = test_string1.splitlines()
    
     
    dtpo = pd.DataFrame(test_list1)
    list1 = dtpo.values[0][0].split()
    dtpo1 = pd.DataFrame(list1).T
    
    for i in range(1,len(test_list1)):
        xx = dtpo.values[i][0].split()
        
        for j in range(len(xx)):
            dtpo1.loc[i, j] = xx[j]
            
    used_vlans = []
    for i in range(len(dtpo1)):
        p = list(dtpo1.iloc[i].values)
        z = [str(o) for o in p]
        for j,k in enumerate(z):
            if 'connected' in k or 'notconnect' in k or 'disabled' in k:
                try:
                    vlan_num = int(p[j+1])
                    used_vlans.append(str(vlan_num))
                    break
                except: break
        continue
    
    used_vlanss = list(set(used_vlans))
    for i in used_vlanss:
        if i == '1':
            used_vlanss.remove(i)
        else: pass
    return used_vlanss


if __name__=='__main__':
    current_time = time.time()
    formatted_time = datetime.fromtimestamp(current_time).strftime("%m-%d-%Y %H:%M:%S") 


    try:
        kwargs = {
            'device_type': 'cisco_ios','ip': switch,'username': '********','password': '*********'
            }
        connection = ConnectHandler(**kwargs)
    except:
        kwargs = {
            'device_type': 'cisco_ios_telnet','ip': switch,'username': '********','password': '********'
            }
        connection = ConnectHandler(**kwargs)
        
