from netmiko import ConnectHandler
import pandas as pd
import csv
import time
from datetime import datetime

#return ['timestamp', 'switch name', 'interface name', 'status']
current_time = time.time()
formatted_time = datetime.fromtimestamp(current_time).strftime("%m-%d-%Y %H:%M:%S") 


#switch = "sg211-cr1-cs4-famn"
#switch = "sg624-afmr0-cs1-cn"
#switch = "sg624-frm4-as26-mn240"
switch= "sg209-b1rm5x-as6-cn240"

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
test_string2 = connection.send_command("show int | i CRC|output errors|line|Keepalive")
test_list1 = test_string1.splitlines()
test_list = test_string2.splitlines()
test_list2 = [x for x in test_list if 'line' in x or 'Keepalive' in x ]
#test_list3 = [x for x in test_list1 if 'trunk' in x]
      
dtpo = pd.DataFrame(test_list1)
list1 = dtpo.values[0][0].split()
dtpo1 = pd.DataFrame(list1).T
for i in range(1,len(test_list1)):
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

dict_int_info = {}

for i in range(len(dtpo1)):
    p = list(map(lambda x: x.replace('Gi', 'GigabitEthernet') if 'Gi' in x \
                     else x.replace('Fa', 'FastEthernet') \
                  if 'Fa' in x else x.replace('Te', 'TenGigabitEthernet') \
                      if 'Te' in x else x.replace('Fo', 'FortyGigabitEthernet') \
                          if 'Fo' in x else 'anomaly', [dtpo1.iloc[i,0]]))[0]
    q = list(dtpo1.iloc[i].values)
    
    if p == 'anomaly':
        continue
    else:
        dict_int_info.setdefault(p, [])
        if 'notconnect' in q and 'trunk' in q:
            dict_int_info.setdefault(p).append('notconnect')
            dict_int_info.setdefault(p).append('trunk')
        elif 'notconnect' in q and 'trunk' not in q:
            dict_int_info.setdefault(p).append('notconnect')
            dict_int_info.setdefault(p).append('access')
        elif 'connected' in q and 'trunk' in q:
            dict_int_info.setdefault(p).append('connected')
            dict_int_info.setdefault(p).append('trunk')
        elif 'connected' in q and 'trunk' not in q:
            dict_int_info.setdefault(p).append('connected')
            dict_int_info.setdefault(p).append('access')
        elif 'disabled' in q and 'routed' in q:
            dict_int_info.setdefault(p).append('disabled')
            dict_int_info.setdefault(p).append('routed')
        elif 'disabled' in q and 'trunk' not in q and 'routed' not in q:
            dict_int_info.setdefault(p).append('disabled')
            dict_int_info.setdefault(p).append('access')
        elif 'err-disabled' in q:
            dict_int_info.setdefault(p).append('err-disabled')
        else: pass
      
for i in range(len(dtpo3)):
    x = list(dtpo3.iloc[i].values)[0]
    if 'Ether' in x:
        dict_int_info.setdefault(x, [])
        isit = list(dtpo3.iloc[i+1].values)
        if 'Keepalive' in isit and 'set' in isit and 'not' not in isit:
            dict_int_info.setdefault(x).append('set')
        elif 'Keepalive' in isit and 'not' in isit and 'set' in isit:
            dict_int_info.setdefault(x).append('not-set')
        else: dict_int_info.setdefault(x).append('not-set')
    else: continue

res_check_keepalive_list=[]
for m,n in dict_int_info.items():
    if 'access' in n and 'set' in n:
        res_check_keepalive_list.append({'timestamp' : formatted_time,
                'switch name' : switch,
                'interface name': m,
                'status': 'correct'
                })
    elif 'access' in n and 'not-set' in n and 'notconnect' in n:
        res_check_keepalive_list.append({'timestamp' : formatted_time,
                'switch name' : switch,
                'interface name': m,
                'status': 'warning'
                })
    elif 'trunk' in n and 'not-set' in n:
        res_check_keepalive_list.append({'timestamp' : formatted_time,
                'switch name' : switch,
                'interface name': m,
                'status': 'correct'
                })
    elif 'trunk' in n and 'set' in n and 'notconnect' in n:
        res_check_keepalive_list.append({'timestamp' : formatted_time,
                'switch name' : switch,
                'interface name': m,
                'status': 'warning'
                })
    elif '1/1/' in m and 'not-set' in n and 'connected' in n:
        res_check_keepalive_list.append({'timestamp' : formatted_time,
                'switch name' : switch,
                'interface name': m,
                'status': 'correct'
                })
    else:
        res_check_keepalive_list.append({'timestamp' : formatted_time,
                'switch name' : switch,
                'interface name': m,
                'status': 'not correct'
                })
        
print(res_check_keepalive_list)        
    

    
         
     
            
            
            
        
    


    
    
