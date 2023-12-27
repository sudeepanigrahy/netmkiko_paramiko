from netmiko import ConnectHandler
import csv


#This code is for testing and seeing if switches of one particular model type have same OSs or not
x = []
with open("testing.csv", "r") as filetypeobject:
    header = ["switchname"]
    dictreadertypeobject = csv.DictReader(filetypeobject, fieldnames = header)
    
    for i in dictreadertypeobject:
        x.append(i["switchname"]) 
        
#print(x)
        
for i in x:
    s = i
    try:
        kwargs = {
            'device_type': 'cisco_ios','ip': s,'username': 'spanigrahy','password': 'Sueme@0124','port':'22'
            }
        connection = ConnectHandler(**kwargs)
        
        y = connection.send_command("show version")
        z = y.splitlines()
        print(z[0])
    except:
        try:
            kwargs = {
                'device_type': 'cisco_ios','ip': s,'username': 'spanigrahy','password': 'Sueme@0124','port':'23'
                }
            connection = ConnectHandler(**kwargs)
            
            y = connection.send_command("show version")
            z = y.splitlines()
            print(z[0])
        except:
            if s == "switchname":
                print("This is just a header !!")
            else:
                print(s, "ain't letting me in")
            
        
        
"""
x = ConnectHandler(**kwargs)

y = x.send_command("show version")


if "Cisco IOS Software" in y and "System Serial Number" not in y:
    print("only IOS")
elif "Cisco IOS XE Software" and "System Serial Number" in y:
    print("IOS XE")
elif "Cisco IOS Software, IOS-XE Software" in y:
    if "Processor board ID" in y and "System Serial Number" not in y:
        print("IOS and IOS XE: Variety 1")
    elif "System Serial Number" in y:
        print("IOS and IOS XE: Variety 2")
    else:
        print("some other variety")
else:
    print("lol")
"""

