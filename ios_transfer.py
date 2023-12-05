from netmiko import ConnectHandler, file_transfer
from paramiko.ssh_exception import SSHException
from netmiko import NetmikoTimeoutException
import csv
import datetime
import time
from getpass import getpass

def pusher(connection, switch):
    #password = getpass()
    source_file = "cat9k_iosxe.17.03.04.SPA.bin"
    dest_file = "cat9k_iosxe.17.03.04.SPA.bin"
    direction = "put"
    file_system = "flash:"

    transfer_dict = file_transfer(
        connection,
        source_file = source_file,
        dest_file = dest_file,
        file_system=file_system,
        direction=direction,
        overwrite_file=True
    )

    print(transfer_dict)

def reachability(switchlist):
    global connection
    for switch in switchlist:
        try:
            kwargs = {
                'device_type': 'cisco_ios', 'ip': switch, 'username': '*******', 'password': '******', 'port': '22'
            }
        except:
            try:
                kwargs = {
                'device_type': 'cisco_ios', 'ip': switch, 'username': '*******', 'password': '******', 'port': '23'
            }
            except:
                print("Can't login through ssh or telnet", switch)
                with open("no_login_through_ssh_or_telnet.csv", "a", newline='') as filetypeobject:
                    header= ["switchname"]
                    dictwritertypeobject = csv.DictWriter(filetypeobject, fieldnames = header)
                    dictwritertypeobject.writerow({'switchname': switch})
                    connection.disconnect()

with open("input.csv", "r") as filetypeobject:
    header = ["switchname"]
    dictreadertypeobject = csv.DictReader(filetypeobject, fieldnames = header)
    inputswitchlist = []
    for i in dictreadertypeobject:
        inputswitchlist.append(i["switchname"])
    inputswitchlist.pop(0)
    reachability(inputswitchlist)

    