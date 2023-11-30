from netmiko import ConnectHandler
import sys
import csv
from netmiko.exceptions import NetMikoAuthenticationException 
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import SSHException
import diffios
import pandas as pd
from pandas import DataFrame

global path_txt_files
global path_csv_files
path_txt_files = r"c:\Users\*******\.spyder-py3\Saves\Python.N\Tasks\compare_configs_task\data\config_text_files"
path_csv_files = r"c:\Users\*******\.spyder-py3\Saves\Python.N\Tasks\compare_configs_task\data\compare_csv_files"
path_compare_txt_files = r"c:\Users\*******\.spyder-py3\Saves\Python.N\Tasks\compare_configs_task\data\compar_text_files"

with open("no_login.csv", "w", newline='') as filetypeobject:
    header = ["switchname"]   
    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)    
    dictwritertypeobject.writeheader()

def post_work(file, switch1, switch2):

    list1=[]
    left=[]
    right=[]
    with open(file, 'r') as textfiletypeobject: 
        data_string = textfiletypeobject.read() 
        list1 = data_string.splitlines()

        for i in list1:
            if i.startswith("-"): left.append(i) 
            elif i.startswith("+"): right.append(i)

    if len(left) != len(right):
        if len(left)>len(right):
            x = len(left)-len(right) 
            for i in range(x): 
                right.append("...")
        elif len(right)>len(left):
            x = len(right)-len (left) 
            for i in range(x):
                left.append("...")
    
    data = {f"missing_on_{switch2}": left, f"missing_on_{switch1}": right }
    df = DataFrame(data)

    writer = pd.ExcelWriter(f'{path_csv_files}\{switch1}_{switch2}.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()

    return f"Compare_Configs_for_{switch1}_{switch2}_Completed..."


def work(file1, file2):
    baseline = f"{path_txt_files}\{file1}"
    comparison = f"{path_txt_files}\{file2}" 
    ignore = "ignore.txt"
    
    diff = diffios.Compare(baseline, comparison, ignore)
    x = diff.delta()
    
    name = f"{file1}_{file2}"
    naam = name.replace(".txt", "")
    f = open(f"{path_compare_txt_files}\{naam}.txt", "w")
    f.write(x)
    f.close()
    return f"{naam}.txt"


def pre_work(pair):
    for e,switch in enumerate(pair):
        if e == 0:
            try:
                kwargs = {
                'device_type': 'cisco_ios', 'ip': switch, 'username': '*******', 'password': '**********', 'port':"22"
                }
                connection = ConnectHandler(**kwargs)
                baseline = connection.send_command('show run')
                with open(f"{path_txt_files}\{switch}.txt", "w") as filetypeobject:
                    filetypeobject.write(baseline)
                    filetypeobject.close()
                continue
            except:
                try:
                    kwargs = {
                    'device_type': 'cisco_ios_telnet', 'ip': switch, 'username': '*******', 'password': "*********", 'port':"23"
                    }
                    connection = ConnectHandler(**kwargs)
                    baseline = connection.send_command('show run')
                    with open(f"{path_txt_files}\{switch}.txt", "w") as filetypeobject:
                        filetypeobject.write(baseline)
                        filetypeobject.close()
                    continue

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
                    print(sys.exc_info()[0])
                    print("Exception Occurred")
                    print("Ain't Happening for: ", switch)
                    with open("no_login.csv", "a", newline='') as filetypeobject: 
                        header = ["switchname"]
                        dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
                        dictwritertypeobject.writerow({'switchname': switch})
                        connection.disconnect()

        elif e == 1:
            try:
                kwargs = {
                'device_type': 'cisco_ios', 'ip': switch, 'username': '*********', 'password': '********', 'port':'22'
                }
                connection = ConnectHandler(**kwargs)
                comparison = connection.send_command('show run')
                with open(f"{path_txt_files}\{switch}.txt", "w") as filetypeobject:
                    filetypeobject.write(comparison)
                    filetypeobject.close()
                continue
            except:
                try:
                    kwargs = {
                    'device_type': 'cisco_ios_telnet', 'ip': switch, 'username': 'spanigrahy', 'password': 'Sueme@0128', 'port':'23'
                    }
                    connection = ConnectHandler(**kwargs)
                    comparison = connection.send_command('show run')
                    with open(f" {path_txt_files}\{switch}.txt", "w") as filetypeobject:
                        filetypeobject.write(comparison)
                        filetypeobject.close()
                    continue

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
                    print(sys.exc_info()[0])
                    print("Exception Occurred")
                    print("Ain't Happening for: ", switch)
                    with open("no_login.csv", "a", newline='') as filetypeobject: 
                        header = ["switchname"]
                        dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
                        dictwritertypeobject.writerow({'switchname': switch})
                        connection.disconnect()

    done = work(f"{pair[0]}.txt", f"{pair[1]}.txt")
    return(done, pair[0], pair[1])

def pairing(switchlist):
    j=0
    dict_of_lists={}
    for i in range(0,int (len(switchlist)/2)): 
        dict_of_lists[i] = [switchlist[j]] 
        dict_of_lists[i].append(switchlist [j+1])
        j=j+2
    return dict_of_lists

with open("input2.csv", "r") as filetypeobject:
    header = ["switchname"]
    dictreadertypeobject = csv.DictReader(filetypeobject, fieldnames = header)
    inputswitchlist = []
    for i in dictreadertypeobject:
        inputswitchlist.append(i["switchname"])
    inputswitchlist.pop(0)
    dict = pairing(inputswitchlist)

    for p,q in dict.items():
        x, f, g = pre_work(q)
        y = post_work(f"{path_compare_txt_files}\{x}", f, g)
        print(y)            
