import netmiko
from ScriptConstants import *

class QueryHandler:

    def __init__(self, i_target_ip, i_device_type):
        self._device_type = i_device_type
        
        if(i_device_type is DeviceType.CISCO_IOS): 
            self._command_set = CISCO_IOS_COMMAND_SET
            self._default_device_profile = {
                'device_type': 'cisco_ios',
                'host': str(i_target_ip),
                'username': 'nwtools',
                'password': '!1Jst4Tls7!'
            }
            self._telnet_device_profile = {
                'device_type': 'cisco_ios_telnet',
                'host': str(i_target_ip),
                'username': 'nwtools',
                'password': '!1Jst4Tls7!'
            }
        
        elif(i_device_type is DeviceType.CISCO_NXOS): 
            self._command_set = CISCO_NXOS_COMMAND_SET
            self._default_device_profile = {
                'device_type': 'cisco_nxos',
                'host': str(i_target_ip),
                'username': 'nwtools',
                'password': '!1Jst4Tls7!'
            }
            self._telnet_device_profile = {
                'device_type': 'cisco_ios_telnet',
                'host': str(i_target_ip),
                'username': 'nwtools',
                'password': '!1Jst4Tls7!'
            }
        
        elif(i_device_type is DeviceType.ARISTA_EOS): 
            self._command_set = ARISTA_EOS_COMMAND_SET
            self._default_device_profile = {
                'device_type': 'arista_eos',
                'host' : str(i_target_ip),
                'username' : "nwtools",
                'password' : "!1Jst4Tls7!"
            }
            self._telnet_device_profile = {
                'device_type': 'arista_eos_telnet',
                'host': str(i_target_ip),
                'username': 'nwtools',
                'password': '!1Jst4Tls7!'
            }
        
        else:
            self._command_set = CISCO_IOS_COMMAND_SET
            self._default_device_profile = {
                'device_type': 'autodetect',
                'host': str(i_target_ip),
                'username': 'nwtools',
                'password': '!1Jst4Tls7!'
            }
            self._telnet_device_profile = {
                'device_type': 'cisco_ios_telnet',
                'host': str(i_target_ip),
                'username': 'nwtools',
                'password': '!1Jst4Tls7!'
            }

        self._host = str(i_target_ip)

        self._show_int = ''
        self._show_int_status = ''
        self._show_neighbour = ''
        self._show_running_config = ''
        self._show_startup_config = ''
        self._show_spanning_tree = ''
        self._show_spanning_tree_root= ''
        self._show_process_memory = ''
        self._show_version = ''
        self._show_power_inline = ''
        self._show_platform_resources = ''
        self._show_total_memory = ''
        self._show_kernel_memory = '' 
        self._show_vlan_br = ''
        self._show_int_trunk = ''

        self._is_ready = False

        try:
            self._handler_object = netmiko.ConnectHandler(**self._default_device_profile)
            self._is_ready = True

        except Exception as err:

            try:                
                self._handler_object = netmiko.ConnectHandler(**self._telnet_device_profile)
                self._is_ready = True
            
            except Exception as err_2:
                print("<ALERT>: " + str(i_target_ip) + " encounters an error, telnet failed: " + str(err_2))

    def execute_command(self, i_string):
        try:
            if(self._is_ready):
                outstr = self._handler_object.send_command(i_string, read_timeout=30)
                return outstr
        except Exception as err:
            print("<ALERT>: " + str(self._host) + " encounters an error, failed to execute command: " + str(err))
            return 'err'

    def disconnect(self):
        self._handler_object.disconnect()
        self._is_ready = False
        return

    def get_show_int(self):
        if(self._show_int != '' and self._show_int != 'ERROR'): return self._show_platform_resources        
        try:
            self._show_int = self._handler_object.send_command(self._command_set['show_int'], read_timeout = 30)
            return self._show_int
        except Exception as err:
            print("<ALERT>: " + str(self._host) + " encounters an error, show int failed: " + str(err))
            self._show_int = 'ERROR'
            return self._show_int

    def get_show_int_status(self):
        if(self._show_int_status != '' and self._show_int_status != 'ERROR'): return self._show_int_status      
        try:
            self._show_int_status = self._handler_object.send_command(self._command_set['show_int_status'], read_timeout = 30)
            return self._show_int_status
        except Exception as err:
            print("<ALERT>: " + str(self._host) + " encounters an error, show int status failed: " + str(err))
            self._show_int_status = 'ERROR'
            return self._show_int_status

    def get_show_running_config(self):
        if(self._show_running_config != '' and self._show_running_config != 'ERROR'): return self._show_running_config        
        try:
            self._show_running_config = self._handler_object.send_command(self._command_set['show_running_config'], read_timeout = 30)
            return self._show_running_config
        except Exception as err:
            print("<ALERT>: " + str(self._host) + " encounters an error, show int failed: " + str(err))
            self._show_running_config = 'ERROR'
            return self._show_running_config            
        
    def get_show_version(self):
        if(self._show_version != '' and self._show_version != 'ERROR'): return self._show_version        
        try:
            self._show_version = self._handler_object.send_command(self._command_set['show_version'], read_timeout = 30)
            return self._show_version
        except Exception as err:
            print("<ALERT>: " + str(self._host) + " encounters an error, show int failed: " + str(err))
            self._show_version = 'ERROR'
            return self._show_version            
        

    def get_show_spanning_tree_root(self):
        if(self._show_spanning_tree_root != '' and self._show_spanning_tree_root != 'ERROR'): return self._show_spanning_tree_root        
        try:
            self._show_spanning_tree_root = self._handler_object.send_command(self._command_set['show_spanning_tree_root'], read_timeout = 30)
            return self._show_spanning_tree_root
        except Exception as err:
            print("<ALERT>: " + str(self._host) + " encounters an error, show spanning-tree root failed: " + str(err))
            self._show_spanning_tree_root = 'ERROR'
            return self._show_spanning_tree_root 

    def get_show_neighbour(self):
        if(self._show_neighbour != '' and self._show_neighbour != 'ERROR'): return self._show_neighbour        
        try:
            self._show_neighbour = self._handler_object.send_command(self._command_set['show_neighbour'], read_timeout = 30)
            return self._show_neighbour
        except Exception as err:
            print("<ALERT>: " + str(self._host) + " encounters an error, show neighbour failed: " + str(err))
            self._show_neighbour = 'ERROR'
            return self._show_neighbour 
        
    def get_show_vlan_br(self):
        if(self._show_vlan_br != '' and self._show_vlan_br != 'ERROR'): return self._show_vlan_br        
        try:
            self._show_vlan_br = self._handler_object.send_command(self._command_set['show_vlan_br'], read_timeout = 30)
            return self._show_vlan_br
        except Exception as err:
            print("<ALERT>: " + str(self._host) + " encounters an error, show neighbour failed: " + str(err))
            self._show_vlan_br = 'ERROR'
            return self._show_vlan_br     

    def get_show_int_trunk(self):
        if(self._show_int_trunk != '' and self._show_int_trunk != 'ERROR'): return self._show_int_trunk       
        try:
            self._show_int_trunk = self._handler_object.send_command(self._command_set['show_int_trunk'], read_timeout = 30)
            return self._show_int_trunk
        except Exception as err:
            print("<ALERT>: " + str(self._host) + " encounters an error, show neighbour failed: " + str(err))
            self._show_int_trunk = 'ERROR'
            return self._show_int_trunk    
       