from ipaddress import ip_address
from ipaddress import ip_network
from ipaddress import IPv4Address
from ipaddress import IPv4Network
from ip_reachability import reachability
from ipaddress import AddressValueError
import sys
import pandas as pd
import ip_csvcreator
import ip_tracer
import ip_aclchecker
import ip_aclconfirmer
import json
import ip_grouper
import ip_checker
import subprocess
from ip_reachability import reachability

"""
ticket_no = "SCTASK0010087465"
Source_IPs = ['10.195.10.50', '172.25.188.208', '10.195.24.112', '10.195.24.111', '10.195.18.62']
Destination_IPs = ['10.195.188.65', '10.195.188.31', '10.195.188.50', '10.195.188.64']

from_ip_aclchecker_s_to_d = {'10.195.10.0/24': {'in_acls': ['permit ip host 10.195.10.50 host 10.195.188.31', 'permit ip host 10.195.10.50 host 10.195.188.65', 'permit ip host 10.195.10.50 host 10.195.188.64'], 'in_numbering': ['1840', '1850', '2000'], 'in_acl_name': 'VL10-in', 'out_acls': [], 'out_numbering': [], 'out_acl_name': '', 'subnet_primary': 'sg624-atdc101-ds1-mn'}, '10.195.24.0/24': {'in_acls': ['permit ip host 10.195.24.111 host 10.195.188.50', 'permit ip host 10.195.24.112 host 10.195.188.50'], 'in_numbering': ['15930', '15940', '20000'], 'in_acl_name': 'VL24-in', 'out_acls': [], 'out_numbering': [], 'out_acl_name': '', 'subnet_primary': 'sg624-atdc108-ds1-mn'}, '10.195.18.0/24': {'in_acls': [], 'in_numbering': ['2440', '2450', '10000'], 'in_acl_name': 'VL18-in', 'out_acls': [], 'out_numbering': [], 'out_acl_name': '', 'subnet_primary': 'sg624-atdc105-ds1-mn'}, '172.25.188.0/22': {'in_acls': ['permit ip host 172.25.188.208 host 10.195.188.31', 'permit ip host 172.25.188.208 host 10.195.188.65', 'permit ip host 172.25.188.208 host 10.195.188.50', 'permit ip host 172.25.188.208 host 10.195.188.64'], 'in_numbering': ['3510', '3520', '5000'], 'in_acl_name': 'control_VL188in', 'out_acls': ['permit ip host 10.195.188.31 host 172.25.188.208', 'permit ip host 10.195.188.65 host 172.25.188.208', 'permit ip host 10.195.188.50 host 172.25.188.208', 'permit ip host 10.195.188.64 host 172.25.188.208'], 'out_numbering': ['3490', '3500', '5000'], 'out_acl_name': 'control_VL188out', 'subnet_primary': 'sg211-cr1-cs4-fAmn'}}
from_ip_aclchecker_d_to_s = {'10.195.188.0/24': {'in_acls': ['permit ip host 10.195.188.31 host 10.195.10.50', 'permit ip host 10.195.188.65 host 10.195.10.50', 'permit ip host 10.195.188.64 host 10.195.10.50', 'permit ip host 10.195.188.50 host 10.195.24.111', 'permit ip host 10.195.188.50 host 10.195.24.112', 'permit ip host 10.195.188.31 host 10.195.18.62', 'permit ip host 10.195.188.65 host 10.195.18.62', 'permit ip host 10.195.188.64 host 10.195.18.62', 'permit ip host 10.195.188.31 host 172.25.188.208', 'permit ip host 10.195.188.65 host 172.25.188.208', 'permit ip host 10.195.188.50 host 172.25.188.208', 'permit ip host 10.195.188.64 host 172.25.188.208'], 'in_numbering': ['41410', '41420', '60000'], 'in_acl_name': 'VL188-in', 'out_acls': [], 'out_numbering': [], 'out_acl_name': '', 'subnet_primary': 'sg624-afmr0-fvap01-ds1-mnvn'}}

action = ip_csvcreator.ipcsvcreator(from_ip_aclchecker_s_to_d, from_ip_aclchecker_d_to_s, Source_IPs, Destination_IPs, ticket_no)

print(action)
"""
"""
dtpo = pd.DataFrame(columns = ["Source_IPs", "Destination_IPs", "Implementations:", "Rollbacks:"])

for i, j in enumerate(Source_IPs):
    dtpo.loc[i, "Source_IPs"] = j

for i, j in enumerate(Destination_IPs):
    dtpo.loc[i, "Destination_IPs"] = j

Implementations_Column = []
for i in [from_ip_aclchecker_s_to_d, from_ip_aclchecker_d_to_s]:
    for kee, val in i.items():
        if len(val['in_acls']) > 0 and len(val['out_acls']) > 0:
            reqd_in_diff = int(val['in_numbering'][1]) - int(val['in_numbering'][0])
            reqd_in_gap = len(val['in_acls'])*(reqd_in_diff)
            reqd_out_diff = int(val['out_numbering'][1]) - int(val['out_numbering'][0])
            reqd_out_gap = len(val['out_acls'])*(reqd_in_diff)
            if (int(val['in_numbering'][-1]) - int(val['in_numbering'][-2])) > 2*(reqd_in_gap) and \
                (int(val['out_numbering'][-1]) - int(val['out_numbering'][-2])) > 2*(reqd_out_gap):
                Implementations_Column.append(val['subnet_primary'])
                Implementations_Column.append("config t")
                Implementations_Column.append(f"ip access-list extended {val['in_acl_name']}")
                Implementations_Column.append(f"remark {ticket_no}")
                [Implementations_Column.append(f"{int(val['in_numbering'][-2])+reqd_in_diff} {x}") for x in val['in_acls']]
                Implementations_Column.append("exit")
                Implementations_Column.append(f"ip access-list extended {val['out_acl_name']}")
                Implementations_Column.append(f"remark {ticket_no}")
                [Implementations_Column.append(f"{int(val['out_numbering'][-2])+reqd_out_diff} {x}") for x in val['out_acls']]
                Implementations_Column.append('end')
                Implementations_Column.append('wr')       
                Implementations_Column.append("")
            elif (int(val['in_numbering'][-1]) - int(val['in_numbering'][-2])) <= 2*(reqd_in_gap) and \
                (int(val['out_numbering'][-1]) - int(val['out_numbering'][-2])) <= 2*(reqd_out_gap):
                    Implementations_Column.append(val['subnet_primary'])
                    Implementations_Column.append("config t")
                    Implementations_Column.append(f"ip access-list extended {val['in_acl_name']}")
                    Implementations_Column.append(f"remark {ticket_no}")
                    Implementations_Column.append(f"no {val['in_numbering'][-1]}")
                    Implementations_Column.append(f"{int(val['in_numbering'][-1])+10*reqd_in_gap} deny ip any any")
                    [Implementations_Column.append(f"{int(val['in_numbering'][-2])+reqd_in_diff} {x}") for x in val['in_acls']]
                    Implementations_Column.append("exit")
                    Implementations_Column.append(f"ip access-list extended {val['out_acl_name']}")
                    Implementations_Column.append(f"remark {ticket_no}")
                    Implementations_Column.append(f"no {val['out_numbering'][-1]}")
                    Implementations_Column.append(f"{int(val['out_numbering'][-1])+10*reqd_out_gap} deny ip any any")
                    [Implementations_Column.append(f"{int(val['out_numbering'][-2])+reqd_out_diff} {x}") for x in val['out_acls']]
                    Implementations_Column.append('end')
                    Implementations_Column.append('wr')       
                    Implementations_Column.append("")
            elif (int(val['in_numbering'][-1]) - int(val['in_numbering'][-2])) > 2*(reqd_in_gap) and \
                (int(val['out_numbering'][-1]) - int(val['out_numbering'][-2])) <= 2*(reqd_out_gap):
                    Implementations_Column.append(val['subnet_primary'])
                    Implementations_Column.append("config t")
                    Implementations_Column.append(f"ip access-list extended {val['in_acl_name']}")
                    Implementations_Column.append(f"remark {ticket_no}")
                    [Implementations_Column.append(f"{int(val['in_numbering'][-2])+reqd_in_diff} {x}") for x in val['in_acls']]
                    Implementations_Column.append("exit")
                    Implementations_Column.append(f"ip access-list extended {val['out_acl_name']}")
                    Implementations_Column.append(f"remark {ticket_no}")
                    Implementations_Column.append(f"no {val['out_numbering'][-1]}")
                    Implementations_Column.append(f"{int(val['out_numbering'][-1])+10*reqd_out_gap} deny ip any any")
                    [Implementations_Column.append(f"{int(val['out_numbering'][-2])+reqd_out_diff} {x}") for x in val['out_acls']]
                    Implementations_Column.append('end')
                    Implementations_Column.append('wr')       
                    Implementations_Column.append("")
            elif (int(val['in_numbering'][-1]) - int(val['in_numbering'][-2])) <= 2*(reqd_in_gap) and \
                (int(val['out_numbering'][-1]) - int(val['out_numbering'][-2])) > 2*(reqd_out_gap):
                    Implementations_Column.append(val['subnet_primary'])
                    Implementations_Column.append("config t")
                    Implementations_Column.append(f"ip access-list extended {val['in_acl_name']}")
                    Implementations_Column.append(f"remark {ticket_no}")
                    Implementations_Column.append(f"no {val['in_numbering'][-1]}")
                    Implementations_Column.append(f"{int(val['in_numbering'][-1])+10*reqd_in_gap} deny ip any any")
                    [Implementations_Column.append(f"{int(val['in_numbering'][-2])+reqd_in_diff} {x}") for x in val['in_acls']]
                    Implementations_Column.append("exit")
                    Implementations_Column.append(f"ip access-list extended {val['out_acl_name']}")
                    Implementations_Column.append(f"remark {ticket_no}")
                    [Implementations_Column.append(f"{int(val['out_numbering'][-2])+reqd_out_diff} {x}") for x in val['out_acls']]
                    Implementations_Column.append('end')
                    Implementations_Column.append('wr')       
                    Implementations_Column.append("")
        elif len(val['in_acls']) > 0 and len(val['out_acls']) == 0:
            reqd_in_diff = int(val['in_numbering'][1]) - int(val['in_numbering'][0])
            reqd_in_gap = len(val['in_acls'])*(reqd_in_diff)
            if (int(val['in_numbering'][-1]) - int(val['in_numbering'][-2])) > 2*(reqd_in_gap):
                Implementations_Column.append(val['subnet_primary'])
                Implementations_Column.append("config t")
                Implementations_Column.append(f"ip access-list extended {val['in_acl_name']}")
                Implementations_Column.append(f"remark {ticket_no}")
                [Implementations_Column.append(f"{int(val['in_numbering'][-2])+reqd_in_diff} {x}") for x in val['in_acls']]
                Implementations_Column.append('end')
                Implementations_Column.append('wr')       
                Implementations_Column.append("")
            elif (int(val['in_numbering'][-1]) - int(val['in_numbering'][-2])) <= 2*(reqd_in_gap):
                Implementations_Column.append(val['subnet_primary'])
                Implementations_Column.append("config t")
                Implementations_Column.append(f"ip access-list extended {val['in_acl_name']}")
                Implementations_Column.append(f"remark {ticket_no}")
                Implementations_Column.append(f"no {val['in_numbering'][-1]}")
                Implementations_Column.append(f"{int(val['in_numbering'][-1])+10*reqd_in_gap} deny ip any any")
                [Implementations_Column.append(f"{int(val['in_numbering'][-2])+reqd_in_diff} {x}") for x in val['in_acls']]
                Implementations_Column.append('end')
                Implementations_Column.append('wr')       
                Implementations_Column.append("")
        elif len(val['in_acls']) == 0 and len(val['out_acls']) > 0:
            reqd_out_diff = int(val['out_numbering'][1]) - int(val['out_numbering'][0])
            reqd_out_gap = len(val['out_acls'])*(reqd_out_diff)
            if (int(val['out_numbering'][-1]) - int(val['out_numbering'][-2])) > 2*(reqd_out_gap):
                Implementations_Column.append(val['subnet_primary'])
                Implementations_Column.append("config t")
                Implementations_Column.append(f"ip access-list extended {val['out_acl_name']}")
                Implementations_Column.append(f"remark {ticket_no}")
                [Implementations_Column.append(f"{int(val['out_numbering'][-2])+reqd_out_diff} {x}") for x in val['out_acls']]
                Implementations_Column.append('end')
                Implementations_Column.append('wr')       
                Implementations_Column.append("")
            elif (int(val['out_numbering'][-1]) - int(val['out_numbering'][-2])) <= 2*(reqd_out_gap):
                Implementations_Column.append(val['subnet_primary'])
                Implementations_Column.append("config t")
                Implementations_Column.append(f"ip access-list extended {val['out_acl_name']}")
                Implementations_Column.append(f"remark {ticket_no}")
                Implementations_Column.append(f"no {val['out_numbering'][-1]}")
                Implementations_Column.append(f"{int(val['out_numbering'][-1])+10*reqd_out_gap} deny ip any any")
                [Implementations_Column.append(f"{int(val['out_numbering'][-2])+reqd_out_diff} {x}") for x in val['out_acls']]
                Implementations_Column.append('end')
                Implementations_Column.append('wr')       
                Implementations_Column.append("")
                                
Rollbacks_Column = []
for i in [from_ip_aclchecker_s_to_d, from_ip_aclchecker_d_to_s]:
    for kee, val in i.items():
        if len(val['in_acls']) > 0 and len(val['out_acls']) > 0:
            reqd_in_diff = int(val['in_numbering'][1]) - int(val['in_numbering'][0])
            reqd_in_gap = len(val['in_acls'])*(reqd_in_diff)
            reqd_out_diff = int(val['out_numbering'][1]) - int(val['out_numbering'][0])
            reqd_out_gap = len(val['out_acls'])*(reqd_in_diff)
            if (int(val['in_numbering'][-1]) - int(val['in_numbering'][-2])) > 2*(reqd_in_gap) and \
                (int(val['out_numbering'][-1]) - int(val['out_numbering'][-2])) > 2*(reqd_out_gap):
                Rollbacks_Column.append(val['subnet_primary'])
                Rollbacks_Column.append("config t")
                Rollbacks_Column.append(f"ip access-list extended {val['in_acl_name']}")
                Rollbacks_Column.append(f"no remark {ticket_no}")
                [Rollbacks_Column.append(f"no {int(val['in_numbering'][-2])+reqd_in_diff} {x}") for x in val['in_acls']]
                Rollbacks_Column.append("exit")
                Rollbacks_Column.append(f"ip access-list extended {val['out_acl_name']}")
                Rollbacks_Column.append(f"remark {ticket_no}")
                [Rollbacks_Column.append(f"no {int(val['out_numbering'][-2])+reqd_out_diff} {x}") for x in val['out_acls']]
                Rollbacks_Column.append('end')
                Rollbacks_Column.append('wr')       
                Rollbacks_Column.append("")
            elif (int(val['in_numbering'][-1]) - int(val['in_numbering'][-2])) <= 2*(reqd_in_gap) and \
                (int(val['out_numbering'][-1]) - int(val['out_numbering'][-2])) <= 2*(reqd_out_gap):
                    Rollbacks_Column.append(val['subnet_primary'])
                    Rollbacks_Column.append("config t")
                    Rollbacks_Column.append(f"ip access-list extended {val['in_acl_name']}")
                    Rollbacks_Column.append(f"no remark {ticket_no}")
                    #Rollbacks_Column.append(f"no {val['in_numbering'][-1]}")
                    #Rollbacks_Column.append(f"{int(val['in_numbering'][-1])+10*reqd_in_gap} deny ip any any")
                    [Rollbacks_Column.append(f"no {int(val['in_numbering'][-2])+reqd_in_diff} {x}") for x in val['in_acls']]
                    Rollbacks_Column.append("exit")
                    Rollbacks_Column.append(f"ip access-list extended {val['out_acl_name']}")
                    Rollbacks_Column.append(f"remark {ticket_no}")
                    #Rollbacks_Column.append(f"no {val['out_numbering'][-1]}")
                    #Rollbacks_Column.append(f"{int(val['out_numbering'][-1])+10*reqd_out_gap} deny ip any any")
                    [Rollbacks_Column.append(f"no {int(val['out_numbering'][-2])+reqd_out_diff} {x}") for x in val['out_acls']]
                    Rollbacks_Column.append('end')
                    Rollbacks_Column.append('wr')       
                    Rollbacks_Column.append("")
            elif (int(val['in_numbering'][-1]) - int(val['in_numbering'][-2])) > 2*(reqd_in_gap) and \
                (int(val['out_numbering'][-1]) - int(val['out_numbering'][-2])) <= 2*(reqd_out_gap):
                    Rollbacks_Column.append(val['subnet_primary'])
                    Rollbacks_Column.append("config t")
                    Rollbacks_Column.append(f"ip access-list extended {val['in_acl_name']}")
                    Rollbacks_Column.append(f"no remark {ticket_no}")
                    [Rollbacks_Column.append(f"no {int(val['in_numbering'][-2])+reqd_in_diff} {x}") for x in val['in_acls']]
                    Rollbacks_Column.append("exit")
                    Rollbacks_Column.append(f"ip access-list extended {val['out_acl_name']}")
                    Rollbacks_Column.append(f"no remark {ticket_no}")
                    #Rollbacks_Column.append(f"no {val['out_numbering'][-1]}")
                    #Rollbacks_Column.append(f"{int(val['out_numbering'][-1])+10*reqd_out_gap} deny ip any any")
                    [Rollbacks_Column.append(f"no {int(val['out_numbering'][-2])+reqd_out_diff} {x}") for x in val['out_acls']]
                    Rollbacks_Column.append('end')
                    Rollbacks_Column.append('wr')       
                    Rollbacks_Column.append("")
            elif (int(val['in_numbering'][-1]) - int(val['in_numbering'][-2])) <= 2*(reqd_in_gap) and \
                (int(val['out_numbering'][-1]) - int(val['out_numbering'][-2])) > 2*(reqd_out_gap):
                    Rollbacks_Column.append(val['subnet_primary'])
                    Rollbacks_Column.append("config t")
                    Rollbacks_Column.append(f"ip access-list extended {val['in_acl_name']}")
                    Rollbacks_Column.append(f"no remark {ticket_no}")
                    #Rollbacks_Column.append(f"no {val['in_numbering'][-1]}")
                    #Rollbacks_Column.append(f"{int(val['in_numbering'][-1])+10*reqd_in_gap} deny ip any any")
                    [Rollbacks_Column.append(f"no {int(val['in_numbering'][-2])+reqd_in_diff} {x}") for x in val['in_acls']]
                    Rollbacks_Column.append("exit")
                    Rollbacks_Column.append(f"ip access-list extended {val['out_acl_name']}")
                    Rollbacks_Column.append(f"no remark {ticket_no}")
                    [Rollbacks_Column.append(f"no {int(val['out_numbering'][-2])+reqd_out_diff} {x}") for x in val['out_acls']]
                    Rollbacks_Column.append('end')
                    Rollbacks_Column.append('wr')       
                    Rollbacks_Column.append("")
        elif len(val['in_acls']) > 0 and len(val['out_acls']) == 0:
            reqd_in_diff = int(val['in_numbering'][1]) - int(val['in_numbering'][0])
            reqd_in_gap = len(val['in_acls'])*(reqd_in_diff)
            if (int(val['in_numbering'][-1]) - int(val['in_numbering'][-2])) > 2*(reqd_in_gap):
                Rollbacks_Column.append(val['subnet_primary'])
                Rollbacks_Column.append("config t")
                Rollbacks_Column.append(f"ip access-list extended {val['in_acl_name']}")
                Rollbacks_Column.append(f"no remark {ticket_no}")
                [Rollbacks_Column.append(f"no {int(val['in_numbering'][-2])+reqd_in_diff} {x}") for x in val['in_acls']]
                Rollbacks_Column.append('end')
                Rollbacks_Column.append('wr')       
                Rollbacks_Column.append("")
            elif (int(val['in_numbering'][-1]) - int(val['in_numbering'][-2])) <= 2*(reqd_in_gap):
                Rollbacks_Column.append(val['subnet_primary'])
                Rollbacks_Column.append("config t")
                Rollbacks_Column.append(f"ip access-list extended {val['in_acl_name']}")
                Rollbacks_Column.append(f"no remark {ticket_no}")
                #Rollbacks_Column.append(f"no {val['in_numbering'][-1]}")
                #Rollbacks_Column.append(f"{int(val['in_numbering'][-1])+10*reqd_in_gap} deny ip any any")
                [Rollbacks_Column.append(f"no {int(val['in_numbering'][-2])+reqd_in_diff} {x}") for x in val['in_acls']]
                Rollbacks_Column.append('end')
                Rollbacks_Column.append('wr')       
                Rollbacks_Column.append("")
        elif len(val['in_acls']) == 0 and len(val['out_acls']) > 0:
            reqd_out_diff = int(val['out_numbering'][1]) - int(val['out_numbering'][0])
            reqd_out_gap = len(val['out_acls'])*(reqd_out_diff)
            if (int(val['out_numbering'][-1]) - int(val['out_numbering'][-2])) > 2*(reqd_out_gap):
                Rollbacks_Column.append(val['subnet_primary'])
                Rollbacks_Column.append("config t")
                Rollbacks_Column.append(f"ip access-list extended {val['out_acl_name']}")
                Rollbacks_Column.append(f"no remark {ticket_no}")
                [Rollbacks_Column.append(f"no {int(val['out_numbering'][-2])+reqd_out_diff} {x}") for x in val['out_acls']]
                Rollbacks_Column.append('end')
                Rollbacks_Column.append('wr')       
                Rollbacks_Column.append("")
            elif (int(val['out_numbering'][-1]) - int(val['out_numbering'][-2])) <= 2*(reqd_out_gap):
                Rollbacks_Column.append(val['subnet_primary'])
                Rollbacks_Column.append("config t")
                Rollbacks_Column.append(f"ip access-list extended {val['out_acl_name']}")
                Rollbacks_Column.append(f"no remark {ticket_no}")
                #Rollbacks_Column.append(f"no {val['out_numbering'][-1]}")
                #Rollbacks_Column.append(f"{int(val['out_numbering'][-1])+10*reqd_out_gap} deny ip any any")
                [Rollbacks_Column.append(f"no {int(val['out_numbering'][-2])+reqd_out_diff} {x}") for x in val['out_acls']]
                Rollbacks_Column.append('end')
                Rollbacks_Column.append('wr')       
                Rollbacks_Column.append("")

for i,j in enumerate(Implementations_Column):
    dtpo.loc[i, "Implementations:"] = j

for i,j in enumerate(Rollbacks_Column):
    dtpo.loc[i, "Rollbacks:"] = j       

dtpo.to_csv(f"{ticket_no}.csv")
"""
"""
sources_grouped_details = {('10.195.10.50',): {'group_L3': '10.195.1.2', 'group_vlan_no.': '10', 'group_subnet_svi': ['10.195.10.2', '255.255.255.0'], 'group_acls': {'in': 'VL10-in', 'out': 'not_present'}},\
                           ('10.195.24.112', '10.195.24.111'): {'group_L3': '10.195.1.30', 'group_vlan_no.': '24', 'group_subnet_svi': ['10.195.24.2', '255.255.255.0'], 'group_acls': {'in': 'VL24-in', 'out': 'not_present'}},\
                               ('10.195.18.62',): {'group_L3': '10.195.1.18', 'group_vlan_no.': '18', 'group_subnet_svi': ['10.195.18.2', '255.255.255.0'], 'group_acls': {'in': 'VL18-in', 'out': 'not_present'}}}


sources_grouped_details = {('10.195.10.50',): {'group_L3': '10.195.1.2', 'group_vlan_no.': '10', 'group_subnet_svi': ['10.195.10.2', '255.255.255.0'], 'group_acls': {'in': 'VL10-in', 'out': 'not_present'}},\
                           ('10.195.24.112', '10.195.24.111'): {'group_L3': '10.195.1.30', 'group_vlan_no.': '24', 'group_subnet_svi': ['10.195.24.2', '255.255.255.0'], 'group_acls': {'in': 'VL24-in', 'out': 'not_present'}},
                           ('172.25.188.208',): {'group_L3': '172.28.1.146', 'group_vlan_no.': '188', 'group_subnet_svi': ['172.25.188.6', '255.255.252.0'], 'group_acls': {'in': 'control_VL188in', 'out': 'control_VL188out'}}}
                               

destinations_grouped_details = {('10.195.188.64', '10.195.188.50', '10.195.188.65', '10.195.188.31'): {'group_L3': '10.195.1.74', 'group_vlan_no.': '188', 'group_subnet_svi': ['10.195.188.2', '255.255.255.0'], 'group_acls': {'in': 'VL188-in', 'out': 'not_present'}},
                                ('10.195.18.62',): {'group_L3': '10.195.1.18', 'group_vlan_no.': '18', 'group_subnet_svi': ['10.194.102.0', '255.255.254.0'], 'group_acls': {'in': 'VL18-in', 'out': 'not_present'}}}


#sources_grouped_details = {('10.195.10.50',): {'group_L3': '10.195.1.2', 'group_vlan_no.': '10', 'group_subnet_svi': ['10.195.10.2', '255.255.255.0'], 'group_acls': {'in': 'VL10-in', 'out': 'not_present'}}}
#sources_grouped_details = {('172.25.188.208',): {'group_L3': '172.28.1.146', 'group_vlan_no.': '188', 'group_subnet_svi': ['172.25.188.6', '255.255.252.0'], 'group_acls': {'in': 'control_VL188in', 'out': 'control_VL188out'}}}



destinations_grouped_details = {('10.195.188.64', '10.195.188.50', '10.195.188.65', '10.195.188.31'): {'group_L3': '10.195.1.74', 'group_vlan_no.': '188', 'group_subnet_svi': ['10.195.188.2', '255.255.255.0'], 'group_acls': {'in': 'VL188-in', 'out': 'not_present'}}}

"""
"""
sources_grouped_details = {('10.195.10.50',): {'group_L3': '10.195.1.2', 'group_vlan_no.': '10', 'group_subnet_svi': ['10.195.10.2', '255.255.255.0'], 'group_acls': {'in': 'VL10-in', 'out': 'not_present'}}, \
                           ('10.195.24.112', '10.195.24.111'): {'group_L3': '10.195.1.30', 'group_vlan_no.': '24', 'group_subnet_svi': ['10.195.24.2', '255.255.255.0'], 'group_acls': {'in': 'VL24-in', 'out': 'not_present'}}, \
                           ('10.195.18.62',): {'group_L3': '10.195.1.18', 'group_vlan_no.': '18', 'group_subnet_svi': ['10.195.18.2', '255.255.255.0'], 'group_acls': {'in': 'VL18-in', 'out': 'not_present'}}}

destinations_grouped_details = {('10.195.188.64', '10.195.188.31', '10.195.188.65', '10.195.188.50'): {'group_L3': '10.195.1.74', 'group_vlan_no.': '188', 'group_subnet_svi': ['10.195.188.2', '255.255.255.0'], 'group_acls': {'in': 'not_present', 'out': 'not_present'}}}
"""
"""
primary = "sg209-b1mr5y-cs1-mn"
dtpo_L3s = pd.read_csv("redundants.csv")

mask = dtpo_L3s['switchname'] == primary
find = dtpo_L3s[mask]

print(list(dtpo_L3s.iloc[int(str(list(find.index.values)[0]))+1].values)[0])
#print(int(str(list(find.index.values)[0])))
"""
"""
source_IPs = ['10.195.10.50', '10.195.18.62', '172.25.188.208', '10.195.24.112', '10.195.24.111', '10.195.24.249']
destination_IPs = ['10.195.188.31', '10.195.188.64', '10.195.188.50', '10.195.188.65']

s_traces, d_traces = ip_tracer.iptracer(source_IPs, destination_IPs)

print(s_traces, d_traces)
""" 
"""
Sources_L3s = {'10.195.10.50': '10.195.1.2', '10.195.18.62': '10.195.1.18', '172.25.188.208': '172.28.1.146', \
               '10.195.24.112': '10.195.1.30', '10.195.24.111': '10.195.1.30', '10.195.24.249': 'trace_failure'}
Destinations_L3s = {'10.195.188.31': '10.195.1.74', '10.195.188.6': 'trace_failure', '10.195.188.64': '10.195.1.74', \
                    '10.195.188.50': '10.195.1.74', '10.195.188.65': '10.195.1.74'}      

filetypeobject = open("failed.txt", "w")
            
print(Sources_L3s, 2*'\n', Destinations_L3s, 2*'\n')    

new_Sources_L3s = {}
new_Destinations_L3s = {}
for index, L3s in enumerate([Sources_L3s, Destinations_L3s]):
    for kee, val in L3s.items():
        if val == 'trace_failure' and index==0:
            print(f"\nRemoving the {kee} address from further processing since its L3 cannot be obtained..\n")
            filetypeobject.write(kee)
            filetypeobject.write('\n')
            continue
        elif val != 'trace_failure' and index==0:
            new_Sources_L3s[kee] = val
        elif val == 'trace_failure' and index==1:
            print(f"\nRemoving the {kee} address from further processing since its L3 cannot be obtained..\n")
            filetypeobject.write(kee)
            filetypeobject.write('\n')
            continue
        elif val != 'trace_failure' and index==1:
            new_Destinations_L3s[kee] = val

filetypeobject.close()            
print(new_Sources_L3s, 2*'\n', new_Destinations_L3s)
"""            

"""
sources_grouped_details = {('10.195.25.52',): {'group_L3': '10.195.1.30', 'group_vlan_no.': '25', 'group_subnet_svi': ['10.195.25.2', '255.255.255.0'], 'group_acls': {'in': 'VL25-in', 'out': 'not_present'}}}

destinations_grouped_details = {('10.195.27.42',): {'group_L3': '10.195.1.34', 'group_vlan_no.': '27', 'group_subnet_svi': ['10.195.27.2', '255.255.255.0'], 'group_acls': {'in': 'VL27-in', 'out': 'not_present'}}}

from_ip_aclchecker_s_to_d = ip_aclchecker.ipaclchecker(sources_grouped_details, destinations_grouped_details, 'source_to_destination')
from_ip_aclchecker_d_to_s = ip_aclchecker.ipaclchecker(destinations_grouped_details, sources_grouped_details, 'destination_to_source')

from_ip_aclchecker_s_to_d_j = json.dumps(from_ip_aclchecker_s_to_d, sort_keys=True, indent=4)
from_ip_aclchecker_d_to_s_j = json.dumps(from_ip_aclchecker_d_to_s, sort_keys=True, indent=4)
print('ACLs from the source side subnets towards destination subnets:', 2*'\n', from_ip_aclchecker_s_to_d_j, 2*'\n', \
      'ACLs from the destination side subnets towards source subnets:', 2*'\n', from_ip_aclchecker_d_to_s_j, 2*'\n', sep="")
"""
"""
lthree_connection = reachability("10.195.1.30")
entries_in = lthree_connection.send_command("sh ip access-lists VL25-in")
entries_in_list = entries_in.splitlines()

dtpo = pd.DataFrame(entries_in_list)
list1 = dtpo.values[0][0].split()
dtpo1 = pd.DataFrame(list1).T

for i in range(1,len(entries_in_list)):
    xx = dtpo.values[i][0].split()
    
    for j in range(len(xx)):
        dtpo1.loc[i, j] = xx[j] 
dtpo1 = dtpo1.reset_index(drop=True)

bool1 = dtpo1[3] == 'host'
bool2 = dtpo1[5] == 'host'
#bool3 = dtpo1[7].isnull()
bool4 = dtpo1[4] != 'any'
bool5 = dtpo1[4] != 'host'
bool6 = dtpo1[6] != 'any'
bool7 = dtpo1[6] != 'host'
allowtohost_dtpo = dtpo1[bool1 & bool2 & bool4 & bool5 & bool6 & bool7]
allowtohost_dtpo = allowtohost_dtpo.reset_index(drop=True)

print(allowtohost_dtpo)

sources_grouped_details = {('10.195.30.96',): {'group_L3': '10.195.1.42', 'group_vlan_no.': '30', 'group_subnet_svi': ['10.195.30.2', '255.255.255.0'], 'group_acls': {'in': 'VL30-in', 'out': 'not_present'}}}
destinations_grouped_details = {('10.195.188.101',): {'group_L3': '10.195.1.74', 'group_vlan_no.': '188', 'group_subnet_svi': ['10.195.188.2', '255.255.255.0'], 'group_acls': {'in': 'VL188-in', 'out': 'not_present'}}}

x = ip_aclchecker.ipaclchecker(destinations_grouped_details, sources_grouped_details, 'source_to_destination')

print(x)
"""
"""
reachables_sources = ['10.195.30.96']
reachables_destinations = ['10.195.188.98', '10.195.188.172', '10.195.188.173', '10.195.188.113', '10.195.188.99', '10.195.188.170', '10.195.188.117', '10.195.188.115', '10.195.188.116', '10.195.188.100', '10.195.188.219', '10.195.188.101', '10.195.188.175', '10.195.188.218', '10.195.188.174', '10.195.188.171', '10.195.188.220', '10.195.188.216', '10.195.188.114', '10.195.188.112', '10.195.188.97']
reachable_sources_L3s = {'10.195.30.96': '10.195.1.42'}
reachable_destinations_L3s = {'10.195.188.98': '10.195.1.74', '10.195.188.172': '10.195.1.74', '10.195.188.173': '10.195.1.74', '10.195.188.113': '10.195.1.74', '10.195.188.99': '10.195.1.74', '10.195.188.170': '10.195.1.74', '10.195.188.117': '10.195.1.74', '10.195.188.115': '10.195.1.74', '10.195.188.116': '10.195.1.74', '10.195.188.100': '10.195.1.74', '10.195.188.219': '10.195.1.74', '10.195.188.101': '10.195.1.74', '10.195.188.175': '10.195.1.74', '10.195.188.218': '10.195.1.74', '10.195.188.174': '10.195.1.74', '10.195.188.171': '10.195.1.74', '10.195.188.220': '10.195.1.74', '10.195.188.216': '10.195.1.74', '10.195.188.114': '10.195.1.74', '10.195.188.112': '10.195.1.74', '10.195.188.97': '10.195.1.74'}

sources_grouped, destinations_grouped, sources_vlan_details, destinations_vlan_details = \
    ip_grouper.ipgrouper(reachables_sources, reachables_destinations, reachable_sources_L3s, reachable_destinations_L3s)
"""
"""
x = reachability("10.195.1.74")
y = x.send_command("sh version | i uptime")
print(y)
x.disconnect()
#z = y = x.send_command("sh version | i Model")
#print(x)
"""
"""
reachables_sources = ['10.195.30.96']
reachables_destinations = ['10.195.188.98', '10.195.188.172', '10.195.188.173', '10.195.188.113', '10.195.188.99', '10.195.188.170', '10.195.188.117']
reachable_sources_L3s = {'10.195.30.96': '10.195.1.42'}
reachable_destinations_L3s = {'10.195.188.98': '10.195.1.74', '10.195.188.172': '10.195.1.74', '10.195.188.173': '10.195.1.74', '10.195.188.113': '10.195.1.74', '10.195.188.99': '10.195.1.74', '10.195.188.170': '10.195.1.74', '10.195.188.117': '10.195.1.74'}

sources_grouped, destinations_grouped, sources_vlan_details, destinations_vlan_details = \
    ip_grouper.ipgrouper(reachables_sources, reachables_destinations, reachable_sources_L3s, reachable_destinations_L3s)
"""
"""
reachables_sources = ['172.25.154.14', '172.25.154.19', '172.25.154.17', '172.25.154.18', '172.25.190.214', '172.25.154.16']
reachables_destinations = ['172.25.92.74', '172.25.92.72', '172.25.92.101', '172.25.92.71', '172.25.92.73', '172.25.92.70']
ticket_no = "SCTASK001000892192"
from_ip_aclchecker_s_to_d = {'172.25.152.0/21': {'in_acls': [], 'in_numbering': ['4380', '4390', '6000'], 'in_acl_name': 'control_VL152in', 'out_acls': [], 'out_numbering': ['4180', '4190', '6000'], 'out_acl_name': 'control_VL152out', 'subnet_primary': 'sg211-cr1-cs4-fbmn'}, '172.25.188.0/22': {'in_acls': [], 'in_numbering': ['3520', '3530', '5000'], 'in_acl_name': 'control_VL188in', 'out_acls': [], 'out_numbering': ['3500', '3510', '5000'], 'out_acl_name': 'control_VL188out', 'subnet_primary': 'sg211-cr1-cs4-fAmn'}} 

from_ip_aclchecker_d_to_s = {'172.25.92.0/24': {'in_acls': [], 'in_numbering': ['2620', '2630', '2640'], 'in_acl_name': 'control_VL92in', 'out_acls': [], 'out_numbering': ['2430', '2440', '2450'], 'out_acl_name': 'control_VL92out', 'subnet_primary': 'sg211-cr1-cs1-vsn'}}

action = ip_csvcreator.ipcsvcreator(from_ip_aclchecker_s_to_d, from_ip_aclchecker_d_to_s, reachables_sources, reachables_destinations, ticket_no) 
print(action)
"""
"""
reachables_sources = ['10.193.235.77']
reachables_destinations = ['10.193.247.158']

reachable_sources_L3s, reachable_destinations_L3s = ip_tracer.iptracer(reachables_sources, reachables_destinations)

print("reachable_sources_L3s:", reachable_sources_L3s, "\n") 
print("reachable_destinations_L3s:", reachable_destinations_L3s, "\n")
"""
"""
#x = ip_grouper.subnet_finder('10.194.1.178', '10.194.107.121')
x = ip_grouper.subnet_finder('10.194.2.130', '10.195.188.225')
print(x)
"""
"""
reachables_sources, reachables_destinations, unreachables_sources, unreachables_destinations = ip_checker.ipchecker()

print(reachables_sources)
print(reachables_destinations)
print(unreachables_sources)
print(unreachables_destinations)
"""
"""
address = "10.193.247.253"
output = subprocess.check_output(f"tracert {address}", shell=True).decode('utf-8')        
dtpo = pd.DataFrame(output.splitlines())
list1 = dtpo.values[0][0].split()
dtpo1 = pd.DataFrame(list1).T

for i in range(1,len(output.splitlines())):
    xx = dtpo.values[i][0].split()
    
    for j in range(len(xx)):
        dtpo1.loc[i, j] = xx[j]
        
dtpo1 = dtpo1.reset_index(drop=True)       
last_hop = list(dtpo1.loc[int(dtpo1.shape[0]) - int(2)])


#print(dtpo1, 3*'\n', last_hop)

dtpo1.to_csv("dtpo2.csv")
"""
"""
dtpo1 = pd.read_csv("dtpo2.csv")
dtpo1 = dtpo1.reset_index(drop=True)
print(ip_tracer.failediptracer(dtpo1))
"""

"""
for i in range(dtpo1.shape[0]):
    hop = list(dtpo1.loc[i].values)
    
    if 'Request' in hop and 'timed' in hop and 'out.' in hop:
        print(list(dtpo1.loc[i - 1].values))
        break
"""
"""
unreachableip = "10.195.188.225"
apparentlayerthree = "10.194.2.130"
lthree_connection = reachability(f"{apparentlayerthree}")
output = lthree_connection.send_command(f"sh ip route {unreachableip}")

dtpo = pd.DataFrame(output.splitlines())
list1 = dtpo.values[0][0].split()
dtpo1 = pd.DataFrame(list1).T

for i in range(1,len(output.splitlines())):
    xx = dtpo.values[i][0].split()
    
    for j in range(len(xx)):
        dtpo1.loc[i, j] = xx[j]
        
dtpo1 = dtpo1.reset_index(drop=True)

for i in range(dtpo1.shape[0]):
    if dtpo1.loc[i, 0] == '*':
        print(str(dtpo1.loc[i, 1]).replace(",", ""))
"""
"""
reachables_sources = ['172.25.154.30', '10.195.34.128', '10.195.34.129']
reachables_destinations = ['10.195.188.218', '10.195.14.67', '10.195.188.171', '10.193.247.242']
unreachables_sources = []
unreachables_destinations = []
from_ip_aclchecker_s_to_d = {'172.25.152.0/21': {'in_acls': ['permit ip host 172.25.154.30 host 10.195.188.218', 'permit ip host 172.25.154.30 host 10.195.188.171', 'permit ip host 172.25.154.30 host 10.195.14.67', 'permit ip host 172.25.154.30 host 10.193.247.242'], 'in_numbering': ['4400', '4410', '6000'], 'in_acl_name': 'control_VL152in', 'out_acls': ['permit ip host 10.195.188.218 host 172.25.154.30', 'permit ip host 10.195.188.171 host 172.25.154.30', 'permit ip host 10.195.14.67 host 172.25.154.30', 'permit ip host 10.193.247.242 host 172.25.154.30'], 'out_numbering': ['4200', '4210', '6000'], 'out_acl_name': 'control_VL152out', 'subnet_primary': 'sg211-cr1-cs4-fbmn'}, '10.195.34.0/24': {'in_acls': ['permit ip host 10.195.34.128 host 10.195.14.67', 'permit ip host 10.195.34.129 host 10.195.14.67', 'permit ip host 10.195.34.128 host 10.193.247.242', 'permit ip host 10.195.34.129 host 10.193.247.242'], 'in_numbering': ['2520', '2530', '5000'], 'in_acl_name': 'VL34-in', 'out_acls': [], 'out_numbering': [], 'out_acl_name': '', 'subnet_primary': 'sg624-atdc113-ds1-mn'}}
from_ip_aclchecker_d_to_s = {'10.195.188.0/24': {'in_acls': ['permit ip host 10.195.188.218 host 172.25.154.30', 'permit ip host 10.195.188.171 host 172.25.154.30'], 'in_numbering': ['57780', '57790', '60000'], 'in_acl_name': 'VL188-in', 'out_acls': [], 'out_numbering': [], 'out_acl_name': '', 'subnet_primary': 'sg624-afmr0-fvap01-ds1-mnvn'}, '10.195.14.0/24': {'in_acls': ['permit ip host 10.195.14.67 host 172.25.154.30', 'permit ip host 10.195.14.67 host 10.195.34.128', 'permit ip host 10.195.14.67 host 10.195.34.129'], 'in_numbering': ['3420', '3430', '10000'], 'in_acl_name': 'VL14-in', 'out_acls': [], 'out_numbering': [], 'out_acl_name': '', 'subnet_primary': 'sg624-atdc103-ds1-mn'}, '10.193.247.0/24': {'in_acls': ['permit ip host 10.193.247.242 host 172.25.154.30', 'permit ip host 10.193.247.242 host 10.195.34.128', 'permit ip host 10.193.247.242 host 10.195.34.129'], 'in_numbering': ['25970', '26000', '27000'], 'in_acl_name': 'control_VL247in', 'out_acls': ['permit ip host 172.25.154.30 host 10.193.247.242', 'permit ip host 10.195.34.128 host 10.193.247.242', 'permit ip host 10.195.34.129 host 10.193.247.242'], 'out_numbering': ['70', '80', '90'], 'out_acl_name': 'control_VL247out', 'subnet_primary': 'sg624-fmr0-cs1-mn'}}
ticket_no = 'testingtesting'

action = ip_csvcreator.ipcsvcreator(from_ip_aclchecker_s_to_d, from_ip_aclchecker_d_to_s, reachables_sources, reachables_destinations, unreachables_sources, unreachables_destinations, ticket_no) 
print(action)
"""
"""
#pre
sources_grouped_details = {('172.25.154.30',): {'group_L3': '172.28.1.154', 'group_vlan_no.': '152', 'group_subnet_svi': ['172.25.152.14', '255.255.248.0'], 'group_acls': {'in': 'control_VL152in', 'out': 'control_VL152out'}}, ('10.195.34.128', '10.195.34.129'): {'group_L3': '10.195.1.50', 'group_vlan_no.': '34', 'group_subnet_svi': ['10.195.34.2', '255.255.255.0'], 'group_acls': {'in': 'not_present', 'out': 'not_present'}}}
destinations_grouped_details = {('10.195.188.218', '10.195.188.171'): {'group_L3': '10.195.1.74', 'group_vlan_no.': '188', 'group_subnet_svi': ['10.195.188.2', '255.255.255.0'], 'group_acls': {'in': 'not_present', 'out': 'not_present'}}, ('10.193.247.242',): {'group_L3': '10.194.1.162', 'group_vlan_no.': '247', 'group_subnet_svi': ['10.193.247.2', '255.255.255.0'], 'group_acls': {'in': 'control_VL247in', 'out': 'not_present'}}, ('10.195.14.67',): {'group_L3': '10.195.1.10', 'group_vlan_no.': '14', 'group_subnet_svi': ['10.195.14.2', '255.255.255.0'], 'group_acls': {'in': 'VL14-in', 'out': 'not_present'}}}

sources_grouped_details, destinations_grouped_details = ip_aclconfirmer.pre_ipaclconfirmer(sources_grouped_details,\
                                                                                           destinations_grouped_details)
"""
"""
#post
sources_grouped_details = {('172.25.154.30',): {'group_L3': '172.28.1.154', 'group_vlan_no.': '152', 'group_subnet_svi': ['172.25.152.14', '255.255.248.0'], 'group_acls': {'in': 'control_VL152in', 'out': 'control_VL152out'}}, ('10.195.34.128', '10.195.34.129'): {'group_L3': '10.195.1.50', 'group_vlan_no.': '34', 'group_subnet_svi': ['10.195.34.2', '255.255.255.0'], 'group_acls': {'in': 'VL34-in', 'out': 'not_present'}}}
destinations_grouped_details = {('10.195.188.218', '10.195.188.171'): {'group_L3': '10.195.1.74', 'group_vlan_no.': '188', 'group_subnet_svi': ['10.195.188.2', '255.255.255.0'], 'group_acls': {'in': 'VL188-in', 'out': 'not_present'}}, ('10.193.247.242',): {'group_L3': '10.194.1.162', 'group_vlan_no.': '247', 'group_subnet_svi': ['10.193.247.2', '255.255.255.0'], 'group_acls': {'in': 'control_VL247in', 'out': 'control_VL247out'}}, ('10.195.14.67',): {'group_L3': '10.195.1.10', 'group_vlan_no.': '14', 'group_subnet_svi': ['10.195.14.2', '255.255.255.0'], 'group_acls': {'in': 'VL14-in', 'out': 'not_present'}}}

sources_grouped_details, destinations_grouped_details = ip_aclconfirmer.pre_ipaclconfirmer(sources_grouped_details,\
                                                                                           destinations_grouped_details)
"""
"""
from_ip_aclchecker_s_to_d = {'172.25.176.0/21': {'in_acls': [], 'in_numbering': [], 'in_acl_name': '', 'out_acls': [], 'out_numbering': [], 'out_acl_name': '', 'subnet_primary': 'sg211-cr1-cs4-cn'}} 

from_ip_aclchecker_d_to_s = {'172.25.92.0/24': {'in_acls': ['permit ip host 172.25.92.19 host 172.25.182.224'], 'in_numbering': ['2630', '2640', '2650'], 'in_acl_name': 'control_VL92in', 'out_acls': ['permit ip host 172.25.182.224 host 172.25.92.19'], 'out_numbering': ['2440', '2450', '2460'], 'out_acl_name': 'control_VL92out', 'subnet_primary': 'sg211-cr1-cs1-vsn'}} 

reachables_sources = ['172.25.182.224'] 

reachables_destinations = ['172.25.92.19'] 

unreachables_sources = [] 

unreachables_destinations = [] 

ticket_no = 'testingtesting'

action = ip_csvcreator.ipcsvcreator(from_ip_aclchecker_s_to_d, from_ip_aclchecker_d_to_s, reachables_sources, reachables_destinations, unreachables_sources, unreachables_destinations, ticket_no) 
print(action)
"""
"""
reachables_sources = ['10.195.24.229']
reachables_destinations = ['10.193.143.38', '10.193.143.35', '10.193.143.33', '10.193.143.32', '10.193.143.37', '10.193.143.36', '10.193.143.34', '10.193.143.39']
reachable_sources_L3s = {'10.195.24.229': '10.195.1.30'}
reachable_destinations_L3s = {'10.193.143.38': '10.194.2.177', '10.193.143.35': '10.194.2.177', '10.193.143.33': '10.194.2.177', '10.193.143.32': '10.194.2.177', '10.193.143.37': '10.194.2.177', '10.193.143.36': '10.194.2.177', '10.193.143.34': '10.194.2.177', '10.193.143.39': '10.194.2.177'}

sources_grouped, destinations_grouped, sources_vlan_details, destinations_vlan_details = \
    ip_grouper.ipgrouper(reachables_sources, reachables_destinations, reachable_sources_L3s, reachable_destinations_L3s)

sources_grouped = [tuple(x) for x in sources_grouped]
destinations_grouped = [tuple(x) for x in destinations_grouped]

print("sources_grouped:", sources_grouped)
print("destinations_grouped:", destinations_grouped)
"""
"""
deny_in = ''
lthree_connection = reachability("192.153.243.11")
entries_in = lthree_connection.send_command("sh ip access-lists control_VL92in")
entries_in_list = entries_in.splitlines()

dtpo = pd.DataFrame(entries_in_list)
list1 = dtpo.values[0][0].split()
dtpo1 = pd.DataFrame(list1).T

for i in range(1,len(entries_in_list)):
    xx = dtpo.values[i][0].split()
    
    for j in range(len(xx)):
        dtpo1.loc[i, j] = xx[j] 
dtpo1 = dtpo1.reset_index(drop=True)  

lastentry = list(dtpo1.tail(1).values[0])
if 'deny' in lastentry and 'ip' in lastentry and 'any' in lastentry:
    denyy = 'yes'
else: denyy = 'no'

print(denyy)
"""

