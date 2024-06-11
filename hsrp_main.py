from netmiko import ConnectHandler
from paramiko.ssh_exception import SSHException
from netmiko import NetmikoTimeoutException
import pandas as pd
import csv
import sys
import re
import datetime
import time

global h
h = ['Switch', 'Vlan', 'Group', 'Priority', 'Preempt', 'State', 'Active', 'Standby', 'Virtual_IP', 'Remarks']

with open("login_issue.csv", "w", newline='') as filetypeobject:
    header = ["switchname"]
    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
    dictwritertypeobject.writeheader()
    
with open("output.csv", "w", newline='') as filetypeobject:
    header = h
    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
    dictwritertypeobject.writeheader()

def work(connection, switch):
    
    test_string1 = connection.send_command("sh standby br")    
    test_list1 = test_string1.splitlines()
     
    dtpo = pd.DataFrame(test_list1)
    list1 = dtpo.values[0][0].split()
    dtpo1 = pd.DataFrame(list1).T
    
    for i in range(1,len(test_list1)):
        xx = dtpo.values[i][0].split()
        
        for j in range(len(xx)):
            dtpo1.loc[i, j] = xx[j]
    dtpo1 = dtpo1.reset_index(drop=True)
    

    remark = ''
    for i in range(3, len(dtpo1)):
                
        if dtpo1.loc[i, 3] == 'P':
            if dtpo1.loc[i, 4] == 'Active': remark = 'Okay, Active'
            else: remark = dtpo1.loc[i, 4]
            
            with open("output.csv", "a", newline='') as filetypeobject:
                header = h
                dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
                dictwritertypeobject.writerow({h[0]: switch , h[1]: dtpo1.loc[i, 0], h[2]: dtpo1.loc[i, 1], h[3]: dtpo1.loc[i, 2], \
                                               h[4]: dtpo1.loc[i, 3], h[5]: dtpo1.loc[i, 4], h[6]: dtpo1.loc[i, 5], h[7]: dtpo1.loc[i, 6], \
                                                   h[8]: dtpo1.loc[i, 7], h[9]: remark})
                connection.disconnect()        
        else:
            if dtpo1.loc[i, 3] == 'Active': remark = 'Okay, Active'
            else: remark = dtpo1.loc[i, 3]
            
            with open("output.csv", "a", newline='') as filetypeobject:
                header = h
                dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
                dictwritertypeobject.writerow({h[0]: switch , h[1]: dtpo1.loc[i, 0], h[2]: dtpo1.loc[i, 1], h[3]: dtpo1.loc[i, 2], \
                                               h[4]: 'NA', h[5]: dtpo1.loc[i, 3], h[6]: dtpo1.loc[i, 4], h[7]: dtpo1.loc[i, 5], \
                                                   h[8]: dtpo1.loc[i, 6], h[9]: remark})
                connection.disconnect()
            
    
    
def reachability(switchlist):        
    global connection
    for switch in switchlist:
        print(f"Working on {switch}...")
        try:
            kwargs = {
                'device_type': 'cisco_ios','ip': switch,'username': 'spanigrahy','password': 'Sueme@1123','port':'22'
                }
            connection = ConnectHandler(**kwargs)
            work(connection, switch)                        
        except:
            try:
                kwargs = {
                    'device_type': 'cisco_ios_telnet','ip': switch,'username': 'spanigrahy','password': 'Sueme@1123','port':'23'
                    }
                connection = ConnectHandler(**kwargs)
                work(connection, switch)
            except:
                print("can't login through ssh or telnet", switch)
                with open("login_issue.csv", "a", newline='') as filetypeobject:
                    header = ["switchname"]
                    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
                    dictwritertypeobject.writerow({'switchname': switch})
                    connection.disconnect()

                
with open("switchlist.csv", "r") as filetypeobject:
    header = ["switchname"]
    dictreadertypeobject = csv.DictReader(filetypeobject, fieldnames = header)
    inputswitchlist = []
    for i in dictreadertypeobject:
        inputswitchlist.append(i["switchname"])
    inputswitchlist.pop(0)
    reachability(inputswitchlist)                
        
