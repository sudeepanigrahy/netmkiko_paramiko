from netmiko import ConnectHandler
import pandas as pd
import csv
import time
from datetime import datetime


def vlanspriority(string1, string2):    
    test_string1 = connection.send_command("sh run")
    test_string2 = connection.send_command("show vlan br")
    test_list1 = test_string1.splitlines()
    test_list2 = test_string2.splitlines()
    
    dtpo = pd.DataFrame(test_list1)
    list1 = dtpo.values[0][0].split()
    dtpo1 = pd.DataFrame(list1).T
    
    for i in range(1,len(test_list1)):
        xx = dtpo.values[i][0].split()
        
        for j in range(len(xx)):
            dtpo1.loc[i, j] = xx[j]
    
    mask = dtpo1[0] == "spanning-tree"  
    dtpo2 = dtpo1[mask].iloc[0:, [2,3,4]]
    dtpo2 = dtpo2.dropna()
    
    vlans_priority_dict = {}
    vlans_total = []
    for i in range(len(dtpo2)):
        if dtpo2.iloc[i,0]=="type":
            break
        x = dtpo2.iloc[i,0].split(',')
        vlans_total.extend(x)
        
        if dtpo2.iloc[i,2] in list(vlans_priority_dict.keys()):
            vlans_priority_dict[dtpo2.iloc[i,2]].extend(x)     
        else:    
            vlans_priority_dict[dtpo2.iloc[i,2]] = x
    v=[]
    dash=[]      
    for i in vlans_total:
        if "-" in i:
            xx = i.split("-")
            v.extend(xx)
            dash.append(i)
            xxx = (int(xx[-1]) - int(xx[0]))-1
            if xxx==0:
                continue
            else:
                for j in range(xxx):
                    v.append(str(int(xx[0])+int(j)+1))  
    [vlans_total.append(x) for x in v]
    [vlans_total.remove(x) for x in dash]            
    vlans_total = [int(x) for x in vlans_total]  
    vlans_total.sort()        
    if int(1) in vlans_total: vlans_total.remove(int(1))             
    
    dtpo3 = pd.DataFrame(test_list2)
    list2 = dtpo3.values[0][0].split()
    dtpo4 = pd.DataFrame(list2).T
    
    for i in range(1,len(test_list2)):
        xx = dtpo3.values[i][0].split()
        
        for j in range(len(xx)):
            dtpo4.loc[i, j] = xx[j]  
            
    vlans_in_switch = []
    for i in list(dtpo4[0].values):
        try:
            if int(i)>1 and int(i)<1002:
                vlans_in_switch.append(i)
            elif int(i)>1005 and int(i)<=4096:
                vlans_in_switch.append(i)
        except:
            continue
    vlans_in_switch = [int(x) for x in vlans_in_switch]
    vlans_in_switch.sort()
     
    if vlans_in_switch==vlans_total:
        res_check_priority_dict = {'timestamp' : formatted_time,
                'switch name' : switch,
                'discrepancy': 'no',
                'missing_vlans' : [x for x in vlans_in_switch if x not in vlans_total],
                'priority': vlans_priority_dict,
                'remarks': ''
                }
    else:
        res_check_priority_dict = {'timestamp' : formatted_time,
                'switch name' : switch,
                'discrepancy': 'yes',
                'missing_vlans' : [x for x in vlans_in_switch if x not in vlans_total],
                'priority': vlans_priority_dict,
                'remarks': 'config changes required'
                }
    res_check_priority_list.append(res_check_priority_dict)
    
    print(res_check_priority_list)

if __name__=='__main__':
    #return ['timestamp', 'switch name', 'discrepancy', 'missing_vlans', 'priority', 'remarks']
    current_time = time.time()
    formatted_time = datetime.fromtimestamp(current_time).strftime("%m-%d-%Y %H:%M:%S") 
    res_check_priority_list = []

    #switch = "**************"
    #switch = "**************"
    switch = '**************'
    try:
        kwargs = {
            'device_type': 'cisco_nxos','ip': switch,'username': '**************','password': '**************','port':'22'
            }
        connection = ConnectHandler(**kwargs)
    except:
        kwargs = {
            'device_type': 'cisco_ios_telnet','ip': switch,'username': '**************','password': '**************','port':'23'
            }
        connection = ConnectHandler(**kwargs)

