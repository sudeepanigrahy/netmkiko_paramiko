import netmiko
from netmiko import ConnectHandler
import datetime
import difflib
import webbrowser

kwargs = {
    'device_type': 'cisco_ios',
    'ip': "*******",
    'username': '*******',
    'password': '*******',
    'port':'22'
    }

kwargs1 = {
    'device_type': 'cisco_ios',
    'ip': "*******",
    'username': '*******',
    'password': '*******',
    'port':'22'
    }

connection = ConnectHandler(**kwargs)

print(connection.find_prompt(),"\nConnected Successfully", "\n"*3)
running_config = connection.send_command("show run")

now = datetime.datetime.now().replace(microsecond=0)
conf_file = f"{now}_{kwargs['ip']}.txt"
#As windows doesn't allow ":" in a file's name, we'll replace it with a "."
current_conf_file = conf_file.replace(":", ".")

with open(current_conf_file, "w") as filetypeobject:
    filetypeobject.write(running_config)
    
##Below is the code for the config comparison using 'difflib' 
##and 'webbrowser' modules    
oldfiletypeobject = open("backup.txt")
old_content = oldfiletypeobject.readlines()
oldfiletypeobject.close

newfiletypeobject = open(current_conf_file)
new_content = newfiletypeobject.readlines()
newfiletypeobject.close()

"""
with open("backup.txt", "r") as oldfiletypeobject:
    old_content = oldfiletypeobject.readlines()
    
with open(current_conf_file, "r") as newfiletypeobject:
    new_content = newfiletypeobject.readlines()
"""

conf_compare = difflib.HtmlDiff().make_file(fromlines=old_content, tolines=new_content, 
                                            fromdesc="Backup Ref", todesc=f"Current {current_conf_file}")

with open("diff.html", "w") as difffiletypeobject:
    difffiletypeobject.write(conf_compare)

webbrowser.open_new_tab("diff.html")
