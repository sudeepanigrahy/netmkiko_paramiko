import re
import time
from datetime import datetime
import IOHandler
import csv
import pandas as pd

def check_snmp_config(i_string, i_hostname): 
    #return ['timestamp', 'switch name', 'discrepancy', 'remarks']
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
    elif "xxxxx" in i_hostname:
        ip1 = "**********"
        ip2 = "**********"
        if "**********" in i_string and "**********" in i_string and ip1 in i_string and ip2 in i_string:
            discrepancy = "no"
            remark = ""
        else:
            discrepancy = "yes"
            remark = "SNMP server missing"
    elif "xxxxx" in i_hostname:
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

def check_uptime(i_string, i_hostname):
    #return ['timestamp', 'switch name', 'uptime']
    #once this function is called, it'll return the above dict inside a list, to the caller.
    
    current_time = time.time()
    formatted_time = datetime.fromtimestamp(current_time).strftime("%m-%d-%Y %H:%M:%S") 
    res_list = []
    
    list_version = i_string.splitlines()
    uptime_line = []
    for line in list_version:
        if 'uptime' in line:
            uptime_line.append(line)    
    uptime_line_elements = uptime_line[0].split()
    x = {"years":"0","weeks":"0", "days":"0", "hours":"0", "minutes":"0"}   
        
    for i in range(4, len(uptime_line_elements) + 1):
        
        if uptime_line_elements[i-1] == "year," or uptime_line_elements[i-1] == "years,":
            x["years"] = uptime_line_elements[i-2]
            continue
        elif uptime_line_elements[i-1] == "week," or uptime_line_elements[i-1] == "weeks,":
            x["weeks"] = uptime_line_elements[i-2]
            continue
        elif uptime_line_elements[i-1] == "day," or uptime_line_elements[i-1] == "days," or uptime_line_elements[i-1] == "day(s),":
            x["days"] = uptime_line_elements[i-2]
            continue
        elif uptime_line_elements[i-1] == "hour," or uptime_line_elements[i-1] == "hours," or uptime_line_elements[i-1] == "hour(s),":
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
    up_time = "%0.6f"%result
    
    res_dict = {
        'timestamp': formatted_time,
        'switch name': i_hostname,
        'uptime': up_time
        }
    res_list.append(res_dict)

    return res_list
        
def check_vlan(i_string1, i_string2, i_hostname):
    #return ['timestamp', 'switch name', 'vlan', 'discrepancy', 'mac']
    #once this function is called, it'll return the above dict inside a list, to the caller.
    
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

    uplinks = {}
    for i in range(0,dtpo1[0].size):
        if "as" in i_hostname:
            if "ds" in dtpo1.iloc[i, 0]:
                uplinks[dtpo1.iloc[i,0]] = dtpo1.iloc[i+1,0] + dtpo1.iloc[i+1,1]
        elif "ds" in i_hostname:
            if "cs" in dtpo1.iloc[i, 0]:
                uplinks[dtpo1.iloc[i,0]] = dtpo1.iloc[i+1,0] + dtpo1.iloc[i+1,1]
        else: pass    

#----------------------------------------------------------------------------------------

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

#-----------------------------------------------------------------------------------------

    root_port = ''
    for i, j in uplinks.items():
        if "ds1" in i or "ds3" in i or "ds5" in i:
            root_port = j
        elif "cs1" in i or "cs3" in i or "cs5" in i:
            root_port = j
        else: pass
            
            
    if 'Te' in root_port:
        root_port = root_port.replace("Ten", "Te")
    elif 'Gi' in root_port:
        root_port = root_port.replace("Gig", "Gi")

#----------------------------------------------------------------------------------------

    res_list = []
    for i, j in vlan_dict.items():
        if j == root_port:
            res_list.append({'timestamp' : formatted_time,
                    'switch name' : i_hostname,
                    'vlan' : i,
                    'discrepancy': 'no',
                    'mac': mac_dict[i]               
                    })
        
        elif j != root_port:
            res_list.append({'timestamp' : formatted_time,
                    'switch name' : i_hostname,
                    'vlan' : i,
                    'discrepancy': 'yes',
                    'mac': mac_dict[i]               
                    })    
    
    return res_list

def check_bpdu(i_string1, i_string2, i_hostname):
    #return ['timestamp', 'switch name', 'interface name', 'configuration', 'remarks']
    #once this function is called, it'll return the above dict inside a list, to the caller.
    current_time = time.time()
    formatted_time = datetime.fromtimestamp(current_time).strftime("%m-%d-%Y %H:%M:%S")    
    test_list1 = i_string1.splitlines()
    test_list2 = i_string2.splitlines()

    test_list3= []
    for i in test_list2:
        if 'Ethernet' in i or 'bpdu' in i:
            test_list3.append(i)
    #print(test_list1, 5*'\n', test_list3 )
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
        if 'trunk' in list3:
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
    #return #return ['timestamp', 'switch name', 'discrepancy', 'vlans', 'trunked_vlans', 'remarks']
    #once this function is called, it'll return the above dict inside a list, to the caller.
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

    res_check_vlan2 = []
    for p,q in trunked_vlans.items():
        if "-" in q and "," not in q:
            l = q.split("-")
            vlanss = [x for x in vlans if int(x) in range(int(l[0]),int(l[-1])+1)]
            vlanss.sort()
            if vlanss==vlans:
                res_check_vlan2.append({'timestamp' : formatted_time,
                        'switch name' : i_hostname,
                        'discrepancy': 'no',
                        'vlans' : vlans,
                        'trunked_vlans': f"{p}:{q}",
                        'remarks': ''
                        })
            else:
                res_check_vlan2.append({'timestamp' : formatted_time,
                        'switch name' : i_hostname,
                        'discrepancy': 'yes',
                        'vlans' : vlans,
                        'trunked_vlans': f"{p}:{q}",
                        'remarks': 'trunk configuration required'
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
                        'switch name' : i_hostname,
                        'discrepancy': 'no',
                        'vlans' : vlans,
                        'trunked_vlans': f"{p}:{q}",
                        'remarks': ''
                        })
            else:
                res_check_vlan2.append({'timestamp' : formatted_time,
                        'switch name' : i_hostname,
                        'discrepancy': 'yes',
                        'vlans' : vlans,
                        'trunked_vlans': f"{p}:{q}",
                        'remarks': 'trunk configuration required'
                        })
                
        elif "," not in q and "-" not in q:
            l = []
            l.append(q)
            vlanss = [x for x in vlans if x in l]
            if vlanss==vlans:
                res_check_vlan2.append({'timestamp' : formatted_time,
                        'switch name' : i_hostname,
                        'discrepancy': 'no',
                        'vlans' : vlans,
                        'trunked_vlans': f"{p}:{q}",
                        'remarks': ''
                        })
            else:
                res_check_vlan2.append({'timestamp' : formatted_time,
                        'switch name' : i_hostname,
                        'discrepancy': 'yes',
                        'vlans' : vlans,
                        'trunked_vlans': f"{p}:{q}",
                        'remarks': 'trunk configuration required'
                        })
        elif "," in q:
            l = q.split(",")
            vlanss = [x for x in vlans if x in l]
            vlanss.sort()
            if vlanss==vlans:
                res_check_vlan2.append({'timestamp' : formatted_time,
                        'switch name' : i_hostname,
                        'discrepancy': 'no',
                        'vlans' : vlans,
                        'trunked_vlans': f"{p}:{q}",
                        'remarks': ''
                        })
            else:
                res_check_vlan2.append({'timestamp' : formatted_time,
                        'switch name' : i_hostname,
                        'discrepancy': 'yes',
                        'vlans' : vlans,
                        'trunked_vlans': f"{p}:{q}",
                        'remarks': 'trunk configuration required'
                        })
        else: continue
    
    return(res_check_vlan2)

def check_vlan_priority(i_string1, i_string2, i_hostname):
    #return ['timestamp', 'switch name', 'discrepancy', 'missing_vlans', 'priority', 'remarks']
    current_time = time.time()
    formatted_time = datetime.fromtimestamp(current_time).strftime("%m-%d-%Y %H:%M:%S") 
    res_check_priority_list = []
    
    test_list1 = i_string1.splitlines()
    test_list2 = i_string2.splitlines()
    
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
                'switch name' : i_hostname,
                'discrepancy': 'no',
                'missing_vlans' : [x for x in vlans_in_switch if x not in vlans_total],
                'priority': vlans_priority_dict,
                'remarks': ''
                }
    else:
        res_check_priority_dict = {'timestamp' : formatted_time,
                'switch name' : i_hostname,
                'discrepancy': 'yes',
                'missing_vlans' : [x for x in vlans_in_switch if x not in vlans_total],
                'priority': vlans_priority_dict,
                'remarks': 'config changes required'
                }
    res_check_priority_list.append(res_check_priority_dict)    
    return(res_check_priority_list)

def check_loopguard(i_string1, i_string2, i_string3, i_hostname):
    #return ['timestamp', 'switch name', 'interface name', 'configuration']
    current_time = time.time()
    formatted_time = datetime.fromtimestamp(current_time).strftime("%m-%d-%Y %H:%M:%S") 

    
    test_list1 = i_string1.splitlines()
    test_list2 = i_string2.splitlines()
    test_list3 = i_string3.splitlines()
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
    if 'as' in i_hostname or 'AS' in i_hostname:
        for i in range(len(dtpo3)):
            p = dtpo3.iloc[i,0]
            if 'ds' in p or 'ds1' in p or 'ds2' in p or 'ds3' in p\
                or 'DS' in p or 'ds4' in p or 'ds5' in p or 'ds6' in p\
                    or 'ds7' in p or 'ds8' in p or 'cs' in p:
                        uplinks_trunk_list.append(str(dtpo3.iloc[i+1,0]) \
                                                  + str(dtpo3.iloc[i+1,1]))
            else: pass
    elif 'ds' in i_hostname or 'DS' in i_hostname:
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
                    'switch name' : i_hostname,
                    'interface name': i,
                    'configuration': 'yes'
                    })
        elif i in trunks_list and i not in loop_guard_ints:
            res_check_loopguard_list.append({'timestamp' : formatted_time,
                    'switch name' : i_hostname,
                    'interface name': i,
                    'configuration': 'no'
                    })
        else: res_check_loopguard_list.append({'timestamp' : formatted_time,
                'switch name' : i_hostname,
                'interface name': i,
                'configuration': 'warning'
                })
        
    return res_check_loopguard_list

def check_keepalive(i_string1, i_string2, i_hostname):
    #return ['timestamp', 'switch name', 'interface name', 'status']
    current_time = time.time()
    formatted_time = datetime.fromtimestamp(current_time).strftime("%m-%d-%Y %H:%M:%S") 
    
    test_list1 = i_string1.splitlines()
    test_list = i_string2.splitlines()
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
                    'switch name' : i_hostname,
                    'interface name': m,
                    'status': 'correct'
                    })
        elif 'access' in n and 'not-set' in n and 'notconnect' in n:
            res_check_keepalive_list.append({'timestamp' : formatted_time,
                    'switch name' : i_hostname,
                    'interface name': m,
                    'status': 'warning'
                    })
        elif 'trunk' in n and 'not-set' in n:
            res_check_keepalive_list.append({'timestamp' : formatted_time,
                    'switch name' : i_hostname,
                    'interface name': m,
                    'status': 'correct'
                    })
        elif 'trunk' in n and 'set' in n and 'notconnect' in n:
            res_check_keepalive_list.append({'timestamp' : formatted_time,
                    'switch name' : i_hostname,
                    'interface name': m,
                    'status': 'warning'
                    })
        elif '1/1/' in m and 'not-set' in n and 'connected' in n:
            res_check_keepalive_list.append({'timestamp' : formatted_time,
                    'switch name' : i_hostname,
                    'interface name': m,
                    'status': 'correct'
                    })
        else:
            res_check_keepalive_list.append({'timestamp' : formatted_time,
                    'switch name' : i_hostname,
                    'interface name': m,
                    'status': 'not correct'
                    })
            
    return res_check_keepalive_list       
        
