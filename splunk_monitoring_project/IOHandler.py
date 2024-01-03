import csv
from ScriptConstants import *
from datetime import datetime

# i_site_name = SiteName enum, predetermined values
class InputHandler:

    def __init__(self, i_input_path, i_site_name):
        
        self._input_path = i_input_path
        self._sitename = i_site_name
        self._accepted_ip_range = list()
        self._arista_device_list = list()
        self._nexus_device_list = list()
        self._cisco_device_list = list()

        if(i_site_name is SiteName.F10NXA): self._accepted_ip_range = ['10.193.', '10.194.', '10.195.']
        elif(i_site_name is SiteName.F10W): self._accepted_ip_range = ['172.25.', '172.28.']
        elif(i_site_name is SiteName.MSB): self._accepted_ip_range = ['10.160.', '10.198.']
        else:
            # logging placeholder 
            self._accepted_ip_range = ['None']
    
    def initialise_device_list(self):
        
        self._arista_device_list.clear()
        self._cisco_device_list.clear()
        self._nexus_device_list.clear()
        with open(self._input_path, mode='r') as i_csv:
            csv_reader = csv.reader(i_csv, delimiter=',')
            headers = next(csv_reader) # stripping out the first line
            
            for row in csv_reader:
                check_device = False
                device_name, device_ip, device_os = row[1], row[2], row[3]
                
                for ip in self._accepted_ip_range:
                    if(ip in device_ip): check_device = True
                
                if(not check_device):
                    continue

                if(device_os == 'EOS'): self._arista_device_list.append(device_name)
                elif(device_os == 'IOS' or device_os == 'XE-IOS'): self._cisco_device_list.append(device_name)
                elif(device_os == 'NXOS'): self._nexus_device_list.append(device_name)
                else: pass

    def get_cisco_device_list(self):
        return self._cisco_device_list
    
    def get_nexus_device_list(self):
        return self._nexus_device_list

class OutputHandler:
    def __init__(self, i_site_name, i_monitoring_parameter):
        self._site = i_site_name
        self._monitoring_parameter = i_monitoring_parameter
        if(i_site_name is SiteName.F10NXA):
            self._output_filepath_prefix = F10NXA_OUTPUT_FILEPATH
            self._working_filepath_prefix = F10NXA_WORKING_FILEPATH
        elif(i_site_name is SiteName.F10W):
            self._output_filepath_prefix = F10W_OUTPUT_FILEPATH
            self._working_filepath_prefix = F10W_WORKING_FILEPATH
        elif(i_site_name is SiteName.MSB):
            self._output_filepath_prefix = MSB_OUTPUT_FILEPATH
            self._working_filepath_prefix = MSB_WORKING_FILEPATH

        self._param_dict = {
            MonitoringParameter.BPDU : ((self._working_filepath_prefix + BPDU_CHECK_FILENAME), (self._output_filepath_prefix + BPDU_CHECK_FILENAME), BPDU_CHECK_FIELDS),
            MonitoringParameter.BROADCAST : ((self._working_filepath_prefix + BROADCAST_CHECK_FILENAME), (self._output_filepath_prefix + BROADCAST_CHECK_FILENAME), BROADCAST_CHECK_FIELDS),
            MonitoringParameter.CRC : ((self._working_filepath_prefix + CRC_CHECK_FILENAME), (self._output_filepath_prefix + CRC_CHECK_FILENAME), CRC_CHECK_FIELDS),
            MonitoringParameter.DISCONNECTED_PORTS : ((self._working_filepath_prefix + DISCONNECTED_PORTS_CHECK_FILENAME), (self._output_filepath_prefix + DISCONNECTED_PORTS_CHECK_FILENAME), DISCONNECTED_PORTS_CHECK_FIELDS),
            MonitoringParameter.KEEPALIVE : ((self._working_filepath_prefix + KEEPALIVE_CHECK_FILENAME), (self._output_filepath_prefix + KEEPALIVE_CHECK_FILENAME), KEEPALIVE_CHECK_FIELDS),
            MonitoringParameter.LOOPGUARD : ((self._working_filepath_prefix + LOOPGUARD_CHECK_FILENAME), (self._output_filepath_prefix + LOOPGUARD_CHECK_FILENAME), LOOPGUARD_CHECK_FIELDS),
            MonitoringParameter.MEMORY : ((self._working_filepath_prefix + MEMORY_CHECK_FILENAME), (self._output_filepath_prefix + MEMORY_CHECK_FILENAME), MEMORY_CHECK_FIELDS),
            MonitoringParameter.NTP_CONFIG : ((self._working_filepath_prefix + NTP_CONFIG_CHECK_FILENAME), (self._output_filepath_prefix + NTP_CONFIG_CHECK_FILENAME), NTP_CONFIG_CHECK_FIELDS),
            MonitoringParameter.PLATFORM_RESOURCES : ((self._working_filepath_prefix + PLATFORM_RESOURCES_CHECK_FILENAME), (self._output_filepath_prefix + PLATFORM_RESOURCES_CHECK_FILENAME), PLATFORM_RESOURCES_CHECK_FIELDS),
            MonitoringParameter.POE : ((self._working_filepath_prefix + POE_CHECK_FILENAME), (self._output_filepath_prefix + POE_CHECK_FILENAME), POE_CHECK_FIELDS),
            MonitoringParameter.RUN_STARTUP : ((self._working_filepath_prefix + RUN_STARTUP_CHECK_FILENAME), (self._output_filepath_prefix + RUN_STARTUP_CHECK_FILENAME), RUN_STARTUP_CHECK_FIELDS),
            MonitoringParameter.SPANNING_TREE : ((self._working_filepath_prefix + SPANNING_TREE_CHECK_FILENAME), (self._output_filepath_prefix + SPANNING_TREE_CHECK_FILENAME), SPANNING_TREE_CHECK_FIELDS),
            MonitoringParameter.SNMP_CONFIG : ((self._working_filepath_prefix + SNMP_CONFIG_CHECK_FILENAME), (self._output_filepath_prefix + SNMP_CONFIG_CHECK_FILENAME), SNMP_CONFIG_CHECK_FIELDS),
            MonitoringParameter.SSH_CONFIG : ((self._working_filepath_prefix + SSH_CONFIG_CHECK_FILENAME), (self._output_filepath_prefix + SSH_CONFIG_CHECK_FILENAME), SSH_CONFIG_CHECK_FIELDS),
            MonitoringParameter.SYSLOG_CONFIG : ((self._working_filepath_prefix + SYSLOG_CONFIG_CHECK_FILENAME), (self._output_filepath_prefix + SYSLOG_CONFIG_CHECK_FILENAME), SYSLOG_CONFIG_CHECK_FIELDS),
            MonitoringParameter.TACACS_CONFIG : ((self._working_filepath_prefix + TACACS_CONFIG_CHECK_FILENAME), (self._output_filepath_prefix + TACACS_CONFIG_CHECK_FILENAME), TACACS_CONFIG_CHECK_FIELDS),
            MonitoringParameter.UDLD : ((self._working_filepath_prefix + UDLD_CHECK_FILENAME), (self._output_filepath_prefix + UDLD_CHECK_FILENAME), UDLD_CHECK_FIELDS),
            MonitoringParameter.UPTIME : ((self._working_filepath_prefix + UPTIME_CHECK_FILENAME), (self._output_filepath_prefix + UPTIME_CHECK_FILENAME), UPTIME_CHECK_FIELDS),
            MonitoringParameter.VLAN : ((self._working_filepath_prefix + VLAN_CHECK_FILENAME), (self._output_filepath_prefix + VLAN_CHECK_FILENAME), VLAN_CHECK_FIELDS),
            MonitoringParameter.VLAN2 : ((self._working_filepath_prefix + VLAN_CHECK_FILENAME2), (self._output_filepath_prefix + VLAN_CHECK_FILENAME2), VLAN_CHECK_FIELDS2),
            MonitoringParameter.VLAN_PRIORITY : ((self._working_filepath_prefix + VLAN_PRIORITY_CHECK_FILENAME), (self._output_filepath_prefix + VLAN_PRIORITY_CHECK_FILENAME), VLAN_PRIORITY_CHECK_FIELDS)
        }

        self._working_file = None
        self._working_file_dictwriter = None
        
    def initialise_working_file(self):
        try:
            print(self._param_dict[self._monitoring_parameter][0])
            self._working_file = open(((self._param_dict[self._monitoring_parameter])[0]), 'w', newline="")
            self._working_file_dictwriter = csv.DictWriter(self._working_file, (self._param_dict[self._monitoring_parameter])[2])
            self._working_file_dictwriter.writeheader()
            return
        except Exception as err:
            print("<ALERT> unable to create working file ... " + str(err))
            return

    def write_row_working_file(self, i_dict):
        try:
            if(self._working_file == None or self._working_file_dictwriter == None): 
                print("<ALERT> working file object is not instantiated ... ")
                return
            self._working_file_dictwriter.writerow(i_dict)
            return
        except Exception as err:
            print("<ALERT> unable to write to working file ... " + str(err))
            return

    def close_working_file(self):
        try:
            if(self._working_file == None or self._working_file_dictwriter == None):
                print("<ALERT> working file object is not instantiated ... " + str(err))
                return
            self._working_file.close()
            self._working_file_dictwriter = None
            return
        except Exception as err:
            print("<ALERT> unable to close working file ... ")
            return
           

