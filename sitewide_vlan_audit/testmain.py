from netmiko import ConnectHandler
from paramiko.ssh_exception import SSHException
from netmiko import NetmikoTimeoutException
import csv
import sys
import re
import datetime
import time
import checkusedvlans
import checkvlansiftrunked
import checkvlanspriority
import checkvlansrootport
import checkdownlinktrunkedvlans
import vlansconverter

global h
h = ['AS Hostname', 'Spanning-tree Root','AS-Used VLANs','AS-Configured VLANs','AS-Trunked VLANs to Primary',\
     'AS-Trunked VLANs to Secondary','Primary Connected DS Hostname','Primary DS-Configured VLANs',\
         'Primary DS-Trunked VLANs','Secondary Connected DS Hostname','Secondary DS-Configured VLANs',\
             'Secondary DS-Trunked VLANs','Configured VLAN Mismatch','Used VLAN Mismatch']

with open("output.csv", "w", newline='') as filetypeobject:
    header = h
    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
    dictwritertypeobject.writeheader()
    
with open("unconnectables.csv", "w", newline='') as filetypeobject:
    header = ["switchname"]
    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
    dictwritertypeobject.writeheader()


def work(connection, switch):
    
    var1 = connection.send_command("sh int status")
    var2 = connection.send_command("sh vlan br")
    var3 = connection.send_command("sh int trunk")
    var4 = connection.send_command("sh run")
    var5 = connection.send_command("sh cdp nei")
    var6 = connection.send_command("sh spanning-tree root")
    
    one = checkvlansrootport.vlansrootport(var5, var6, switch)[0]
    two = checkusedvlans.usedvlans(var1)
    var7 = checkvlansiftrunked.vlansiftrunked(var2, var3, switch)
    three = var7[0]['vlans']
    list1=[]
    #print(checkvlansrootport.vlansrootport(var5, var6, switch))
    root = checkvlansrootport.vlansrootport(var5, var6, switch)[1][0]
    try:
        secondary_root = checkvlansrootport.vlansrootport(var5, var6, switch)[2][0]
    except:
        secondary_root = 'anomaly/not-present'
    four = ''
    five =''
    for i in range(len(var7)):
        for m,n in var7[i].items():
            if root in n:
                four = n.split(":")[-1]
            elif secondary_root in n:
                five = n.split(":")[-1]
                
    fourr = vlansconverter.converter(str(four), three)
    fivee = vlansconverter.converter(str(five), three)
    six = checkvlansrootport.vlansrootport(var5, var6, switch)[3]
    nine = checkvlansrootport.vlansrootport(var5, var6, switch)[4]
    list1.append(str(six))
    list1.append(str(nine))
    #print(f"list1 is {list1}")
    var10 = ''
    var11 = ''
    var13 = ''
    for m,n in enumerate(list1):
        if m == 0:
            try:
                try:
                    kwargs = {
                        'device_type': 'cisco_ios','ip': n,'username': '*********','password': '**********'
                        }
                    connection1 = ConnectHandler(**kwargs)
                except:
                    kwargs = {
                        'device_type': 'cisco_ios_telnet','ip': n,'username': '*********','password': '***********'
                        }
                    connection1 = ConnectHandler(**kwargs)
            except:
                print("AIN'T HAPPENING FOR", n)
                with open("unconnectables.csv", "a", newline='') as filetypeobject:
                    header = ["switchname"]
                    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
                    dictwritertypeobject.writerow({'switchname': n})
                    connection.disconnect()
                    return None
                
        else:
            if n == '':
                break
            else:
                try:
                    try:
                        #print("here is n: ",n)
                        kwargs = {
                            'device_type': 'cisco_ios','ip': n,'username': '***********','password': '**********'
                            }
                        connection2 = ConnectHandler(**kwargs)
                    except:
                        kwargs = {
                            'device_type': 'cisco_ios_telnet','ip': n,'username': '**********','password': '**********'
                            }
                        connection2 = ConnectHandler(**kwargs)
                    
                    var10 = connection2.send_command("sh cdp nei")
                    var11 = connection2.send_command("sh vlan br")
                    var13 = connection2.send_command("sh int trunk")
                    #print(var11,var13)
                except:
                    print("AIN'T HAPPENING FOR", n)
                    with open("unconnectables.csv", "a", newline='') as filetypeobject:
                        header = ["switchname"]
                        dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
                        dictwritertypeobject.writerow({'switchname': n})
                        connection.disconnect()
                        return None
                    
    var8 = connection1.send_command("sh cdp nei")
    var9 = connection1.send_command("sh vlan br")
    #var10 = connection2.send_command("sh cdp nei")
    #var11 = connection2.send_command("sh vlan br")
    var12 = connection1.send_command("sh int trunk")
    #var13 = connection2.send_command("sh int trunk")
    seven = checkdownlinktrunkedvlans.downlinktrunkedvlans(var8, var9, switch)[0]
    if var10 == '' or var11 == '':
        ten = ''
    else:
        ten = checkdownlinktrunkedvlans.downlinktrunkedvlans(var10, var11, switch)[0]
    
    var14 = checkvlansiftrunked.vlansiftrunked(var9, var12, list1[0])
    
    if var11 == '' or var13 == '':
        var15 = ''
    else:
        var15 = checkvlansiftrunked.vlansiftrunked(var11, var13, list1[1])
        
    #print(var15)
        
    downlink_port1 = checkdownlinktrunkedvlans.downlinktrunkedvlans(var8, var9, switch)[1]
    #print(downlink_port1)
    if var10 == '' or var11 == '':
        downlink_port2 = ''
    else:
        downlink_port2 = checkdownlinktrunkedvlans.downlinktrunkedvlans(var10, var11, switch)[1]
    
    #print("Here is var14:\n", var14)
    #print("here is downlink port1: ",downlink_port1[0])
    eight = ''
    for i in range(len(var14)):
        for m,n in var14[i].items():
            if downlink_port1[0] in n:
                if downlink_port1[0] == n.split(":")[0]:
                    eight = n.split(":")[-1]
    #print("Here is eight", eight)
    
    #print("Here is var15:\n", var15)   
    #print("here is downlink port2: ",downlink_port2[0])         
    eleven = ''
    if downlink_port2 == '':
        eleven = ''
    else:
        for i in range(len(var15)):
            for m,n in var15[i].items():
                if downlink_port2[0] in n:
                    if downlink_port2[0] == n.split(":")[0]:
                        eleven = n.split(":")[-1]
    #print("Here is eleven", eleven)        
    
    eightt = vlansconverter.converter(str(eight), seven)
    elevenn = vlansconverter.converter(str(eleven), ten)
    
    twelve=''
    if(set(three).issubset(set(seven)) and set(three).issubset(set(ten))):
        twelve = 'no'
    else: twelve = 'yes'
    
    var16 = [x for x in two if x in three and x in fivee and x in fourr and x in seven \
             and x in eightt and x in ten and x in elevenn]
    
    thirteen = ''
    if(all(x in var16 for x in two)):
        thirteen='no'
    else: thirteen='yes'
    
    
    with open("output.csv", "a", newline='') as filetypeobject:
        header = h
        dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
        dictwritertypeobject.writerow({h[0]: switch , h[1]:one, h[2]:two, h[3]:three, h[4]:fourr,\
                                       h[5]:fivee, h[6]:six, h[7]:seven, h[8]:eightt, h[9]:nine, \
                                           h[10]:ten, h[11]:elevenn, h[12]:twelve, h[13]:thirteen})
        connection.disconnect()
        
        """
        print(one, '\n', two, '\n', three, '\n', fourr, '\n', fivee, '\n', six, '\n', seven, \
              '\n', eightt, '\n', nine, '\n', ten, '\n', elevenn, '\n', twelve, '\n', thirteen)
        
        
        """
    """
    except:
        print(f"Didnt Happen for {switch}")
        with open("unconnectables.csv", "a", newline='') as filetypeobject:
            header = ["switchname"]
            dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
            dictwritertypeobject.writerow({'switchname': switch})
            connection.disconnect()
        
    """
    
    """    
def reachability(switchlist):        
    global connection
    for switch in switchlist:
        try:
            kwargs = {
                'device_type': 'cisco_ios','ip': switch,'username': '************','password': '***********', 'port': '22'
                }
            connection = ConnectHandler(**kwargs)
            work(connection, switch)                        
        except:
            try:
                kwargs = {
                    'device_type': 'cisco_ios_telnet','ip': switch,'username': '**********','password': '*********', 'port': '23'
                    }
                connection = ConnectHandler(**kwargs)
                work(connection, switch)
            except:
                print("AIN'T HAPPENING FOR", switch)
                with open("unconnectables.csv", "a", newline='') as filetypeobject:
                    header = ["switchname"]
                    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
                    dictwritertypeobject.writerow({'switchname': switch})
                    connection.disconnect()
    """
                
with open("input.csv", "r") as filetypeobject:
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
            'device_type': 'cisco_ios','ip': i,'username': '***********','password': '**********','port':'22'
            }
        connection = ConnectHandler(**kwargs)
    except:
        try:
            kwargs = {
                'device_type': 'cisco_ios_telnet','ip': i,'username': '*********','password': '***********','port':'23'
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

