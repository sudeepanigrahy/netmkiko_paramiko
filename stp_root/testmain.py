from netmiko import ConnectHandler
from paramiko.ssh_exception import SSHException
from netmiko.exceptions import NetMikoTimeoutException
import csv
import sys
import checkvlansrootport
from netmiko.exceptions import NetMikoAuthenticationException
import threading
import pandas as pd
import numpy as np



global h
h = ['AS Hostname', 'Spanning-tree Root', 'Root_port', 'Secondary_Root_Port', 'comments']

def work(connection, switch, t):
    
    var5 = connection.send_command("sh cdp nei")
    var6 = connection.send_command("sh spanning-tree root")
    
    incoming_data = checkvlansrootport.vlansrootport(var5, var6, switch)
    zero = incoming_data[0]
    one = incoming_data[1]
    two = incoming_data[2] 
    three = incoming_data[5]
    
    with open(f"output{t}.csv", "a", newline='') as filetypeobject:
        header = h
        dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
        dictwritertypeobject.writerow({h[0]: switch , h[1]: zero, h[2]: one, h[3]: two, h[4]: three })
        connection.disconnect()
        
       

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
                'device_type': 'cisco_ios','ip': i,'username': '***********','password': '***********','port':'22'
                }
            connection = ConnectHandler(**kwargs)
        except:
            try:
                kwargs = {
                    'device_type': 'cisco_ios_telnet','ip': i,'username': '***********','password': '***********','port':'23'
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
