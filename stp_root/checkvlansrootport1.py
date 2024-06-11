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
    remarks = ''
    #print(dtpo, '\n', dtpo1)
    counter = 0
    for j in list(dtpo1[0]):
        if "-ds" in j or "-DS" in j or '-cr' in j.split(".")[0] or '-CR' in j.split(".")[0] or '-er' in j or '-ER' in j or '-mf' in j or '-MF' in j or '-sr' in j or '-SR' in j:
            counter = counter + 1
        elif "cs" in j or "CS" in j:
            counter = counter + 100
            
    #print(counter)
    
    if counter == 0:
        remarks = "No DS/CS/CR/ER/MF/SR connected with this AS"
    else:
        for i in range(0,dtpo1[0].size):        
            if "as" in switch or "AS" in switch:
                if "-ds" in dtpo1.iloc[i, 0] or "-DS" in dtpo1.iloc[i, 0] or '-cr' in dtpo1.iloc[i, 0].split(".")[0] or '-CR' in dtpo1.iloc[i, 0].split(".")[0] or '-er' in dtpo1.iloc[i, 0] or '-ER' in dtpo1.iloc[i, 0] or '-mf' in dtpo1.iloc[i, 0] or '-MF' in dtpo1.iloc[i, 0] or '-sr' in dtpo1.iloc[i, 0] or '-SR' in dtpo1.iloc[i, 0]:
                    #print('yes')
                    uplinks[dtpo1.iloc[i,0]] = dtpo1.iloc[i+1,0] + dtpo1.iloc[i+1,1]
                elif "cs" in dtpo1.iloc[i, 0] or "CS" in dtpo1.iloc[i, 0]:
                    remarks = 'CS connected to this AS'
            elif "ds" in switch or "DS" in switch:
                if "cs" in dtpo1.iloc[i, 0] or "CS" in dtpo1.iloc[i, 0]:
                    #print('yes')
                    uplinks[dtpo1.iloc[i,0]] = dtpo1.iloc[i+1,0] + dtpo1.iloc[i+1,1]
            else: pass
        
    #print("UPLINKS:", uplinks)        
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
        if "VLAN" in dtpo3[0].values[i]:
            vlan_dict[dtpo3[0].values[i]] = dtpo3.iloc[i, 7]
            mac_dict[dtpo3[0].values[i]] = dtpo3.iloc[i, 2]
        else: pass
    
    #print(dtpo2, dtpo3)
    #print(vlan_dict)
    #---------------------------------------------------------------------
    
    root_port = []
    primary = ''
    secondary = ''
    secondary_root_port = []

    if len(uplinks) == 1:
        for i,j in uplinks.items():
            root_port.append(j)
            primary = i
            remarks = "Only one DS/CS/CR/ER/MF/SR connected with this AS"
            
    elif len(uplinks) == 2:        
        for i,j in uplinks.items():
            cut = i.split(".")
            cuts = cut[0].split('-')
            n = ''
            for c in cuts:
                if 'ds' in c:
                    n = c.split('s')[-1]
                    break
                elif 'cr' in c:
                    n = c.split('r')[-1]
                    break
                elif 'er' in c:
                    n = c.split('r')[-1]
                    break
                elif 'mf' in c:
                    n = c.split('f')[-1]
                    break
                elif 'sr' in c:
                    n = c.split('r')[-1]
                    break
                elif 'DS' in c:
                    n = c.split('S')[-1]
                    break
                elif 'CR' in c:
                    n = c.split('R')[-1]
                    break
                elif 'ER' in j:
                    n = c.split('R')[-1]
                    break
                elif 'MF' in j:
                    n = c.split('F')[-1]
                    break
                elif 'SR' in j:
                    n = c.split('R')[-1]
                    break
            n = int(n)
            
            if n%2 != 0:
                root_port.append(j)
                primary = i
            elif n%2 == 0:
                secondary_root_port.append(j)
                secondary = i
        
    #print("ROOT_PORT")
        
    root_port = list(map(lambda x: x.replace('Ten', 'Te') if 'Ten' in x else x.replace('Gig', 'Gi') if 'Gig' in x\
                         else x.replace('Twe', 'Twe') if 'Twe' in x else 'anomaly', root_port))
    secondary_root_port = list(map(lambda x: x.replace('Ten', 'Te') if 'Ten' in x else x.replace('Gig', 'Gi') if 'Gig' in x\
                                   else x.replace('Twe', 'Twe') if 'Twe' in x else 'anomaly', secondary_root_port))
    
    #print("ROOT_PORT::", root_port)
    checker_list=[]
    faulty_vlans=[]
    #print("COUNTERRRR:", counter)
    #print("VLAN_DICT::", vlan_dict)
    for i,j in vlan_dict.items():
        if counter == 0 or counter == 100 or counter == 200: break
        elif j == root_port[0]:
            checker_list.append('no')
        else:
            checker_list.append('yes')
            faulty_vlans.append(i)
            
    checker_listt = list(set(checker_list))
    #print("CHECKER_LISTT:", checker_list)
    
    if 'no' in checker_listt and 'yes' not in checker_listt:
        return ['yes', root_port, secondary_root_port, primary, secondary, remarks]
    elif 'no' in checker_listt and 'yes' in checker_listt:
        return [{'no': faulty_vlans} , root_port, secondary_root_port, primary, secondary, remarks]
    elif 'yes' in checker_listt and 'no' not in checker_listt:
        return [{'no': faulty_vlans}, root_port, secondary_root_port, primary, secondary, remarks]
    else: return ['', root_port, secondary_root_port, primary, secondary, remarks]     
  

if __name__=='__main__':
    
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