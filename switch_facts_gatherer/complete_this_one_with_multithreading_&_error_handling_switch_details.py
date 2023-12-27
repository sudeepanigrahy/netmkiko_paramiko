from netmiko import ConnectHandler
from paramiko.ssh_exception import SSHException
from netmiko import NetmikoTimeoutException
import csv
import sys
import re
import datetime
import time

global h

with open("outputdatafile_sg.csv", "w", newline='') as filetypeobject:
    header = ["switchname", "version", "serial", "model", "uptime"]
    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
    dictwritertypeobject.writeheader()

with open("unconnectables_sg.csv", "w", newline='') as filetypeobject:
    header = ["switchname"]
    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
    dictwritertypeobject.writeheader()

def ios(connection, switch, version, up):  
    ver = version
    uptime = up
    
    fetch_model = connection.send_command("show version | i Model number")
    list_model = fetch_model.split()
    model = list_model[3]

    fetch_serial = connection.send_command("show version | i System serial number")
    list_serial = fetch_serial.split()
    serial = list_serial[4]
        
    with open("outputdatafile_sg.csv", "a", newline='') as filetypeobject:
        header = ["switchname", "version", "serial", "model", "uptime"]
        dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
        dictwritertypeobject.writerow({'switchname': switch , 'version': ver, 'serial': serial, 'model': model, 'uptime':uptime})
        connection.disconnect()
        
    
def iosxe(connection, switch, version, up):
    ver = version
    uptime = up

    fetch_model = connection.send_command("show version | i Model Number")
    list_model = fetch_model.split()
    model = list_model[3]

    fetch_serial = connection.send_command("show version | i System Serial Number")
    list_serial = fetch_serial.split()
    serial = list_serial[4]  
    
    with open("outputdatafile_sg.csv", "a", newline='') as filetypeobject:
        header = ["switchname", "version", "serial", "model", "uptime"]
        dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
        dictwritertypeobject.writerow({'switchname': switch , 'version': ver, 'serial': serial, 'model': model, 'uptime':uptime})
        connection.disconnect()


def iosandiosxe(connection, switch, variety, version, up):
    ver = version
    uptime = up
    
    if variety == 1:
        fetch_model = connection.send_command("show version | i physical memory")
        list_model = fetch_model.split()
        model = list_model[1]

        fetch_serial = connection.send_command("show version | i Processor board ID")
        list_serial = fetch_serial.split()
        serial = list_serial[3]
       
        with open("outputdatafile_sg.csv", "a", newline='') as filetypeobject:            
            header = ["switchname", "version", "serial", "model", "uptime"]
            dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)            
            dictwritertypeobject.writerow({'switchname': switch , 'version': ver, 'serial': serial, 'model': model, 'uptime':uptime})
            connection.disconnect()
       
    elif variety == 2:
        fetch_model = connection.send_command("show version | i Model Number")
        list_model = fetch_model.split()
        model = list_model[3]

        fetch_serial = connection.send_command("show version | i System Serial Number")
        list_serial = fetch_serial.split()
        serial = list_serial[4]
       
        with open("outputdatafile_sg.csv", "a", newline='') as filetypeobject:          
            header = ["switchname", "version", "serial", "model", "uptime"]
            dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)           
            dictwritertypeobject.writerow({'switchname': switch , 'version': ver, 'serial': serial, 'model': model, 'uptime':uptime})
            connection.disconnect()


def differentiator(connection, switch):
    
    fetch_version = connection.send_command("show version | i Version")
    list_version = fetch_version.splitlines()
    first_line = list_version[0]
    first_line_elements = first_line.split()

    for i in range(1, len(first_line_elements) + 1):
        if first_line_elements[i] == "Version":
            ver = first_line_elements[i+1]
            break
    version = ver.replace(",", "")
 
    s = connection.send_command("show version | i uptime")
    y = s.split()    
    x = {"years":"0","weeks":"0", "days":"0", "hours":"0", "minutes":"0"}   
        
    for i in range(4, len(y) + 1):
        
        if y[i-1] == "year," or y[i-1] == "years,":
            x["years"] = y[i-2]
            continue
        elif y[i-1] == "week," or y[i-1] == "weeks,":
            x["weeks"] = y[i-2]
            continue
        elif y[i-1] == "day," or y[i-1] == "days,":
            x["days"] = y[i-2]
            continue
        elif y[i-1] == "hour," or y[i-1] == "hours,":
            x["hours"] = y[i-2]
            continue
        elif y[i-1] == "minute" or y[i-1] == "minutes":
            x["minutes"] = y[i-2]
            continue	 	 
     
    w=(int(x["weeks"])*7)/365
    d=(int(x["days"])/365)
    h=(int(x["hours"])/(365*24))
    m=(int(x["minutes"])/(365*24*60))
    result=int(x["years"])+w+d+h+m
    up_time = "%0.6f"%result

    
    yy = connection.send_command("show version")
    if "Cisco IOS Software" in yy and "System serial number" in yy and "System Serial Number" not in yy:
        ios(connection, switch, version, up_time)       
    elif "Cisco IOS XE Software" in yy and "System Serial Number" in yy:
        iosxe(connection, switch, version, up_time)
    elif "Cisco IOS Software, IOS-XE Software" in yy:        
        if "Processor board ID" in yy and "System Serial Number" not in yy:
            iosandiosxe(connection, switch, 1, version, up_time)
        elif "System Serial Number" in yy and "Assembly" in yy:
            iosandiosxe(connection, switch, 2, version, up_time)
        else:
            print("THERE IS ANOTHER VARIETY FOR IOSANDIOS-XE", switch )
            #if there's another type of iosandios-xe, create logic for that
    else:
        print("THIS IS A NEW SOFTWARE",switch)
  


"""
def prework(csv_chunk, t):

    with open(f"output{t}.csv", "w", newline='') as filetypeobject:
        header = h
        dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
        dictwritertypeobject.writeheader()
        
    with open(f"unconnectables{t}.csv", "w", newline='') as filetypeobject:
        header = ["switchname"]
        dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
        dictwritertypeobject.writeheader()

    with open(f"check_again{t}.csv", "w", newline='') as filetypeobject:
        header = ["switchname"]
        dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
        dictwritertypeobject.writeheader()       
            
    with open(csv_chunk, "r") as filetypeobject:
        header = ["switchname"]
        dictreadertypeobject = csv.DictReader(filetypeobject, fieldnames = header)
        inputswitchlist = []
        for i in dictreadertypeobject:
            inputswitchlist.append(i["switchname"])
        inputswitchlist.pop(0)
    
        
    for i in inputswitchlist:
        print(f"working on {i}...")
        try:
            kwargs = {
                'device_type': 'cisco_ios','ip': i,'username': 'spanigrahy','password': 'Sueme@0128','port':'22'
                }
            connection = ConnectHandler(**kwargs)
        except:
            try:
                kwargs = {
                    'device_type': 'cisco_ios_telnet','ip': i,'username': 'spanigrahy','password': 'Sueme@0128','port':'23'
                    }
                connection = ConnectHandler(**kwargs)
                
            except NetMikoAuthenticationException:
                print(sys.exc_info()[0])
                print("Authentication Failed")
                
            except NetMikoTimeoutException:
                print(sys.exc_info()[0])
                print("Timeout Exception, so possibly wrong hostname")
            
            except SSHException:
                print(sys.exc_info()[0])
                print("Something wrong with the SSH Connection")
                    
            except:
                print("AIN'T HAPPENING FOR", i)
                print(sys.exc_info()[0])
                with open(f"unconnectables{t}.csv", "a", newline='') as filetypeobject:
                    header = ["switchname"]
                    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
                    dictwritertypeobject.writerow({'switchname': i})
                    connection.disconnect()
                continue
            
        try:
            work(connection, i, t)
        except:
            print(f"{i}: Need to check this switch again, its failing right now..")
            print(sys.exc_info()[0])
            print("Exception Occurred")
            with open(f"check_again{t}.csv", "a", newline='') as filetypeobject:
                header = ["switchname"]
                dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
                dictwritertypeobject.writerow({'switchname': i})
                connection.disconnect()


switches_df = pd.read_csv("switchlist.csv")
num_of_files = 5

#This'll create 5 small dataframe chunks out of one whole dataframe(i.e. out of the switches_df dataframe)
chunks = np.array_split(switches_df, num_of_files)

for i, chunk in enumerate(chunks):
    chunk.to_csv(f'chunk_{i}.csv', index=False)

chunks_list = []
for i in range(num_of_files):
    chunks_list.append(f"chunk_{i}.csv")

stp_root_thread_list = list()
for i, pile in enumerate(chunks_list):
    stp_root_thread = threading.Thread(target=prework, args=(pile, i))
    stp_root_thread.start()
    stp_root_thread_list.append(stp_root_thread)

for i in stp_root_thread_list:
    print(i)

for thread in stp_root_thread_list:
    thread.join()

list_of_DFs = []    
for i in range(num_of_files):
    list_of_DFs.append(pd.read_csv(f"output{i}.csv"))
final_DF = pd.concat(list_of_DFs, ignore_index=True)
final_DF.to_csv("NXA_STP_ROOT_AUDIT.csv")

list_of_DF1s = []    
for i in range(num_of_files):
    list_of_DF1s.append(pd.read_csv(f"unconnectables{i}.csv"))
final_DF1 = pd.concat(list_of_DF1s, ignore_index=True)
final_DF1.to_csv("UNCONNECTABLES.csv")

list_of_DF2s = []    
for i in range(num_of_files):
    list_of_DF2s.append(pd.read_csv(f"check_again{i}.csv"))
final_DF2 = pd.concat(list_of_DF2s, ignore_index=True)
final_DF2.to_csv("CHECK_AGAIN.csv")
"""

"""
def reachability(switchlist):        
    global connection
    for switch in switchlist:
        try:
            kwargs = {
                'device_type': 'cisco_ios','ip': switch,'username': 'spanigrahy','password': 'Sueme@0128','port':'22'
                }
            connection = ConnectHandler(**kwargs)
            differentiator(connection, switch)                        
        except:
            try:
                kwargs = {
                    'device_type': 'cisco_ios','ip': switch,'username': 'spanigrahy','password': 'Sueme@0128','port':'23'
                    }
                connection = ConnectHandler(**kwargs)
                differentiator(connection, switch)
            except:
                print("AIN'T HAPPENING FOR", switch)
                with open("unconnectables_sg.csv", "a", newline='') as filetypeobject:
                    header = ["switchname"]
                    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
                    dictwritertypeobject.writerow({'switchname': switch})
                    connection.disconnect()

                
with open("sg.csv", "r") as filetypeobject:
    header = ["switchname"]
    dictreadertypeobject = csv.DictReader(filetypeobject, fieldnames = header)
    inputswitchlist = []
    for i in dictreadertypeobject:
        inputswitchlist.append(i["switchname"])
    inputswitchlist.pop(0)
    reachability(inputswitchlist)
"""    