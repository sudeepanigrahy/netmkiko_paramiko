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
h = ['timestamp', 'switch name', 'discrepancy', 'vlans', 'trunked_vlans', 'remarks']

with open("output.csv", "w", newline='') as filetypeobject:
    header = h
    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
    dictwritertypeobject.writeheader()

def work(connection, switch):
    #return ['timestamp', 'switch name', 'discrepancy', 'vlans', 'trunked_vlans', 'remarks']
    current_time = time.time()
    formatted_time = datetime.fromtimestamp(current_time).strftime("%m-%d-%Y %H:%M:%S") 

    """
    switch = "sg624-xamr0-cpd14-leaf123b"
    #switch = "sg209-b1mr4d-as1-ah-mn-vpc"
    #switch = "sg211-frm3-as2-famn301"

    kwargs = {
        'device_type': 'arista_eos','ip': switch,'username': 'spanigrahy','password': 'Sueme@0125','port':'22'
        }
    connection = ConnectHandler(**kwargs)
        """

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

    res_check_vlan2=[]
    if len(trunked_vlans)==0:
        res_check_vlan2.append({'timestamp' : formatted_time,
                'switch name' : switch,
                'discrepancy': 'yes',
                'vlans' : vlans,
                'trunked_vlans': 'Possibly no trunk interfaces, or might be only trunk port-channel/s present',
                'remarks': ''
                })
    else:    
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
            if 'All' not in vlanss:    
                vlanss = [int(x) for x in vlanss]
                vlanss.sort()
            else: pass
            
            if vlanss==vlans:
                res_check_vlan2.append({'timestamp' : formatted_time,
                        'switch name' : switch,
                        'discrepancy': 'no',
                        'vlans' : vlans,
                        'trunked_vlans': f"{p}: {vlanss}",
                        'remarks': ''
                        })
            elif 'All' in vlanss:
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

        
    for i in res_check_vlan2:
        with open("output.csv", "a", newline='') as filetypeobject:
            header = h
            dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
            dictwritertypeobject.writerow({h[0]: i[h[0]] , h[1]: i[h[1]], h[2]: i[h[2]], h[3]:i[h[3]], h[4]: i[h[4]], h[5]: i[h[5]]})
            connection.disconnect()
    


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
            'device_type': 'arista_eos','ip': i,'username': 'spanigrahy','password': 'Sueme@0125','port':'22'
            }
        connection = ConnectHandler(**kwargs)
    except:
        try:
            kwargs = {
                'device_type': 'arista_eos_telnet','ip': i,'username': 'spanigrahy','password': 'Sueme@0125','port':'23'
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
