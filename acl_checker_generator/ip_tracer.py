import sys
import subprocess
import ipaddress
import pandas as pd
from netmiko import ConnectHandler


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
                    if index == 0: reachable_sources_traces[address]="trace_failure"
                    elif index == 1: reachable_destinations_traces[address]="trace_failure" 
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
                        if index == 0: reachable_sources_traces[address]=possible_L3_hop_hostname
                        elif index == 1: reachable_destinations_traces[address]=possible_L3_hop_hostname
                    elif possible_L3_hop_ip!="nan" and ipaddress.ip_address(possible_L3_hop_ip):
                        if index == 0: reachable_sources_traces[address]=possible_L3_hop_ip
                        elif index == 1: reachable_destinations_traces[address]=possible_L3_hop_ip
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
                        if index == 0: reachable_sources_traces[address]=possible_L3_hop_hostname
                        elif index == 1: reachable_destinations_traces[address]=possible_L3_hop_hostname
                    elif possible_L3_hop_ip!="nan" and ipaddress.ip_address(possible_L3_hop_ip):
                        if index == 0: reachable_sources_traces[address]=possible_L3_hop_ip
                        elif index == 1: reachable_destinations_traces[address]=possible_L3_hop_ip
                    else: 
                        print("There is a new variety at x-3, contact designer")
                        exit()
                else:
                    print(f"This is unusual, something wrong with trace of {address} at x-2, contact designer")
                    exit()
            else:
                print("There is a new variety at x-2, contact designer")
                
    print(f"Sources_L3s: {reachable_sources_traces}", '\n', f"Destinations_L3s: {reachable_destinations_traces}", '\n', sep="")                        
    return (reachable_sources_traces, reachable_destinations_traces)                
     

        