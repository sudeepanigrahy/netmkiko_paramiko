import sys
import subprocess
import ipaddress
from ipaddress import IPv4Address
from ipaddress import ip_address
from ipaddress import ip_network
from ipaddress import IPv4Network
import pandas as pd
from netmiko import ConnectHandler
import ip_grouper
from ip_reachability import reachability

def failediptracer(dtpo1):
    lasthoplist = []
    for i in range(dtpo1.shape[0]):
        hop = list(dtpo1.loc[i].values)        
        if 'Request' in hop and 'timed' in hop and 'out.' in hop:
            lasthoplist = list(dtpo1.loc[i - 1].values)
            break
    
    failedlasthop = ''
    for i in lasthoplist:
        if "[" in str(i) and "]" in str(i):
            failedlasthop = str(i)
            failedlasthop = failedlasthop.replace("[","")
            failedlasthop = failedlasthop.replace("]","")

    if failedlasthop == '':
        for i in lasthoplist:
            if "." in str(i) and ipaddress.ip_address(str(i)): failedlasthop = str(i)
    else: pass
                    
    return failedlasthop   
    
def findcorrectlayerthree(apparentlayerthree, unreachableip):
    try:
        callthegrouper = ip_grouper.subnet_finder(apparentlayerthree, unreachableip)
        if IPv4Address(f'{unreachableip}') in IPv4Network(f'{callthegrouper[0][0]}/{callthegrouper[0][1]}'):
            return apparentlayerthree
        else: return "something's fishy"
    except:
        lthree_connection = reachability(f"{apparentlayerthree}")
        output = lthree_connection.send_command(f"sh ip route {unreachableip}")

        dtpo = pd.DataFrame(output.splitlines())
        list1 = dtpo.values[0][0].split()
        dtpo1 = pd.DataFrame(list1).T

        for i in range(1,len(output.splitlines())):
            xx = dtpo.values[i][0].split()
            
            for j in range(len(xx)):
                dtpo1.loc[i, j] = xx[j]
                
        dtpo1 = dtpo1.reset_index(drop=True)

        for i in range(dtpo1.shape[0]):
            if dtpo1.loc[i, 0] == '*':
                return str(dtpo1.loc[i, 1]).replace(",", "")
                break
        
def iptracer(rs, rd):
    #This function requires to receive the output of the ipchecker()
    #function as its parameters
    print("\n", "Lets find out the traces of the machines..", "\n", sep="")
    reachable_sources = rs
    reachable_destinations = rd
    reachable_sources_traces = {}
    reachable_destinations_traces = {}
    
    for index, ip_checkered_lists in enumerate([reachable_sources, reachable_destinations]):
        for address in ip_checkered_lists:            
            output = subprocess.check_output(f"tracert {address}", shell=True).decode('utf-8')        
            dtpo = pd.DataFrame(output.splitlines())
            list1 = dtpo.values[0][0].split()
            dtpo1 = pd.DataFrame(list1).T
    
            for i in range(1,len(output.splitlines())):
                xx = dtpo.values[i][0].split()
                
                for j in range(len(xx)):
                    dtpo1.loc[i, j] = xx[j]
                    
            dtpo1 = dtpo1.reset_index(drop=True)       
            last_hop = list(dtpo1.loc[int(dtpo1.shape[0]) - int(2)])
            possible_hostname_address = ""
            possible_ip_address = ""
            
            if dtpo1.loc[int(dtpo1.shape[0])-int(1), 0] == "Trace" and dtpo1.loc[int(dtpo1.shape[0])-int(1), 1] == "complete.":
                if "Request" in last_hop and "timed" in last_hop and "out." in last_hop:
                    if index == 0:
                        failediptraces = failediptracer(dtpo1)
                        reachable_sources_traces[address]=["trace_failure", failediptraces]
                    elif index == 1: 
                        failediptraced = failediptracer(dtpo1)
                        reachable_destinations_traces[address]=["trace_failure", failediptraced] 
                    continue
                else:    
                    possible_hostname_address = str(dtpo1.loc[int(dtpo1.shape[0])-int(2), 7])
                    possible_ip_address = str(dtpo1.loc[int(dtpo1.shape[0])-int(2), 8])
            else: 
                print(f"There is a new variety at x-1, from the trace of {address}, contact designer")
                exit()
                
            if possible_ip_address == 'nan':
                possible_hostname_address=possible_hostname_address.replace("[","")
                possible_hostname_address=possible_hostname_address.replace("]","")
                if ipaddress.ip_address(possible_hostname_address) and possible_hostname_address==address:
                    #print('we have to go above here')
                    possible_L3_hop_hostname = str(dtpo1.loc[int(dtpo1.shape[0])-int(3), 7])
                    possible_L3_hop_ip = str(dtpo1.loc[int(dtpo1.shape[0])-int(3), 8])
                    possible_L3_hop_hostname=possible_L3_hop_hostname.replace("[","")
                    possible_L3_hop_hostname=possible_L3_hop_hostname.replace("]","")
                    possible_L3_hop_ip=possible_L3_hop_ip.replace("[","")
                    possible_L3_hop_ip=possible_L3_hop_ip.replace("]","")
                    
                    if possible_L3_hop_ip=="nan" and ipaddress.ip_address(possible_L3_hop_hostname):
                        if index == 0: reachable_sources_traces[address]=[possible_L3_hop_hostname]
                        elif index == 1: reachable_destinations_traces[address]=[possible_L3_hop_hostname]
                    elif possible_L3_hop_ip!="nan" and ipaddress.ip_address(possible_L3_hop_ip):
                        if index == 0: reachable_sources_traces[address]=[possible_L3_hop_ip]
                        elif index == 1: reachable_destinations_traces[address]=[possible_L3_hop_ip]
                    else: 
                        print("There is a new variety at x-3, contact designer")
                        exit()
            elif possible_ip_address != "nan":
                possible_ip_address=possible_ip_address.replace("[","")
                possible_ip_address=possible_ip_address.replace("]","")
                if possible_ip_address==address:
                    #print('we have to go above here')
                    possible_L3_hop_hostname = str(dtpo1.loc[int(dtpo1.shape[0])-int(3), 7])
                    possible_L3_hop_ip = str(dtpo1.loc[int(dtpo1.shape[0])-int(3), 8])
                    possible_L3_hop_hostname=possible_L3_hop_hostname.replace("[","")
                    possible_L3_hop_hostname=possible_L3_hop_hostname.replace("]","")
                    possible_L3_hop_ip=possible_L3_hop_ip.replace("[","")
                    possible_L3_hop_ip=possible_L3_hop_ip.replace("]","")
                    
                    if possible_L3_hop_ip=="nan" and ipaddress.ip_address(possible_L3_hop_hostname):
                        if index == 0: reachable_sources_traces[address]=[possible_L3_hop_hostname]
                        elif index == 1: reachable_destinations_traces[address]=[possible_L3_hop_hostname]
                    elif possible_L3_hop_ip!="nan" and ipaddress.ip_address(possible_L3_hop_ip):
                        if index == 0: reachable_sources_traces[address]=[possible_L3_hop_ip]
                        elif index == 1: reachable_destinations_traces[address]=[possible_L3_hop_ip]
                    else: 
                        print("There is a new variety at x-3, contact designer")
                        exit()
                else:
                    print(f"This is unusual, something wrong with trace of {address} at x-2, contact designer")
                    exit()
            else:
                print("There is a new variety at x-2, contact designer")
    
    filetypeobject = open("failed.txt", "w")

    print(reachable_sources_traces)
    print(reachable_destinations_traces)

    new_reachable_sources_traces = {}
    new_reachable_destinations_traces = {}
    for index, L3s in enumerate([reachable_sources_traces, reachable_destinations_traces]):
        for kee, val in L3s.items():
            if val[0] == 'trace_failure' and index==0 and ipaddress.ip_address(val[1]):
                print(f"\nThe {kee} address is unreachable, but still making it a part of further processing..\n")
                truelayerthree = findcorrectlayerthree(val[1], kee)
                new_reachable_sources_traces[kee] = truelayerthree
                filetypeobject.write(kee)
                filetypeobject.write('\n')
                continue
            elif val[0] != 'trace_failure' and index==0:
                new_reachable_sources_traces[kee] = val[0]
            elif val[0] == 'trace_failure' and index==1 and ipaddress.ip_address(val[1]):
                print(f"\nThe {kee} address is unreachable, but still making it a part of further processing..\n")
                truelayerthree = findcorrectlayerthree(val[1], kee)
                new_reachable_destinations_traces[kee] = truelayerthree
                filetypeobject.write(kee)
                filetypeobject.write('\n')
                continue
            elif val[0] != 'trace_failure' and index==1:
                new_reachable_destinations_traces[kee] = val[0]    
    filetypeobject.close()
        
    print(f"Sources_L3s: {new_reachable_sources_traces}", '\n', f"Destinations_L3s: {new_reachable_destinations_traces}", '\n', sep="")                        
    return (new_reachable_sources_traces, new_reachable_destinations_traces)                
     

        