import netmiko
from netmiko import ConnectHandler
import datetime
import difflib
import webbrowser
import sys
from netmiko.exceptions import NetMikoAuthenticationException
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import SSHException
import threading


kwargs = {
    'device_type': 'cisco_ios',
    'ip': "sg209-b1rm5x-as6-cn240",
    'username': 'spanigrahy',
    'password': 'Sueme@0124',
    'port':'22'
    }

kwargs1 = {
    'device_type': 'cisco_ios',
    'ip': "sg209-b1mr5y-as4-cn",
    'username': 'spanigrahy',
    'password': 'Sueme@0124',
    'port':'22'
    }

kwargs2 = {
    'device_type': 'cisco_ios',
    'ip': "ssg209-b1mr5y-as3-cn",
    'username': 'spanigrahy',
    'password': 'Sueme@0124',
    'port':'22'
    }

kwargs3 = {
    'device_type': 'cisco_ios',
    'ip': "sg209-b1rm2w-as22-cn188",
    'username': 'spanigrahy',
    'password': 'Sueme@0124',
    'port':'22'
    }

switch_list = [kwargs, kwargs1, kwargs2, kwargs3]

def cisco_backup(device):
    
    now = datetime.datetime.now()
    print("Connecting to the device", f"{device['ip']} at {now}")
    
    try:
        connection = ConnectHandler(**device)
        
        print("Connected successfully to the device ", f"{device['ip']}")
        print(f"{device['ip']} prompt is: {connection.find_prompt()}")
        print(f"Executing 'show run' for the device {device['ip']}")
        running_config = connection.send_command("show run")
        
        now = datetime.datetime.now().replace(microsecond=0)
        conf_file = f"{now}_{device['ip']}.txt"
        #As windows doesn't allow ":" in a file's name, we'll replace it with a "."
        current_conf_file = conf_file.replace(":", ".")
        print(f"Saving the output to file: {current_conf_file} \n")
        with open(current_conf_file, "w") as filetypeobject:
            filetypeobject.write(running_config)
            
        
    
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

loop_thread_list = list()
for switch in switch_list:
    loop_thread = threading.Thread(target=cisco_backup, args=(switch,))
    loop_thread.start()
    loop_thread_list.append(loop_thread)

for i in loop_thread_list:
    print(i)

for thread in loop_thread_list:
    thread.join()
    

print("Finished execution of the script")

for i in loop_thread_list:
    print(i)
"""
t1 = threading.Thread(target=cisco_backup, args=(kwargs,))
t2 = threading.Thread(target=cisco_backup, args=(kwargs1,))
t1.start()
t2.start()
t1.join()
t2.join()
"""
