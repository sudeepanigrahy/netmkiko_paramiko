# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 09:22:05 2024

@author: sscnoc
"""

from netmiko import ConnectHandler
from ipaddress import ip_network
from ipaddress import IPv4Network
from ipaddress import IPv4Address
import json
import ip_checker
import ip_tracer
import ip_grouper
import ip_aclconfirmer
import ip_aclchecker
import ip_csvcreator

ticket_no = input("What's the ticket number ?\n")

#Here, the 'reachables_sources' and the 'reachables_destinations' are getting all the IPs, i.e. reachable ones and unreachable ones too
reachables_sources, reachables_destinations, unreachables_sources, unreachables_destinations = ip_checker.ipchecker()

reachable_sources_L3s, reachable_destinations_L3s = ip_tracer.iptracer(reachables_sources, reachables_destinations)

print("reachables_sources:", '\n', reachables_sources)
print("reachables_destinations:", '\n', reachables_destinations)
print("reachable_sources_L3s:", '\n', reachable_sources_L3s)
print("reachable_destinations_L3s:", '\n', reachable_destinations_L3s, '\n')

sources_grouped, destinations_grouped, sources_vlan_details, destinations_vlan_details = \
    ip_grouper.ipgrouper(reachables_sources, reachables_destinations, reachable_sources_L3s, reachable_destinations_L3s)

sources_grouped = [tuple(x) for x in sources_grouped]
destinations_grouped = [tuple(x) for x in destinations_grouped]

sources_grouped_details = {}
destinations_grouped_details = {}

for index, group_side in enumerate([sources_grouped, destinations_grouped]):
    for group in group_side:
        if index==0:
            sources_grouped_details[group] = {
                                              'group_L3' : reachable_sources_L3s[group[0]],
                                              'group_vlan_no.' : sources_vlan_details[group[0]]['vlan_number'],
                                              'group_subnet_svi' : sources_vlan_details[group[0]]['subnet_svi'],
                                              'group_acls' : {'in': sources_vlan_details[group[0]]['access_list_in'],
                                                              'out': sources_vlan_details[group[0]]['access_list_out']}
                                              }
        elif index==1:
            destinations_grouped_details[group] = {
                                              'group_L3' : reachable_destinations_L3s[group[0]],
                                              'group_vlan_no.' : destinations_vlan_details[group[0]]['vlan_number'],
                                              'group_subnet_svi' : destinations_vlan_details[group[0]]['subnet_svi'],
                                              'group_acls' : {'in': destinations_vlan_details[group[0]]['access_list_in'],
                                                              'out': destinations_vlan_details[group[0]]['access_list_out']}
                                              }

sources_grouped_details, destinations_grouped_details = ip_aclconfirmer.pre_ipaclconfirmer(sources_grouped_details,\
                                                                                           destinations_grouped_details)


from_ip_aclchecker_s_to_d = ip_aclchecker.ipaclchecker(sources_grouped_details, destinations_grouped_details, 'source_to_destination')
from_ip_aclchecker_d_to_s = ip_aclchecker.ipaclchecker(destinations_grouped_details, sources_grouped_details, 'destination_to_source')


from_ip_aclchecker_s_to_d_j = json.dumps(from_ip_aclchecker_s_to_d, sort_keys=True, indent=4)
from_ip_aclchecker_d_to_s_j = json.dumps(from_ip_aclchecker_d_to_s, sort_keys=True, indent=4)
print('ACLs from the source side subnets towards destination subnets:', 2*'\n', from_ip_aclchecker_s_to_d_j, 2*'\n', \
      'ACLs from the destination side subnets towards source subnets:', 2*'\n', from_ip_aclchecker_d_to_s_j, 2*'\n', sep="")

"""    
from_ip_aclchecker_s_to_d["10.195.188.0/24"]["in_numbering"] = [
    "49760",
    "49770",
    "60000"
]
"""
action = ip_csvcreator.ipcsvcreator(from_ip_aclchecker_s_to_d, from_ip_aclchecker_d_to_s, reachables_sources, reachables_destinations, unreachables_sources, unreachables_destinations, ticket_no) 
print(action)
    