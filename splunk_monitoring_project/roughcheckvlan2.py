from netmiko import ConnectHandler
import pandas as pd
import csv
import time
from datetime import datetime

#return ['timestamp', 'switch name', 'discrepancy', 'vlans', 'trunked_vlans', 'remarks']
current_time = time.time()
formatted_time = datetime.fromtimestamp(current_time).strftime("%m-%d-%Y %H:%M:%S") 


switch = "***********"

kwargs = {
    'device_type': 'arista_eos','ip': switch,'username': '***********','password': '***********','port':'22'
    }
connection = ConnectHandler(**kwargs)

test_string1 = connection.send_command("sh vlan br")
test_string2 = connection.send_command("show int trunk")
test_list1 = test_string1.splitlines()
test_list2 = test_string2.splitlines()

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
        
vlans = []
for i in list(dtpo1[0].values):
    try:
        if int(i)>1 and int(i)<1002:
            vlans.append(i)
        elif int(i)>1005 and int(i)<=4096:
            vlans.append(i)
    except:
        continue
vlans = [int(x) for x in vlans]
vlans.sort()

trunked_vlans = {}

for i in range(len(list(dtpo3[0].values))):
    p = list(dtpo3.iloc[i].values)
    if 'Port' in p and 'Vlans' in p and 'allowed' in p and 'management' not in p:
        for j in range(i+1, len(list(dtpo3[0].values))):
            m = dtpo3.iloc[j,0]
            if 'Port' in m:
                break
            elif 'Et' in m or 'Gi' in m or 'Te' in m or 'Twe' in m:
                trunked_vlans.setdefault(m, [])
                trunked_vlans.setdefault(m).append(dtpo3.iloc[j,1])
                for k in range(j+1, len(list(dtpo3[0].values))):
                    if 'Et' in dtpo3.iloc[k,0]:
                        break
                    elif 'Po' in dtpo3.iloc[k,0]:
                        break
                    else:
                        trunked_vlans.setdefault(m).append(dtpo3.iloc[k,0])
                
                if 'None' in trunked_vlans.setdefault(m):
                    trunked_vlans.setdefault(m).remove('None')
                    
            else: continue
    else: continue

"""
for i in range(len(list(dtpo3[0].values))):
    if dtpo3.iloc[i,0] == 'Port':
        if i == 0:
            continue
        elif i != 0:
            for j in range(i+1, len(list(dtpo3[0].values))):
                if dtpo3.iloc[j,0] != 'Port':
                    trunked_vlans[dtpo3.iloc[j,0]] = dtpo3.iloc[j,1]
                else: break
            break
    else: continue
"""
res_check_vlan2=[]
for p,q in trunked_vlans.items():    
    vlanss = []
    for z in q:
        if "-" in z and "," in z:
            l = z.split(",")
            v=[]
            dash=[]
            for i in l:
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
                else: continue
            [l.append(x) for x in v]
            [l.remove(x) for x in dash] 
            vlanss.extend(l)
            #vlanss = [x for x in vlans if x in l]
            #vlanss.sort()
        elif "," in z and '-' not in z:
            l = z.split(",")
            vlanss.extend(l)
            #vlanss = [x for x in vlans if x in l]
            #vlanss.sort()
        elif "-" in z and "," not in z:
            l = z.split("-")
            ll = [x for x in range(int(l[0]),int(l[-1])+1)]
            vlanss.extend(ll)
        elif "," not in z and "-" not in z:
            l = []
            l.append(z)
            vlanss.extend(l)
            
    vlanss = [int(x) for x in vlanss]
    vlanss.sort()
    
    if vlanss==vlans:
        res_check_vlan2.append({'timestamp' : formatted_time,
                'switch name' : switch,
                'discrepancy': 'no',
                'vlans' : vlans,
                'trunked_vlans': f"{p}: {vlanss}",
                'remarks': ''
                })
    else:
        res_check_vlan2.append({'timestamp' : formatted_time,
                'switch name' : switch,
                'discrepancy': 'yes',
                'vlans' : vlans,
                'trunked_vlans': f"{p}: {vlanss}",
                'remarks': 'vlan/s missing from this trunk'
                })

        
print(res_check_vlan2)            


#print(dtpo1, 5*'\n', dtpo3[0].values)
#print(vlans, 5*'\n', trunked_vlans)
#dtpo3.to_csv('dtpo3.csv')
"""
res_check_vlan2 = []
for p,q in trunked_vlans.items():
    if "-" in q and "," not in q:
        l = q.split("-")
        vlanss = [x for x in vlans if int(x) in range(int(l[0]),int(l[-1])+1)]
        vlanss.sort()
        if vlanss==vlans:
            res_check_vlan2.append({'timestamp' : formatted_time,
                    'switch name' : switch,
                    'discrepancy': 'no',
                    'vlans' : vlans,
                    'trunked_vlans': f"{p}: {q}",
                    'remarks': ''
                    })
        else:
            res_check_vlan2.append({'timestamp' : formatted_time,
                    'switch name' : switch,
                    'discrepancy': 'yes',
                    'vlans' : vlans,
                    'trunked_vlans': f"{p}: {q}",
                    'remarks': ''
                    })
            
    elif "-" in q and "," in q:
        l = q.split(",")
        v=[]
        dash=[]
        for i in l:
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
            else: continue
        [l.append(x) for x in v]
        [l.remove(x) for x in dash] 
        vlanss = [x for x in vlans if x in l]
        vlanss.sort()
        if vlanss==vlans:
            res_check_vlan2.append({'timestamp' : formatted_time,
                    'switch name' : switch,
                    'discrepancy': 'no',
                    'vlans' : vlans,
                    'trunked_vlans': f"{p}: {q}",
                    'remarks': ''
                    })
        else:
            res_check_vlan2.append({'timestamp' : formatted_time,
                    'switch name' : switch,
                    'discrepancy': 'yes',
                    'vlans' : vlans,
                    'trunked_vlans': f"{p}: {q}",
                    'remarks': ''
                    })
            
    elif "," not in q and "-" not in q:
        l = []
        l.append(q)
        vlanss = [x for x in vlans if x in l]
        if vlanss==vlans:
            res_check_vlan2.append({'timestamp' : formatted_time,
                    'switch name' : switch,
                    'discrepancy': 'no',
                    'vlans' : vlans,
                    'trunked_vlans': f"{p}: {q}",
                    'remarks': ''
                    })
        else:
            res_check_vlan2.append({'timestamp' : formatted_time,
                    'switch name' : switch,
                    'discrepancy': 'yes',
                    'vlans' : vlans,
                    'trunked_vlans': f"{p}: {q}",
                    'remarks': ''
                    })
    elif "," in q:
        l = q.split(",")
        vlanss = [x for x in vlans if x in l]
        vlanss.sort()
        if vlanss==vlans:
            res_check_vlan2.append({'timestamp' : formatted_time,
                    'switch name' : switch,
                    'discrepancy': 'no',
                    'vlans' : vlans,
                    'trunked_vlans': f"{p}: {q}",
                    'remarks': ''
                    })
        else:
            res_check_vlan2.append({'timestamp' : formatted_time,
                    'switch name' : switch,
                    'discrepancy': 'yes',
                    'vlans' : vlans,
                    'trunked_vlans': f"{p}: {q}",
                    'remarks': ''
                    })
            
            
print(res_check_vlan2)

"""
