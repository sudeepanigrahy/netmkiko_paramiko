Below are the 13 columns of data that will be created when the testmain.py is run:

1-'Spanning-tree Root' : 'yes' if all vlans have primary uplink as root port, otherwise 'no'
2-'AS-Used VLANs' : list of vlans used by all access ports
3-'AS-Configured VLANs' : list of all vlans configured on the switch
4-'AS-Trunked VLANs to Primary' : list of vlans trunked to primary uplink port
5-'AS-Trunked VLANs to Secondary' : list of vlans trunked to secondary uplink port
6-'Primary Connected DS Hostname' : primary connected DS name
7-'Primary DS-Configured VLANs' : list of vlans configured on primary DS
8-'Primary DS-Trunked VLANs' : list of vlans trunked from primary DS towards the AS downlink
  (in spt forwarding state and not pruned)
9-'Secondary Connected DS Hostname' : secondary connected DS name
10-'Secondary DS-Configured VLANs' : list of vlans configured on secondary DS
11-'Secondary DS-Trunked VLANs' : list of vlans trunked from secondary DS towards the AS downlink
12-'Configured VLAN Mismatch' : 'no' if 3 is a subset of 7 and 10, 'yes' if 3 is not a subset of 7 and 10
13-'Used VLAN Mismatch' : 'yes' if atleast one vlan from 2 is not present in
                           3 or 4 or 5 or 7 or 8 or 10 or 11

checkusedvlans: 2
checkvlansiftrunked: 3, 4, 5, 7, 10, 8, 11
checkvlansrootport: 1, 6, 9
checkvlanspriority: 3, 7, 10
checkdownlinktrunkedvlans: 8, 11



