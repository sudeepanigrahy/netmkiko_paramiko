import re
import time
from datetime import datetime
import pandas as pd

# returns a list of dictionary for each queried device
def check_crc(i_string, i_hostname):
    
    res_dict_list = []

    current_time = time.time()
    formatted_time = datetime.fromtimestamp(current_time).strftime("%m-%d-%Y %H:%M:%S")    
    
    expression_1 = "^.*Ethernet[0-9]+(\/[0-9]+)+.*"
    expression_2 = "^.*E[0-9]+(\/[0-9]+)+.*"
    i_string = i_string.replace("\\r\\n", " ")
    string_split_by_whitespace = i_string.split()
    
    cur_index = 0
    cur_sub_index = 0
    for entry in string_split_by_whitespace:
        if(re.search(expression_1, entry) or re.search(expression_2, entry)):
            input_error = None
            output_error = None
            CRC_error = None
            cur_sub_index = cur_index
            interface_name = string_split_by_whitespace[cur_index]
            for sub_entry in string_split_by_whitespace[cur_index:]:
                if('input' in sub_entry):
                    input_error = string_split_by_whitespace[cur_sub_index - 1]
                if('output' in sub_entry):
                    output_error = string_split_by_whitespace[cur_sub_index - 1]
                if('CRC' in sub_entry):
                    CRC_error = string_split_by_whitespace[cur_sub_index - 1]
                if(input_error != None and output_error != None and CRC_error != None): break
                cur_sub_index += 1
            
            res_dict_list.append({
                    'timestamp': formatted_time,
                    'switch name': i_hostname,
                    'interface name': interface_name,
                    'CRC error': CRC_error,
                    'input error': input_error,
                    'output_error': output_error
                })
                
        cur_index += 1

    return res_dict_list

def check_snmp_config(i_string, i_hostname): 
    #return ['timestamp', 'switch name', 'discrepancy', 'remarks']
    #once this function is called, it'll return the above dict inside a list, to the caller.
    
    
    current_time = time.time()
    formatted_time = datetime.fromtimestamp(current_time).strftime("%m-%d-%Y %H:%M:%S")        
    res_list = []
    
    if "sg209" in i_hostname:
        ip1 = "10.160.20.60"
        ip2 = "10.160.21.9"
        if "rc4sing" in i_string and "wc4sing" in i_string and ip1 in i_string and ip2 in i_string:
            discrepancy = "no"
            remark = ""
        else:
            discrepancy = "yes"
            remark = "SNMP server missing"
    elif "sg624" in i_hostname:
        ip1 = "10.193.189.120"
        ip2 = "10.193.189.26"
        if "rc4sing" in i_string and "wc4sing" in i_string and ip1 in i_string and ip2 in i_string:
            discrepancy = "no"
            remark = ""
        else:
            discrepancy = "yes"
            remark = "SNMP server missing"
    elif "sg211" in i_hostname:
        ip1 = "172.25.243.229"
        ip2 = "172.25.243.230"
        if "rc4sing" in i_string and "wc4sing" in i_string and ip1 in i_string and ip2 in i_string:
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
        if 'trunk' in list3 or 'routed' in list3:
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
        p = list(dtpo3.iloc[i].values)
        if 'Port' in p and 'Vlans' in p and 'Allowed' in p and 'on' in p and 'Trunk' in p:
            for j in range(i+1, len(list(dtpo3[0].values))):
                m = dtpo3.iloc[j,0]
                if 'Port' in m:
                    break
                elif 'Eth' in m or 'Gi' in m or 'Te' in m or 'Twe' in m:
                    trunked_vlans[m] = dtpo3.iloc[j,1]
                else: continue
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
# PLEASE ONLY INCLUDE THE FINISHED AND TESTED PARAMETER HANDLER FUNCTIONS INTO THIS FILE