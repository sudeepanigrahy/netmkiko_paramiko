import sys
from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoAuthenticationException
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import SSHException

def reachability(device):
    global connection
    try:
        kwargs = {
            'device_type': 'cisco_ios','ip': device,'username': '********','password': '********','port':'22'
            }
        connection = ConnectHandler(**kwargs)
        
    except:
        try:
            kwargs = {
                'device_type': 'cisco_ios_telnet','ip': device,'username': '********','password': '********','port':'23'
                }
            connection = ConnectHandler(**kwargs)
        except:    
            try:
                kwargs = {
                    'device_type': 'arista_eos','ip': device,'username': '********','password': '********','port':'22'
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
                print("Exception Occurred:", sys.exc_info()[0])
                print("")
    
    return connection

if __name__=='__main__':
    print("Good Day !!")
