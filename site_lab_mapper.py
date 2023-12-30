"""
Script for mapping out the lab of a site
"""

from netmiko import ConnectHandler
from paramiko.ssh_exception import SSHException
from netmiko import NetmikoTimeoutException
import csv
import sys
import re
import datetime
import time
from netmiko.exceptions import NetMikoAuthenticationException
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import SSHException


cs1 = input("Please enter the first core:")
cs2 = input("Please enter the second core:")
cores = [cs1, cs2]

def neighbor_ds_finder(connection, switch):
    cdp_output = connection.send_command("sh cdp neigh")
    cdp_output_lines = cdp_output.splitlines()
    ds_switches = []
    for line in cdp_output_lines:
        if "ds" in line:
            cdp_output_line_list = line.split()
            ds_switches.append(cdp_output_line_list[0])
    print(f"\nBELOW ARE THE DS SWITCHES FROM '{switch.upper()}':\n{ds_switches}")
    neighbor_as_ds_finder(ds_switches)
    print(110*"=")

def neighbor_as_ds_finder(ds_switches):
    
    def as_from_ds_finder(con, switch):
        as_switches = []
        ds_from_ds_switches = []
        cdp_outputt = con.send_command("sh cdp neigh")
        cdp_output_liness = cdp_outputt.splitlines()
        for line in cdp_output_liness:
            if "as" in line:
                cdp_output_line_listt = line.split()
                as_switches.append(cdp_output_line_listt[0])
            elif "ds" in line:
                listt = line.split()
                ds_from_ds_switches.append(listt[0])
            else:
                pass
        print(f"\nBelow are the as switches connected to '{switch}':\n{as_switches}\n")
        print(f"Below are the ds switches connected to '{switch}':\n{ds_from_ds_switches}\n")
        
        if len(ds_from_ds_switches) != 0:
            neighbor_as_from_ds_from_ds_finder(ds_from_ds_switches)
    
    for switch in ds_switches:
        global con
        try:
            kwargs = {
                    'device_type': 'cisco_ios','ip': switch,'username': '*********','password': '*********','port':'22'
                    }
            con = ConnectHandler(**kwargs)
            
            as_from_ds_finder(con, switch)                        
        except:
            try:
                kwargs = {
                        'device_type': 'cisco_ios','ip': switch,'username': '*********','password': '*********','port':'23'
                        }
                con = ConnectHandler(**kwargs)
                as_from_ds_finder(con, switch)
            except:
                print("AIN'T HAPPENING FOR", switch)
                print(sys.exc_info()[0])
        

def neighbor_as_from_ds_from_ds_finder(ds_from_ds_switches):
    
    def as_from_ds_from_ds_finder(conn, switch):
        as_switches = []
        cdp_outputtt = conn.send_command("sh cdp neigh")
        cdp_output_linesss = cdp_outputtt.splitlines()
        for line in cdp_output_linesss:
            if "as" in line:
                as_switches.append(line.split()[0])
            else:
                pass
        
        print(f"Below are the AS Switches connected to '{switch}':\n{as_switches}\n")
        
        
    
    for switch in ds_from_ds_switches:
        global conn
        try:
            kwargs = {
                    'device_type': 'cisco_ios','ip': switch,'username': '*********','password': '*********','port':'22'
                    }
            conn = ConnectHandler(**kwargs)
            
            as_from_ds_from_ds_finder(conn, switch)                        
        except:
            try:
                kwargs = {
                        'device_type': 'cisco_ios','ip': switch,'username': '*********','password': '*********','port':'23'
                        }
                conn = ConnectHandler(**kwargs)
                as_from_ds_from_ds_finder(conn, switch)
            except:
                print("AIN'T HAPPENING FOR", switch)
                print(sys.exc_info()[0])
        
    
        
for switch in cores:
    global connection
    try:
        kwargs = {
                'device_type': 'cisco_ios','ip': switch,'username': '*********','password': '*********','port':'22'
                }
        connection = ConnectHandler(**kwargs)
        neighbor_ds_finder(connection, switch)                        
    except:
        try:
            kwargs = {
                    'device_type': 'cisco_ios','ip': switch,'username': '*********','password': '*********','port':'23'
                    }
            connection = ConnectHandler(**kwargs)
            neighbor_ds_finder(connection, switch)
        except:
            print("AIN'T HAPPENING FOR", switch)
            print(sys.exc_info()[0])
