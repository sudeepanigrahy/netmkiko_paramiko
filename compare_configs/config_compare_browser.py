import netmiko
from netmiko import ConnectHandler
import datetime
import sys
import difflib
import webbrowser
from netmiko.exceptions import NetmikoAuthenticationException
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import SSHException
import threading

kwargs1 = {
    'device_type': 'cisco_ios',
    'ip': "************",
    'username': "*******",
    'password': "********",
    'port': 22
}

kwargs2 = {
    'device_type': 'cisco_ios',
    'ip': "************",
    'username': "*******",
    'password': "********",
    'port': 22
}

try:
    connection1 = ConnectHandler(**kwargs1)
    connection2 = ConnectHandler(**kwargs2)
    cons = {connection1:kwargs1, connection2:kwargs2}
    comp_files=[]

    for i,j in cons.items():              
        print(i.find_prompt(), "\nConnected Successfully", "\n"*3)
        running_config = i.send_command("show run")

        now = datetime.datetime.now().replace(microsecond=0)
        conf_file = f"{now}_{j['ip']}.txt"
        #As windows doesn't allow ":" in a file's name, we'll replace it with a "."
        current_conf_file = conf_file.replace(":", ".")
        print(f"Saving the output to file: {current_conf_file} \n")
        
        with open(current_conf_file, "w") as filetypeobject:
            filetypeobject.write(running_config)
        comp_files.append(current_conf_file)

    #Below is the code for the config comparison using difflib_module,
    #and webbrowser_module.
    oldfiletypeobject = open(comp_files[0])
    old_content = oldfiletypeobject.readlines()
    oldfiletypeobject.close()

    newfiletypeobject = open(comp_files[1])
    new_content = newfiletypeobject.readlines()
    newfiletypeobject.close()

    conf_compare = difflib.HtmlDiff().make_file(fromlines=old_content, tolines=new_content,
                                                fromdesc=comp_files[0], todesc=f"Current {comp_files[1]}")
    
    with open("diff.html", "w") as difffiletypeobject:
            difffiletypeobject.write(conf_compare)

    webbrowser.open_new_tab("diff.html")

except NetmikoAuthenticationException:
        print(sys.exc_info()[0])
        print("Authentication Failed")

except NetMikoTimeoutException:
    print(sys.exc_info()[0])
    print("Timeout Exception, so possibly wrong hostname")

except SSHException:
    print(sys.exc_info()[0])
    print("Something wromng with the ssh connection")

except:
    print(sys.exc_info()[0])
    print("Exception Occurred")

##When you have multiple 'except' blocks in your code, then except for the 
##last 'except' block, for all the other 'except' blocks you gotta specify 
##exactly what its supposed to catch.