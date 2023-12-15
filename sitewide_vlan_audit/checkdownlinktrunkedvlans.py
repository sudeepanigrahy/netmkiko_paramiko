from netmiko import ConnectHandler
import pandas as pd
import csv
import time
from datetime import datetime


def downlinktrunkedvlans(string1, string2, switch2):
    test_string1 = string1
    test_list1 = test_string1.splitlines()
    test_string2 = string2
    test_list2 = test_string2.splitlines()
     
    dtpo = pd.DataFrame(test_list1)
    list1 = dtpo.values[0][0].split()
    dtpo1 = pd.DataFrame(list1).T
    
    for i in range(1,len(test_list1)):
        xx = dtpo.values[i][0].split()
        
        for j in range(len(xx)):
            dtpo1.loc[i, j] = xx[j]
            
    downlink_port=[]
    switch2 = str(switch2.split(".****")[0])
    if 'svi' in switch2:
        switch2 = switch2.split("-svi")[0]
    else: pass
    #print(dtpo, '\n', dtpo1)
    #print(f"switch is : {switch2}")
    for i in range(len(dtpo1)):
        #print(dtpo1.iloc[i,0])
        #print(f"this is {dtpo1.iloc[i,0]} and {switch2}")
        if switch2.lower() in dtpo1.iloc[i,0].lower():
            #print(f"this is {dtpo1.iloc[i,0]} and {switch2}")
            downlink_port.append(str(dtpo1.iloc[i+1,0])+str(dtpo1.iloc[i+1,1]))
            #print(f"this is downlink_port: {downlink_port}")
        else: continue
    #print(f"Downlink port from checkdownlinktrunkedvlans is : {downlink_port}")
    
    downlink_port = list(map(lambda x: x.replace('Ten', 'Te') if 'Ten' in x \
                             else x.replace('Gig', 'Gi') if 'Gig' in x\
                                 else x.replace('Twe', 'Twe') if 'Twe' in x \
                                     else 'anomaly', downlink_port))    
    #print(f"Downlink port is : {downlink_port}")
    
    dtpo2 = pd.DataFrame(test_list2)
    list2 = dtpo2.values[0][0].split()
    dtpo3 = pd.DataFrame(list2).T
    
    for i in range(1,len(test_list2)):
        xx = dtpo2.values[i][0].split()
        
        for j in range(len(xx)):
            dtpo3.loc[i, j] = xx[j]
    
    vlans = []
    for i in list(dtpo3[0].values):
        try:
            if int(i)>0 and int(i)<1002:
                vlans.append(i)
            elif int(i)>1005 and int(i)<=4096:
                vlans.append(i)
        except:
            continue
    vlans.sort()
    
    return [vlans, downlink_port]
    
    
if __name__=='__main__':
    """
    try:
        kwargs = {
            'device_type': 'cisco_nxos','ip': switch1,'username': '********','password': '********'
            }
        connection = ConnectHandler(**kwargs)
    except:
        kwargs = {
            'device_type': 'cisco_ios_telnet','ip': switch1,'username': '******','password': '********'
            }
        connection = ConnectHandler(**kwargs)
"""      
