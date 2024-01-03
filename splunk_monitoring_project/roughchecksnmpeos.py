from netmiko import ConnectHandler
from paramiko.ssh_exception import SSHException
from netmiko import NetmikoTimeoutException
import csv
import sys
import re
#import datetime
from datetime import datetime
import time


def work(connection, i_hostname):
    #return ['timestamp', 'switch name', 'uptime']
    #once this function is called, it'll return the above dict inside a list, to the caller.
    
    current_time = time.time()
    formatted_time = datetime.fromtimestamp(current_time).strftime("%m-%d-%Y %H:%M:%S") 
    res_list = []
    
    #switch = "***********"

    i_string = connection.send_command("sh run")
    
    
    #test_string2 = connection.send_command("show int trunk")
    #test_list1 = test_string1.splitlines()
    #test_list2 = test_string2.splitlines()
    """
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
    """

    if "xxxxx" in i_hostname:
        ip1 = "***********"
        ip2 = "***********"
        if "***********" in i_string and "***********" in i_string and ip1 in i_string and ip2 in i_string:
            discrepancy = "no"
            remark = ""
        else:
            discrepancy = "yes"
            remark = "SNMP server missing"
    elif "xxxxx" in i_hostname:
        ip1 = "***********"
        ip2 = "***********"
        if "***********" in i_string and "***********" in i_string and ip1 in i_string and ip2 in i_string:
            discrepancy = "no"
            remark = ""
        else:
            discrepancy = "yes"
            remark = "SNMP server missing"
    elif "xxxxx" in i_hostname:
        ip1 = "***********"
        ip2 = "***********"
        if "***********" in i_string and "***********" in i_string and ip1 in i_string and ip2 in i_string:
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
    
    print(res_list)        
    #return res_list
   


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
            'device_type': 'cisco_nxos','ip': i,'username': '***********','password': '***********','port':'22'
            }
        connection = ConnectHandler(**kwargs)
    except:
        try:
            kwargs = {
                'device_type': 'cisco_ios_telnet','ip': i,'username': '***********','password': '***********','port':'23'
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
