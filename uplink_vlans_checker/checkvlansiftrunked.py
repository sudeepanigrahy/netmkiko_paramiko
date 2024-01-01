from netmiko import ConnectHandler
import pandas as pd
import csv
import time
from datetime import datetime

def vlansiftrunked(string1, string2, switch):
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
            if int(i)>0 and int(i)<1002:
                vlans.append(i)
            elif int(i)>1005 and int(i)<=4096:
                vlans.append(i)
        except:
            continue
    vlans.sort()
    trunked_vlans = {}
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
    
    #print(trunked_vlans)
    res_check_vlan2 = []
    for p,q in trunked_vlans.items():
        if "-" in q and "," not in q:
            l = q.split("-")
            vlanss = [x for x in vlans if int(x) in range(int(l[0]),int(l[-1])+1)]
            vlanss.sort()
            if vlanss==vlans:
                res_check_vlan2.append({'switch name' : switch,
                        'discrepancy': 'no',
                        'vlans' : vlans,
                        'trunked_vlans': f"{p}: {q}",
                        'remarks': ''
                        })
            else:
                res_check_vlan2.append({'switch name' : switch,
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
                res_check_vlan2.append({'switch name' : switch,
                        'discrepancy': 'no',
                        'vlans' : vlans,
                        'trunked_vlans': f"{p}: {q}",
                        'remarks': ''
                        })
            else:
                res_check_vlan2.append({'switch name' : switch,
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
                res_check_vlan2.append({'switch name' : switch,
                        'discrepancy': 'no',
                        'vlans' : vlans,
                        'trunked_vlans': f"{p}: {q}",
                        'remarks': ''
                        })
            else:
                res_check_vlan2.append({'switch name' : switch,
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
                res_check_vlan2.append({'switch name' : switch,
                        'discrepancy': 'no',
                        'vlans' : vlans,
                        'trunked_vlans': f"{p}: {q}",
                        'remarks': ''
                        })
            else:
                res_check_vlan2.append({'switch name' : switch,
                        'discrepancy': 'yes',
                        'vlans' : vlans,
                        'trunked_vlans': f"{p}: {q}",
                        'remarks': ''
                        })
                
    #print(res_check_vlan2)            
    return res_check_vlan2

if __name__=='__main__':
    #return ['timestamp', 'switch name', 'discrepancy', 'vlans', 'trunked_vlans', 'remarks']
    current_time = time.time()
    formatted_time = datetime.fromtimestamp(current_time).strftime("%m-%d-%Y %H:%M:%S") 


    #switch = "sg209-b1rm5x-as6-cn240"
    #switch = "sg209-b1mr4d-as1-ah-mn-vpc"
    #switch = "sg211-frm3-as2-famn301"
    switch = "sg624-frm2-ds3-mn"

    kwargs = {
        'device_type': 'cisco_nxos','ip': switch,'username': 'spanigrahy','password': 'Sueme@0125','port':'22'
        }
    connection = ConnectHandler(**kwargs)
