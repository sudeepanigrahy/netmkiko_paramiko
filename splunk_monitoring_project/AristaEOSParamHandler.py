import re
import time
from datetime import datetime
import pandas as pd

def check_uptime(i_string, i_hostname):
    #return [{'timestamp', 'switch name', 'uptime'}]
    #once this function is called, it'll return the above dict inside a list, to the caller.
    
    current_time = time.time()
    formatted_time = datetime.fromtimestamp(current_time).strftime("%m-%d-%Y %H:%M:%S") 
    res_list = []
    
    list_version = i_string.splitlines()
    uptime_line = []
    for line in list_version:
        if 'Uptime' in line:
            uptime_line.append(line)    
            
    uptime_line_elements = uptime_line[0].split()
    x = {"years":"0","weeks":"0", "days":"0", "hours":"0", "minutes":"0"}   
        
    for i in range(2, len(uptime_line_elements) + 1):
        
        if uptime_line_elements[i-1] == "year," or uptime_line_elements[i-1] == "years,":
            x["years"] = uptime_line_elements[i-2]
            continue
        elif uptime_line_elements[i-1] == "week," or uptime_line_elements[i-1] == "weeks,":
            x["weeks"] = uptime_line_elements[i-2]
            continue
        elif uptime_line_elements[i-1] == "day," or uptime_line_elements[i-1] == "days," or uptime_line_elements[i-1] == "day(s),":
            x["days"] = uptime_line_elements[i-2]
            continue
        elif uptime_line_elements[i-1] == "hour" or uptime_line_elements[i-1] == "hours" or uptime_line_elements[i-1] == "hour(s),":
            x["hours"] = uptime_line_elements[i-2]
            continue
        elif uptime_line_elements[i-1] == "minute" or uptime_line_elements[i-1] == "minutes" or uptime_line_elements[i-1] == "minute(s),":
            x["minutes"] = uptime_line_elements[i-2]
            continue	 	  
    
    w=(int(x["weeks"])*7)/365
    d=(int(x["days"])/365)
    h=(int(x["hours"])/(365*24))
    m=(int(x["minutes"])/(365*24*60))
    result=int(x["years"])+w+d+h+m
    up_time = "%0.3f"%result
    
    res_dict = {
        'timestamp': formatted_time,
        'switch name': i_hostname,
        'uptime': up_time
        }
    res_list.append(res_dict) 

    return res_list


def check_snmp_config(i_string, i_hostname): 
    #return [{'timestamp', 'switch name', 'discrepancy', 'remarks'}]
    #once this function is called, it'll return the above dict inside a list, to the caller.
    
    
    current_time = time.time()
    formatted_time = datetime.fromtimestamp(current_time).strftime("%m-%d-%Y %H:%M:%S")        
    res_list = []
    
    if "xxxxx" in i_hostname:
        ip1 = "**********"
        ip2 = "**********"
        if "**********" in i_string and "**********" in i_string and ip1 in i_string and ip2 in i_string:
            discrepancy = "no"
            remark = ""
        else:
            discrepancy = "yes"
            remark = "SNMP server missing"
    elif "sg624" in i_hostname:
        ip1 = "**********"
        ip2 = "**********"
        if "**********" in i_string and "**********" in i_string and ip1 in i_string and ip2 in i_string:
            discrepancy = "no"
            remark = ""
        else:
            discrepancy = "yes"
            remark = "SNMP server missing"
    elif "sg211" in i_hostname:
        ip1 = "**********"
        ip2 = "**********"
        if "**********" in i_string and "**********" in i_string and ip1 in i_string and ip2 in i_string:
            discrepancy = "no"
            remark = ""
        else:
            discrepancy = "yes"
            remark = "SNMP server missing"
    else:
        pass
    
    res_dict = {
        'timestamp': formatted_time,
        'switch name': i_hostname,
        'discrepancy': discrepancy,
        'remarks': remark
        }
    res_list.append(res_dict)
            
    return res_list

def check_bpdu(i_string1, i_string2, i_hostname):
    #['timestamp','switch name', 'interface name', 'configuration', 'remarks']
    current_time = time.time()
    formatted_time = datetime.fromtimestamp(current_time).strftime("%m-%d-%Y %H:%M:%S") 

    test_list1 = i_string1.splitlines()
    test_list2 = i_string2.splitlines()

    test_list3= []
    for i in test_list2:
        if 'Ethernet' in i or 'bpdu' in i:
            test_list3.append(i)
            
    dtpo = pd.DataFrame(test_list1)
    list1 = dtpo.values[0][0].split()
    dtpo1 = pd.DataFrame(list1).T
    
    for i in range(1,len(test_list1)):
        xx = dtpo.values[i][0].split()
        
        for j in range(len(xx)):
            dtpo1.loc[i, j] = xx[j]

            
    dtpo2 = pd.DataFrame(test_list3)
    list2 = dtpo2.values[0][0].split()
    dtpo3 = pd.DataFrame(list2).T

    for i in range(1,len(test_list3)):
        xx = dtpo2.values[i][0].split()
        
        for j in range(len(xx)):
            dtpo3.loc[i, j] = xx[j]

    list4 = []
    for i in range(0, len(dtpo1)):
        list3 = list(dtpo1.iloc[i].values)
        if 'trunk' in list3 or 'routed' in list3 or 'MLAG' in list3:
            continue
        else:
            for j in range(0, len(list3)):            
                if 'Gi' in str(dtpo1.iloc[i][j]):
                    dtpo1.iloc[i][j] = str(dtpo1.iloc[i][j]).replace("Gi", "GigabitEthernet")
                    list4.append(dtpo1.iloc[i][j]) 
                elif 'Fa' in str(dtpo1.iloc[i][j]):
                    dtpo1.iloc[i][j] = str(dtpo1.iloc[i][j]).replace("Fa", "FastEthernet")
                    list4.append(dtpo1.iloc[i][j])
                elif 'Te' in str(dtpo1.iloc[i][j]):
                    dtpo1.iloc[i][j] = str(dtpo1.iloc[i][j]).replace("Te", "TenGigabitEthernet")
                    list4.append(dtpo1.iloc[i][j])   
                elif 'Eth' in str(dtpo1.iloc[i][j]):
                    dtpo1.iloc[i][j] = str(dtpo1.iloc[i][j]).replace("Eth", "Ethernet")
                    list4.append(dtpo1.iloc[i][j])
                elif 'Et' in str(dtpo1.iloc[i][j]):
                    dtpo1.iloc[i][j] = str(dtpo1.iloc[i][j]).replace("Et", "Ethernet")
                    list4.append(dtpo1.iloc[i][j])
                    

    res_list = []
    for i in list4:
        for j in range(0, len(dtpo3)):
            if i in list(dtpo3.iloc[j].values):
                if j == len(dtpo3)-1:
                    res_list.append({'timestamp': formatted_time,
                                  'switch name': i_hostname, 
                                  'interface name': i, 
                                  'configuration': 'no', 
                                  'remarks': 'bpdu configuration missing'
                                  })
                    break
                    
                elif 'bpduguard' in list(dtpo3.iloc[j+1].values):
                    res_list.append({'timestamp': formatted_time,
                                  'switch name': i_hostname, 
                                  'interface name': i, 
                                  'configuration': 'yes', 
                                  'remarks': ''
                                  })
                    break
                elif 'bpduguard' not in list(dtpo3.iloc[j+1].values):
                    res_list.append({'timestamp': formatted_time,
                                  'switch name': i_hostname, 
                                  'interface name': i, 
                                  'configuration': 'no', 
                                  'remarks': 'bpdu configuration missing'
                                  })
            else: continue

    return res_list

def check_vlan2(i_string1, i_string2, i_hostname):
    #return ['timestamp', 'switch name', 'discrepancy', 'vlans', 'trunked_vlans', 'remarks']
    current_time = time.time()
    formatted_time = datetime.fromtimestamp(current_time).strftime("%m-%d-%Y %H:%M:%S") 

    test_list1 = i_string1.splitlines()
    test_list2 = i_string2.splitlines()

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
                'switch name' : i_hostname,
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
                        'switch name' : i_hostname,
                        'discrepancy': 'no',
                        'vlans' : vlans,
                        'trunked_vlans': f"{p}: {vlanss}",
                        'remarks': ''
                        })
            elif 'All' in vlanss:
                res_check_vlan2.append({'timestamp' : formatted_time,
                        'switch name' : i_hostname,
                        'discrepancy': 'no',
                        'vlans' : vlans,
                        'trunked_vlans': f"{p}: {vlanss}",
                        'remarks': ''
                        })            
            else:
                res_check_vlan2.append({'timestamp' : formatted_time,
                        'switch name' : i_hostname,
                        'discrepancy': 'yes',
                        'vlans' : vlans,
                        'trunked_vlans': f"{p}: {vlanss}",
                        'remarks': 'vlan/s missing from this trunk'
                        })
                
    return res_check_vlan2
