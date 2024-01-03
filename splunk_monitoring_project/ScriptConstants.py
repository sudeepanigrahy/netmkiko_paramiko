import enum

class MonitoringParameter(enum.Enum):
    CRC = 1
    MEMORY= 2
    PLATFORM_RESOURCES = 3
    DISCONNECTED_PORTS = 4
    NTP_CONFIG = 5
    SYSLOG_CONFIG = 6
    SNMP_CONFIG = 7
    SSH_CONFIG = 8
    TACACS_CONFIG = 9
    VLAN = 10
    BPDU = 11
    BROADCAST = 12
    KEEPALIVE = 13
    LOOPGUARD = 14
    RUN_STARTUP = 15
    SPANNING_TREE = 16
    UPTIME = 17
    UDLD = 18
    POE = 19
    VLAN2 = 20
    VLAN_PRIORITY = 21

class SiteName(enum.Enum):
    F10NXA = 1
    F10W = 2
    MSB = 3

class DeviceType(enum.Enum):
    CISCO_IOS = 1
    CISCO_NXOS = 2
    ARISTA_EOS = 3

CISCO_IOS_COMMAND_SET = {
    'show_int': "show int | i CRC|output errors|line|Keepalive",
    'show_int_status': "show int status",
    'show_neighbour': "show cdp nei",
    'show_running_config': "show run",
    'show_startup_config': "show startup-config",
    'show_spanning_tree': "show spanning-tree",
    'show_spanning_tree_root': "show spanning-tree root",
    'show_platform_resources': "show platform resources",
    'show_process_memory': "sh processes memory | i Processor|System",
    'show_kernel_memory': "sh platform software status control-processor brief",
    'show_version': "show version",
    'show_power_inline': "show power inline",
    'show_vlan_br': "show vlan br",
    'show_int_trunk': "show int trunk"
    
}
CISCO_NXOS_COMMAND_SET = {
    'show_int': "show int | i 'Ethernet|CRC|output error|input error|Keepalive'",
    'show_int_status': "show int status",
    'show_neighbour': "show cdp nei",
    'show_running_config': "show run",
    'show_startup_config': "show startup-config",
    'show_spanning_tree': "show spanning-tree",
    'show_process_memory': "show system resources | i 'Memory usage'",
    'show_version': "show version"


}
ARISTA_EOS_COMMAND_SET = {
    'show_int': "show int | i CRC|output errors|line",
    'show_int_status': "show int status",
    'show_neighbour': "show lldp nei",
    'show_running_config': "show run",
    'show_startup_config': "show startup-config",
    'show_spanning_tree': "show spanning-tree",
    'show_total_memory': "show version | i memory",
    'show_process_memory': "show process top once | i Mem",
    'show_version': "show version"

}

F10NXA_SNMP_SERVER_IP = ['***********', '***********']
F10W_SNMP_SERVER_IP = ['***********', '***********']
MSB_SNMP_SERVER_IP = ['***********', '***********']
SNMP_COMMUNITY = '***********'
SNMP_VERSION = '***********'

F10NXA_SYSLOG_SERVER_IP = '***********'
F10W_SYSLOG_SERVER_IP = '***********'
MSB_SYSLOG_SERVER_IP = '***********'

F10NXA_OUTPUT_FILEPATH = r'***********'
F10W_OUTPUT_FILEPATH = r'***********'
MSB_OUTPUT_FILEPATH = r'***********'

F10NXA_WORKING_FILEPATH = r'***********'
F10W_WORKING_FILEPATH = r'C:\Users\***********\.spyder-py3\Saves\Python.N\WorkingFolder\myworkingfolder\F10W_'
MSB_WORKING_FILEPATH = r'***********'

CRC_CHECK_FILENAME = "crc_check.csv"                           
MEMORY_CHECK_FILENAME = "memory.csv"                            
PLATFORM_RESOURCES_CHECK_FILENAME = "platformResources.csv"     
POE_CHECK_FILENAME = "poe_check.csv"                            
DISCONNECTED_PORTS_CHECK_FILENAME = "disconnectedPorts.csv"     
NTP_CONFIG_CHECK_FILENAME = "ntpcheck.csv"
SYSLOG_CONFIG_CHECK_FILENAME = "syslogcheck.csv"
SNMP_CONFIG_CHECK_FILENAME = "snmpcheck.csv"
SSH_CONFIG_CHECK_FILENAME = "sshcheck.csv"
TACACS_CONFIG_CHECK_FILENAME = "tacacscheck.csv"
VLAN_CHECK_FILENAME = "checkvlan.csv"
VLAN_CHECK_FILENAME2 = "checkvlan2.csv"
VLAN_PRIORITY_CHECK_FILENAME = "checkvlanpriority.csv"
BPDU_CHECK_FILENAME = "bpdu_check.csv"
BROADCAST_CHECK_FILENAME = "broadcast_check.csv"
KEEPALIVE_CHECK_FILENAME = "keepalive_check.csv"
LOOPGUARD_CHECK_FILENAME = "loopguard_check.csv"
RUN_STARTUP_CHECK_FILENAME = "run_startup_check.csv"            
SPANNING_TREE_CHECK_FILENAME = "spanningtree_check.csv"         
UPTIME_CHECK_FILENAME = "bug_uptime_check.csv"
UDLD_CHECK_FILENAME = "udld_check.csv"


CRC_CHECK_FIELDS = ['timestamp', 'switch name', 'interface name', 'CRC error', 'input error', 'output error']
MEMORY_CHECK_FIELDS = ['timestamp', 'switch name', 'process name', 'total', 'used', 'free', 'commited', 'used percentage', 'kernel percentage']
PLATFORM_RESOURCES_CHECK_FIELDS = ['timestamp', 'switch name', 'cpu status', 'mem status', 'remarks']
POE_CHECK_FIELDS = ['timestamp', 'switch name' ,'available power', 'used power', 'rem power', 'percentage used', 'remarks']
DISCONNECTED_PORTS_CHECK_FIELDS = ['timestamp', 'switch name', 'interface name']
NTP_CONFIG_CHECK_FIELDS = ['timestamp', 'switch name', 'discrepancy']
SYSLOG_CONFIG_CHECK_FIELDS = ['timestamp', 'switch name', 'discrepancy']
SNMP_CONFIG_CHECK_FIELDS = ['timestamp', 'switch name', 'discrepancy', 'remarks']
SSH_CONFIG_CHECK_FIELDS = ['timestamp', 'switch name', 'discrepancy', 'enabled', 'version']
TACACS_CONFIG_CHECK_FIELDS = ['timestamp', 'switch name', 'discrepancy', 'remarks']
VLAN_CHECK_FIELDS = ['timestamp', 'switch name', 'vlan', 'discrepancy', 'mac']
VLAN_CHECK_FIELDS2 = ['timestamp', 'switch name', 'discrepancy', 'vlans', 'trunked_vlans', 'remarks']
VLAN_PRIORITY_CHECK_FIELDS = ['timestamp', 'switch name', 'discrepancy', 'missing_vlans', 'priority', 'remarks']
BPDU_CHECK_FIELDS = ['timestamp', 'switch name', 'interface name', 'configuration', 'remarks']
BROADCAST_CHECK_FIELDS = ['timestamp', 'switch name', 'interface name', 'configuration', 'remarks']
KEEPALIVE_CHECK_FIELDS = ['timestamp', 'switch name', 'interface name', 'status']
LOOPGUARD_CHECK_FIELDS = ['timestamp', 'switch name', 'interface name', 'configuration']
RUN_STARTUP_CHECK_FIELDS = ['timestamp', 'switch name', 'last config change', 'discrepancy']
SPANNING_TREE_CHECK_FIELDS = ['timestamp', 'switch name', 'vlan number', 'interface name', 'role', 'status', 'dual link']
UDLD_CHECK_FIELDS = ['timestamp', 'switch name', 'interface name', 'configuration']
UPTIME_CHECK_FIELDS = ['timestamp', 'switch name', 'uptime']


