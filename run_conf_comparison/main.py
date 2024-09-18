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
global path_compare_txt_files
global path_counts
path_txt_files = r"c:\Users\*******\Documents\automata\netmiko_paramiko\compare_configs_chrome\run_conf_comparison\data\config_text_files"
path_csv_files=r"c:\Users\*******\Documents\automata\netmiko_paramiko\compare_configs_chrome\run_conf_comparison\data\compare_csv_files"
path_compare_txt_files=r"c:\Users\*******\Documents\automata\netmiko_paramiko\compare_configs_chrome\run_conf_comparison\data\compare_text_files"
path_counts = r"c:\Users\*******\Documents\automata\netmiko_paramiko\compare_configs_chrome\run_conf_comparison\data\counts"

with open("no_login.csv", "w", newline='') as filetypeobject:
    header = ["switchname"]
    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
    dictwritertypeobject.writeheader()
    
with open(f"{path_counts}\counts.csv", "w", newline='') as filetypeobject1:
    header = ["pair", "no._of_lines"]
    dictwritertypeobject1 = csv.DictWriter(filetypeobject1, fieldnames = header)
    dictwritertypeobject1.writeheader()

def count_lines(final_sheet):
    final_sheet_with_path = f"{path_csv_files}\{final_sheet}"
    
    dtpo = pd.ExcelFile(final_sheet_with_path)
    sheets = dtpo.sheet_names
    df = dtpo.parse(sheets[0])
    dimensions = df.shape
    
    with open(f"{path_counts}\counts.csv", "a", newline='') as filetypeobject1:
        header = ["pair", "no._of_lines"]
        dictwritertypeobject = csv.DictWriter(filetypeobject1, fieldnames = header)
        dictwritertypeobject.writerow({'pair': final_sheet,'no._of_lines': dimensions[0]})
        
    return dimensions
    
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
            x = len(right)-len(left)
            for i in range(x):
                left.append("...")


    data = {f"missing_on_{switch2}": left, f"missing_on_{switch1}": right }
    df = DataFrame(data)

    writer = pd.ExcelWriter(f'{path_csv_files}\Compared_{switch1}_{switch2}.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    
    return [f"Compare_Configs_for_{switch1}_{switch2}_Completed...", f"Compared_{switch1}_{switch2}.xlsx"]
    

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
                    'device_type': 'cisco_ios','ip': switch,'username': '*********','password': '*********','port':'22'
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
                        'device_type': 'cisco_ios_telnet','ip': switch,'username': '*********','password': '*********','port':'23'
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
                            'device_type': 'cisco_nxos','ip': switch,'username': '*********','password': '*********','port':'22'
                            }
                        connection = ConnectHandler(**kwargs)
                        baseline = connection.send_command('show run')
                        with open(f"{path_txt_files}\{switch}.txt", "w") as filetypeobject:
                            filetypeobject.write(baseline)
                            filetypeobject.close()
                        continue
                
                    except NetMikoAuthenticationException:
                        kwargs = {
                            'device_type': 'arista_eos','ip': switch,'username': '*********','password': '*********','port':'22'
                            }
                        connection = ConnectHandler(**kwargs)
                        baseline = connection.send_command('show run')
                        with open(f"{path_txt_files}\{switch}.txt", "w") as filetypeobject:
                            filetypeobject.write(baseline)
                            filetypeobject.close()
                        continue
                
                    except:
                        print("\n")
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
                    'device_type': 'cisco_ios','ip': switch,'username': '*********','password': '*********','port':'22'
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
                        'device_type': 'cisco_ios_telnet','ip': switch,'username': '*********','password': '*********','port':'23'
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
                            'device_type': 'cisco_nxos','ip': switch,'username': '*********','password': '*********','port':'22'
                            }
                        connection = ConnectHandler(**kwargs)
                        comparison = connection.send_command('show run')
                        with open(f"{path_txt_files}\{switch}.txt", "w") as filetypeobject:
                            filetypeobject.write(comparison)
                            filetypeobject.close()
                        continue
                
                    except NetMikoAuthenticationException:
                        kwargs = {
                            'device_type': 'arista_eos','ip': switch,'username': '*********','password': '*********','port':'22'
                            }
                        connection = ConnectHandler(**kwargs)
                        comparison = connection.send_command('show run')
                        with open(f"{path_txt_files}\{switch}.txt", "w") as filetypeobject:
                            filetypeobject.write(comparison)
                            filetypeobject.close()
                        continue
                
                    except:
                        print("\n")
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
    j = 0
    dict_of_lists={}
    for i in range(0,int(len(switchlist)/2)):
        dict_of_lists[i] = [switchlist[j]]
        dict_of_lists[i].append(switchlist[j+1])
        j = j + 2
    return dict_of_lists
                
with open("input.csv", "r") as filetypeobject:
    header = ["switchname"]
    dictreadertypeobject = csv.DictReader(filetypeobject, fieldnames = header)
    inputswitchlist = []
    for i in dictreadertypeobject:
        inputswitchlist.append(i["switchname"])
    inputswitchlist.pop(0)
    dict = pairing(inputswitchlist)                

    for p,q in dict.items():
        try:
            x, f, g = pre_work(q)
            y = post_work(f"{path_compare_txt_files}\{x}", f, g)
            print("\n" + y[0])
            shape = count_lines(y[1])
            print("rows:", int(shape[0])-1)
        except OSError:
            print("\n")
            print(sys.exc_info()[0], " ", f"Please shorten the hostnames of {q}, which combined is possibly greater than 255 characters allowed in windows filesystem.", "\n")
            continue
        except Exception as e:
            print("\n")
            print(e)
        except:
            print(sys.exc_info()[0])

               
