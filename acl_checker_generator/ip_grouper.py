import sys
import pandas as pd
from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoAuthenticationException
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import SSHException
from ipaddress import IPv4Address
from ipaddress import ip_address
from ipaddress import ip_network
from ipaddress import IPv4Network
from ip_reachability import reachability

def subnet_finder(lthree, actual_ip):
    if IPv4Address(lthree):
        lthree_connection = reachability(lthree)
        string = lthree_connection.send_command("sh vlan br")
        string_list = string.splitlines()

        dtpo = pd.DataFrame(string_list)
        list1 = dtpo.values[0][0].split()
        dtpo1 = pd.DataFrame(list1).T

        for i in range(1,len(string_list)):
            xx = dtpo.values[i][0].split()
            
            for j in range(len(xx)):
                dtpo1.loc[i, j] = xx[j]

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

        vlan_details = {}
        for vlan in vlans:
            vlan_details[vlan] = {'subnet_svi' : 'not_present', 'access_list_in' : 'not_present',\
                                  'access_list_out' : 'not_present'}

        for vlan_no in vlans:
            vlan_string = lthree_connection.send_command(f"sh run int vlan {vlan_no}")
            
            if 'Invalid' in vlan_string or 'input' in vlan_string:
                continue
            else:    
                vlan_string_list = vlan_string.splitlines()
                        
                dtpo2 = pd.DataFrame(vlan_string_list)
                list1 = dtpo2.values[0][0].split()
                dtpo3 = pd.DataFrame(list1).T
                
                for i in range(1,len(vlan_string_list)):
                    xx = dtpo2.values[i][0].split()
                    
                    for j in range(len(xx)):
                        dtpo3.loc[i, j] = xx[j] 
                dtpo3 = dtpo3.reset_index(drop=True)
                
                for row in range(len(dtpo3)):
                    if dtpo3.loc[row][0]=='ip' and dtpo3.loc[row][1]=='address':
                        vlan_details[vlan_no]['subnet_svi'] = [dtpo3.loc[row][2], dtpo3.loc[row][3]]
                    elif dtpo3.loc[row][0]=='ip' and dtpo3.loc[row][1]=='access-group' and dtpo3.loc[row][3]=='in':
                        vlan_details[vlan_no]['access_list_in'] = dtpo3.loc[row][2]
                    elif dtpo3.loc[row][0]=='ip' and dtpo3.loc[row][1]=='access-group' and dtpo3.loc[row][3]=='out':
                        vlan_details[vlan_no]['access_list_out'] = dtpo3.loc[row][2]                
                    else: continue
                
        subnet_of_ip = []
        vlan_details_actual_ip = []
        for kee, val in vlan_details.items():            
            if vlan_details[kee]['subnet_svi']=='not_present': continue
            elif IPv4Address(actual_ip) in \
                ip_network(f"{vlan_details[kee]['subnet_svi'][0]}/{vlan_details[kee]['subnet_svi'][1]}",\
                           strict=False):
                subnet_of_ip.append(str(ip_network(f"{vlan_details[kee]['subnet_svi'][0]}/{vlan_details[kee]['subnet_svi'][1]}",\
                           strict=False).network_address))
                subnet_of_ip.append(str(ip_network(f"{vlan_details[kee]['subnet_svi'][0]}/{vlan_details[kee]['subnet_svi'][1]}",\
                           strict=False).netmask))  
                vlan_details_actual_ip.append(vlan_details[kee])
                vlan_details_actual_ip[0]['vlan_number'] = kee 
                break    
            else: continue     
        
        return [subnet_of_ip, vlan_details_actual_ip[0]]
    else:
        return "Subnet details couldn't be obtained, check with designer."

"""
sources = ['10.195.24.112', '10.195.24.111', '10.195.18.62', '10.195.10.50']
destinations = ['10.195.188.64', '10.195.188.31', '10.195.188.65', '10.195.188.50']
sources_traces = {'10.195.24.112': '10.195.1.30', '10.195.24.111': '10.195.1.30', \
                  '10.195.18.62': '10.195.1.18', '10.195.10.50': '10.195.1.2'}
destinations_traces = {'10.195.188.64': '10.195.1.74', '10.195.188.31': '10.195.1.74', \
                       '10.195.188.65': '10.195.1.74', '10.195.188.50': '10.195.1.74'}    
"""
    
def ipgrouper(sources, destinations, sources_traces, destinations_traces):
    #This function requires to receive the outputs of ipchecker() and iptracer()
    #functions as its parameters
    print("Lets group the source and destination IPs acc. to subnets..", '\n', sep="")
    sources_subnets = {}
    destinations_subnets = {} 
    sources_vlan_details = {}
    destinations_vlan_details = {}
    
    for index, ips_side in enumerate([sources, destinations]):
        for ip in ips_side:
            if index==0: 
                xx = subnet_finder(sources_traces[ip], ip)
                sources_subnets[ip] = xx[0]
                sources_vlan_details[ip] = xx[1] 
            elif index==1: 
                yy = subnet_finder(destinations_traces[ip], ip)
                destinations_subnets[ip] = yy[0]
                destinations_vlan_details[ip] = yy[1]
                
    sources_subnets_set = []
    destinations_subnets_set = []
    for inde, subnets_side in enumerate([sources_subnets, destinations_subnets]):
        for ipv4, subnet in subnets_side.items():
            if inde==0: sources_subnets_set.append(str(IPv4Network(f"{subnet[0]}/{subnet[1]}")))
            elif inde==1: destinations_subnets_set.append(str(IPv4Network(f"{subnet[0]}/{subnet[1]}")))
    sources_subnets_set = list(set(sources_subnets_set))
    destinations_subnets_set = list(set(destinations_subnets_set))
            
    sources_subnets_set_dict = {}
    destinations_subnets_set_dict = {}
    for ind,subnets_set_side  in enumerate([sources_subnets_set, destinations_subnets_set]):
        for sub in subnets_set_side:
            if ind==0: sources_subnets_set_dict[sub] = []
            if ind==1: destinations_subnets_set_dict[sub] = []
    
    list(map(lambda x: list(map(lambda y: sources_subnets_set_dict[y].append(x) if IPv4Address(x) in IPv4Network(y) else 'no-subnet',\
                               list(sources_subnets_set_dict.keys()))), list(sources_subnets.keys())))
        
    list(map(lambda x: list(map(lambda y: destinations_subnets_set_dict[y].append(x) if IPv4Address(x) in IPv4Network(y) else 'no-subnet',\
                               list(destinations_subnets_set_dict.keys()))), list(destinations_subnets.keys())))
    
    sources_grouped = list(sources_subnets_set_dict.values())
    destinations_grouped = list(destinations_subnets_set_dict.values())
    print(f"Sources_Grouped: {sources_grouped}", '\n', f"Destinations_Grouped: {destinations_grouped}", '\n', sep="")
    
    return(sources_grouped, destinations_grouped, sources_vlan_details, destinations_vlan_details)
            
        







