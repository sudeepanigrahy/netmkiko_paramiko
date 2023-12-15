from netmiko import ConnectHandler
import pandas as pd
import csv
import time
from datetime import datetime

   
def vlansrootport(string1, string2, switch):
    test_string1 = string1
    test_string2 = string2
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
        if "as" in switch or "AS" in switch:
            if "ds" in dtpo1.iloc[i, 0] or "DS" in dtpo1.iloc[i, 0] or "cs" in dtpo1.iloc[i, 0] or "CS" in dtpo1.iloc[i, 0]:
                #print('yes')
                uplinks[dtpo1.iloc[i,0]] = dtpo1.iloc[i+1,0] + dtpo1.iloc[i+1,1]
        elif "ds" in switch or "DS" in switch:
            if "cs" in dtpo1.iloc[i, 0] or "CS" in dtpo1.iloc[i, 0]:
                #print('yes')
                uplinks[dtpo1.iloc[i,0]] = dtpo1.iloc[i+1,0] + dtpo1.iloc[i+1,1]
        else: pass    
    
    #print("uplinks, line 36:\n", uplinks)        
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
    
    #print("vlan_dict, line 58:\n", vlan_dict)
    #print("mac_dict, line 58:\n", mac_dict)
    
    #---------------------------------------------------------------------
    
    root_port = []
    primary = ''
    secondary = ''
    secondary_root_port = []
    for i, j in uplinks.items():
        if "ds1" in i or "ds3" in i or "ds5" in i or "DS1" in i or "DS3" in i or "DS5" in i:
            root_port.append(j)
            primary = i
        elif "cs1" in i or "cs3" in i or "cs5" in i or "CS1" in i or "CS3" in i or "CS5" in i:
            root_port.append(j)
            primary = i    
        elif "ds2" in i or "ds4" in i or "ds6" in i or "DS2" in i or "DS4" in i or "DS6" in i:
            secondary_root_port.append(j)
            secondary = i
        elif "cs2" in i or "cs4" in i or "cs6" in i or "CS2" in i or "CS4" in i or "CS6" in i:
            secondary_root_port.append(j)
            secondary = i
        else: pass

    #print("root_port, line 82:\n", root_port)    
        
    root_port = list(map(lambda x: x.replace('Ten', 'Te') if 'Ten' in x else x.replace('Gig', 'Gi') if 'Gig' in x else 'anomaly', root_port))
    secondary_root_port = list(map(lambda x: x.replace('Ten', 'Te') if 'Ten' in x else x.replace('Gig', 'Gi') if 'Gig' in x else 'anomaly', secondary_root_port))
    
    #print("root_port, line 87:\n", root_port)
    
    """
    if 'Te' in root_port:
        #print(root_port)
        root_port = root_port.replace("Ten", "Te")
    elif 'Gi' in root_port:
        root_port = root_port.replace("Gig", "Gi")
    """
    #print("vlan_dict, line 96:\n", vlan_dict )
    
    checker_list=[]
    faulty_vlans=[]
    for i,j in vlan_dict.items():
        if j == root_port[0]:
            checker_list.append('no')
        else:
            checker_list.append('yes')
            faulty_vlans.append(i)
            
    checker_listt = list(set(checker_list))
    
    #print("checker_list, line 103:\n", checker_list)
    #print("checker_listt, line 104:\n", checker_listt)
    #print("faulty_vlans, line 111:\n", faulty_vlans)
    
    if 'no' in checker_listt and 'yes' not in checker_listt:
        return ['yes', root_port, secondary_root_port, primary, secondary]
    elif 'no' in checker_listt and 'yes' in checker_listt:
        return [{'no': faulty_vlans} , root_port, secondary_root_port, primary, secondary]
    elif 'yes' in checker_listt and 'no' not in checker_listt:
        return [{'no': faulty_vlans}, root_port, secondary_root_port, primary, secondary]    
  


if __name__=='__main__':
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