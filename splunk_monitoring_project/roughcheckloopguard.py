from netmiko import ConnectHandler
import pandas as pd
import csv
import time
from datetime import datetime

#return ['timestamp', 'switch name', 'interface name', 'configuration']
current_time = time.time()
formatted_time = datetime.fromtimestamp(current_time).strftime("%m-%d-%Y %H:%M:%S") 


#switch = "sg211-cr1-cs4-famn"
#switch= "sg209-b1rm5x-as6-cn240"
#switch = "sg624-atdr301-ds1-pn"
switch = "sg624-frt7-as12-mn236"
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

test_string1 = connection.send_command("Show interface status")
test_string2 = connection.send_command("show cdp neigh")
test_string3 = connection.send_command("Show run")
test_list1 = test_string1.splitlines()
test_list2 = test_string2.splitlines()
test_list3 = test_string3.splitlines()
test_list4 = [x for x in test_list1 if 'trunk' in x]
test_list5 = [x for x in test_list3 if 'Ethernet' in x or 'guard loop' \
              in x or 'GigE' in x]
test_list6 = [x for x in test_list1 if 'routed' in x]
test_list7 = list(map(lambda x: x.split()[0].replace('Gi', 'Gig') \
                                  if 'Gi' in x else x.split()[0].replace('Te', 'Ten') \
                                           if 'Te' in x else x.split()[0], test_list6))
    
dtpo = pd.DataFrame(test_list4)
list1 = dtpo.values[0][0].split()
dtpo1 = pd.DataFrame(list1).T
for i in range(1,len(test_list4)):
    xx = dtpo.values[i][0].split()    
    for j in range(len(xx)):
        dtpo1.loc[i, j] = xx[j]
       
dtpo2 = pd.DataFrame(test_list2)
list2 = dtpo2.values[0][0].split()
dtpo3 = pd.DataFrame(list2).T
for i in range(1,len(test_list2)):
    xx = dtpo2.values[i][0].split()    
    for j in range(len(xx)):
        dtpo3.loc[i, j] = xx[j] 
        
dtpo4 = pd.DataFrame(test_list5)
list3 = dtpo4.values[0][0].split()
dtpo5 = pd.DataFrame(list3).T
for i in range(1,len(test_list5)):
    xx = dtpo4.values[i][0].split()    
    for j in range(len(xx)):
        dtpo5.loc[i, j] = xx[j] 

uplinks_trunk_list=[]
if 'as' in switch or 'AS' in switch:
    for i in range(len(dtpo3)):
        p = dtpo3.iloc[i,0]
        if 'ds' in p or 'ds1' in p or 'ds2' in p or 'ds3' in p\
            or 'DS' in p or 'ds4' in p or 'ds5' in p or 'ds6' in p\
                or 'ds7' in p or 'ds8' in p or 'cs' in p:
                    uplinks_trunk_list.append(str(dtpo3.iloc[i+1,0]) \
                                              + str(dtpo3.iloc[i+1,1]))
        else: pass
elif 'ds' in switch or 'DS' in switch:
    for i in range(len(dtpo3)):
        p = dtpo3.iloc[i,0]
        if 'cs' in p or 'cs1' in p or 'cs2' in p or 'cs3' in p\
            or 'CS' in p or 'cs4' in p or 'cs5' in p or 'cs6' in p:
                uplinks_trunk_list.append(str(dtpo3.iloc[i+1,0]) \
                                          + str(dtpo3.iloc[i+1,1]))                  
        else: pass
    
uplinks_trunk_list2=[]
for i in uplinks_trunk_list:
    if i in test_list7:
        uplinks_trunk_list.remove(i)
        for i in range(len(dtpo3)):
            p = dtpo3.iloc[i,0]
            if 'ds' in p or 'ds1' in p or 'ds2' in p or 'ds3' in p\
                or 'DS' in p or 'ds4' in p or 'ds5' in p or 'ds6' in p\
                    or 'ds7' in p or 'ds8' in p:
                        uplinks_trunk_list2.append(str(dtpo3.iloc[i+1,0]) +\
                                                  str(dtpo3.iloc[i+1,1]))
    else: pass
uplinks_trunk_list.extend(uplinks_trunk_list2)

trunks_list=[]                
for i in range(len(dtpo1)):
    trunks_list.append(dtpo1.iloc[i,0])
    
enlarge=[]    
z = [uplinks_trunk_list, trunks_list]   
for p,q in enumerate(z):   
    q = list(map(lambda x: x.replace('Gig', 'GigabitEthernet') if 'Gig' \
                                  in x else x.replace('Gi', 'GigabitEthernet') \
                                      if 'Gi' in x else x.replace('Ten', 'TenGigabitEthernet') \
                                          if 'Ten' in x else x.replace('Te', 'TenGigabitEthernet') \
                                              if 'Te' in x else x.replace('Eth', 'Ethernet') \
                                                  if 'Eth' in x else x.replace('Twe', 'TwentyFiveGigE')\
                                                      if 'Twe' in x else 'anomaly', q))
    enlarge.append(q)
uplinks_trunk_list = enlarge[0]
trunks_list = enlarge[1]        

loop_guard_ints=[]   
for i in range(len(dtpo5)):
    if i == int(len(dtpo5)-1) and 'Ether' in dtpo5.iloc[i,1]:
        break
    elif i == int(len(dtpo5)-1) and 'GigE' in dtpo5.iloc[i,1]:
        break
    elif 'Ether' in dtpo5.iloc[i,1] and 'guard' in dtpo5.iloc[i+1,1]:
        loop_guard_ints.append(dtpo5.iloc[i,1])
    elif 'GigE' in dtpo5.iloc[i,1] and 'guard' in dtpo5.iloc[i+1,1]:
        loop_guard_ints.append(dtpo5.iloc[i,1])

res_check_loopguard_list=[]
for i in uplinks_trunk_list:
    if i in trunks_list and i in loop_guard_ints:
        res_check_loopguard_list.append({'timestamp' : formatted_time,
                'switch name' : switch,
                'interface name': i,
                'configuration': 'yes'
                })
    elif i in trunks_list and i not in loop_guard_ints:
        res_check_loopguard_list.append({'timestamp' : formatted_time,
                'switch name' : switch,
                'interface name': i,
                'configuration': 'no'
                })
    else: res_check_loopguard_list.append({'timestamp' : formatted_time,
            'switch name' : switch,
            'interface name': i,
            'configuration': 'warning'
            })
    
print(res_check_loopguard_list)
