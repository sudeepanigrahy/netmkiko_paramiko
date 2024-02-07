import netmiko
from netmiko import ConnectHandler
import datetime
import difflib
import webbrowser
import sys
from netmiko.exceptions import NetMikoAuthenticationException
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import SSHException

"""
switch1 = input("Enter the first switch's name, without the domain")
switch2 = input("Enter the second switch's name, without the domain")
"""

kwargs1 = {
    'device_type': 'cisco_ios',
    'ip': "**********",
    'username': '**********',
    'password': '**********',
    'port':'22'
    }

kwargs2 = {
    'device_type': 'cisco_ios',
    'ip': "**********",
    'username': '**********',
    'password': '**********',
    'port':'22'
    }

try:
    connection1 = ConnectHandler(**kwargs1)
    connection2 = ConnectHandler(**kwargs2)
    cons = {connection1:kwargs1, connection2:kwargs2}
    comp_files=[]
    for i,j in cons.items():
        print(i.find_prompt(),"\nConnected Successfully", "\n"*3)
        i.send_command("term len 0")
        running_config = i.send_command("show run")
        
        now = datetime.datetime.now().replace(microsecond=0)
        conf_file = f"{now}_{j['ip']}.txt"
        #As windows doesn't allow ":" in a file's name, we'll replace it with a "."
        current_conf_file = conf_file.replace(":", ".")
        
        with open(current_conf_file, "w") as filetypeobject:
            filetypeobject.write(running_config)
        
        comp_files.append(current_conf_file)
        
    ##Below is the code for the config comparison using 'difflib' 
    ##and 'webbrowser' modules    
    oldfiletypeobject = open(comp_files[0])
    old_content = oldfiletypeobject.readlines()
    oldfiletypeobject.close
    
    newfiletypeobject = open(comp_files[1])
    new_content = newfiletypeobject.readlines()
    newfiletypeobject.close()
    
    """
    with open("backup.txt", "r") as oldfiletypeobject:
        old_content = oldfiletypeobject.readlines()
        
    with open(current_conf_file, "r") as newfiletypeobject:
        new_content = newfiletypeobject.readlines()
    """
    
    conf_compare = difflib.HtmlDiff().make_file(fromlines=old_content, tolines=new_content, 
                                                fromdesc=comp_files[0], todesc=f"Current {comp_files[1]}")
    
    with open("diff.html", "w") as difffiletypeobject:
        difffiletypeobject.write(conf_compare)
    
    webbrowser.open_new_tab("diff.html")

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
