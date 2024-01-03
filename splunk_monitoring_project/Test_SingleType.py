import CiscoIOSParamHandler
import QueryHandler
import IOHandler
from ScriptConstants import *
from datetime import datetime

print(datetime.now())

input_handler = IOHandler.InputHandler(r"inputfilef10w.csv", SiteName.F10W)
input_handler.initialise_device_list()

test_list = input_handler.get_cisco_device_list()

#output_handler = IOHandler.OutputHandler(SiteName.F10W, MonitoringParameter.UPTIME)
#output_handler = IOHandler.OutputHandler(SiteName.F10W, MonitoringParameter.DISCONNECTED_PORTS)
#output_handler = IOHandler.OutputHandler(SiteName.F10W, MonitoringParameter.SNMP_CONFIG)
#output_handler = IOHandler.OutputHandler(SiteName.F10W, MonitoringParameter.VLAN)
output_handler = IOHandler.OutputHandler(SiteName.F10W, MonitoringParameter.VLAN2)
#output_handler = IOHandler.OutputHandler(SiteName.F10W, MonitoringParameter.VLAN_PRIORITY)
#output_handler = IOHandler.OutputHandler(SiteName.F10W, MonitoringParameter.BPDU)
#output_handler = IOHandler.OutputHandler(SiteName.F10W, MonitoringParameter.LOOPGUARD)
#output_handler = IOHandler.OutputHandler(SiteName.F10W, MonitoringParameter.KEEPALIVE)
output_handler.initialise_working_file()

for entry in test_list:
    try:
        query_handler = QueryHandler.QueryHandler(entry, DeviceType.CISCO_IOS)
        #test_string_show_int_status = query_handler.get_show_int_status()
        #test_string_show_run = query_handler.get_show_running_config()
        #test_string_show_version = query_handler.get_show_version()
        #test_string_show_cdp_neighbour = query_handler.get_show_neighbour()
        #test_string_show_spanning_tree_root = query_handler.get_show_spanning_tree_root()
        test_string_show_vlan_br = query_handler.get_show_vlan_br()
        test_string_show_int_trunk = query_handler.get_show_int_trunk()
        #test_string_show_int = query_handler.get_show_int()
        query_handler.disconnect()
        print("now processing " + str(entry) + " ...")
        
        #res_check_snmp_config = CiscoIOSParamHandler.check_snmp_config(test_string_show_run, entry)
        #res_disconnected_ports = CiscoIOSParamHandler.check_disconnected_ports(test_string_show_int_status, entry)
        #res_check_uptime = CiscoIOSParamHandler.check_uptime(test_string_show_version, entry)
        #res_check_vlan = CiscoIOSParamHandler.check_vlan(test_string_show_cdp_neighbour, test_string_show_spanning_tree_root, entry)
        #res_check_keepalive = CiscoIOSParamHandler.check_keepalive(test_string_show_int_status, test_string_show_int, entry)
        
        """
        if 'as' in entry or 'ds' in entry:
            res_check_loopguard = CiscoIOSParamHandler.check_loopguard(test_string_show_int_status, test_string_show_cdp_neighbour, test_string_show_run, entry)
        """  

        """
        if 'cs' in entry or 'ds' in entry and 'as' not in entry:
            res_check_vlan_priority = CiscoIOSParamHandler.check_vlan_priority(test_string_show_run, test_string_show_vlan_br, entry)
        else: continue
        """
        
        if 'as' in entry or 'ds' in entry:
            res_check_vlan2 = CiscoIOSParamHandler.check_vlan2(test_string_show_vlan_br, test_string_show_int_trunk, entry)
        
        
        """
        if 'as' in entry:
            res_check_bpdu = CiscoIOSParamHandler.check_bpdu(test_string_show_int_status, test_string_show_run, entry)
        """    
        for entry in res_check_vlan2:
            output_handler.write_row_working_file(entry)
        
    except Exception as err:
        print("<ALERT> problem with switch " + entry + " ... " + str(err))
        pass
    

output_handler.close_working_file()

print(datetime.now())



