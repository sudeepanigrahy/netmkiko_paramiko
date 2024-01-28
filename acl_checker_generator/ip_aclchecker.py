import pandas as pd
from ipaddress import ip_network
from ipaddress import IPv4Network
from ipaddress import IPv4Address
from ip_reachability import reachability
    
def hosttohost(dtpo1, dtpo3, in_acl_comm, out_acl_comm, ssubnet_IPs, dsubnet_IPs, subnet_s):
    ssubnet_IPs = list(ssubnet_IPs)
    dsubnet_IPs = list(dsubnet_IPs)
    acl_entries_in, acl_entries_out = [], []
    if in_acl_comm=='not_present' and type(dtpo1)==type(pd.DataFrame([])):
        bool1 = dtpo1[3] == 'host'
        bool2 = dtpo1[5] == 'host'
        bool3 = dtpo1[7].isnull()
        bool4 = dtpo1[4] != 'any'
        bool5 = dtpo1[4] != 'host'
        bool6 = dtpo1[6] != 'any'
        bool7 = dtpo1[6] != 'host'
        allowtohost_dtpo = dtpo1[bool1 & bool2 & bool3 & bool4 & bool5 & bool6 & bool7]
        allowtohost_dtpo = allowtohost_dtpo.reset_index(drop=True)

        bool8 = dtpo1[3] == 'any'
        bool9 = dtpo1[4] == 'host'
        bool10 = dtpo1[6].isnull()
        bool11 = dtpo1[5] != 'any'
        bool12 = dtpo1[5] != 'host'
        allowtohost_dtpo1 = dtpo1[bool8 & bool9 & bool10 & bool11 & bool12]
        allowtohost_dtpo1 = allowtohost_dtpo1.reset_index(drop=True)

        bool13 = dtpo1[3] != 'any'
        bool14 = dtpo1[3] != 'host'
        bool15 = dtpo1[4] != 'any'
        bool16 = dtpo1[4] != 'host'
        bool17 = dtpo1[5] == 'host'
        bool18 = dtpo1[7].isnull()
        bool19 = dtpo1[6] != 'any'
        bool20 = dtpo1[6] != 'host'
        allowtohost_dtpo2 = dtpo1[bool13 & bool14 & bool15 & bool16 & bool17 & bool18 & bool19 & bool20]
        allowtohost_dtpo2 = allowtohost_dtpo2.reset_index(drop=True)
        
        bool21 = dtpo1[3] != "any"
        bool22 = dtpo1[3] != "host"
        bool23 = dtpo1[4] != "any"
        bool24 = dtpo1[4] != "host"
        bool25 = dtpo1[5] == "any"
        bool26 = dtpo1[6].isnull()
        allowtohost_dtpo3 = dtpo1[bool21 & bool22 & bool23 & bool24 & bool25 & bool26]
        allowtohost_dtpo3 = allowtohost_dtpo3.reset_index(drop=True)
        
        for s_ip in ssubnet_IPs:
            for d_ip in dsubnet_IPs:
                bool27 = allowtohost_dtpo[4] == s_ip
                bool28 = allowtohost_dtpo[6] == d_ip
                allowedtohost_dtpo =  allowtohost_dtpo[bool27 & bool28]
                
                bool29 = allowtohost_dtpo1[5] == d_ip
                allowedtohost_dtpo1 = allowtohost_dtpo1[bool29]
                
                bool30 = allowtohost_dtpo2[3] == str(subnet_s.network_address)
                bool31 = allowtohost_dtpo2[6] == d_ip
                allowedtohost_dtpo2 = allowtohost_dtpo2[bool30 & bool31]
                
                bool32 = allowtohost_dtpo3[3] == str(subnet_s.network_address)
                allowedtohost_dtpo3 = allowtohost_dtpo3[bool32]
                
                if len(allowedtohost_dtpo) > 0 or len(allowedtohost_dtpo1) > 0:
                    continue
                elif len(allowedtohost_dtpo2) > 0:
                    for row in range(len(allowedtohost_dtpo2)):
                        if subnet_s == ip_network(f"{allowedtohost_dtpo2.loc[row][3]}/{allowedtohost_dtpo2.loc[row][4]}", strict = False) and \
                            allowedtohost_dtpo2.loc[row][6]==d_ip:
                                continue
                elif len(allowedtohost_dtpo3) > 0:
                    for row in range(len(allowedtohost_dtpo3)):
                        row_subnet = ip_network(f"{allowedtohost_dtpo3.loc[row][3]}/{allowedtohost_dtpo3.loc[row][4]}", strict = False)
                        if int(str(row_subnet).split('/')[-1]) > int(str(subnet_s).split('/')[-1]):
                            if row_subnet in list(subnet_s.subnets(new_prefix=int(str(row_subnet).split('/')[-1]))):
                                if IPv4Address(f"{s_ip}") in row_subnet:
                                    continue 
                                else: pass
                            else: pass
                        else: pass
                else:
                    print(f"permit ip host {s_ip} host {d_ip}")
                    acl_entries_in.append(f"permit ip host {s_ip} host {d_ip}")
        print('\n')
        
    if out_acl_comm=='not_present' and type(dtpo3)==type(pd.DataFrame([])):
        bool1 = dtpo1[3] == 'host'
        bool2 = dtpo1[5] == 'host'
        bool3 = dtpo1[7].isnull()
        bool4 = dtpo1[4] != 'any'
        bool5 = dtpo1[4] != 'host'
        bool6 = dtpo1[6] != 'any'
        bool7 = dtpo1[6] != 'host'
        allowtohost_dtpo = dtpo1[bool1 & bool2 & bool3 & bool4 & bool5 & bool6 & bool7]
        allowtohost_dtpo = allowtohost_dtpo.reset_index(drop=True)

        bool8 = dtpo1[3] == 'host'
        bool9 = dtpo1[5] == 'any'
        bool10 = dtpo1[6].isnull()
        bool11 = dtpo1[4] != 'any'
        bool12 = dtpo1[4] != 'host'
        allowtohost_dtpo1 = dtpo1[bool8 & bool9 & bool10 & bool11 & bool12]
        allowtohost_dtpo1 = allowtohost_dtpo1.reset_index(drop=True)

        bool13 = dtpo1[4] != 'any'
        bool14 = dtpo1[4] != 'host'
        bool15 = dtpo1[5] != 'any'
        bool16 = dtpo1[5] != 'host'
        bool17 = dtpo1[6] != 'any'
        bool18 = dtpo1[6] != 'host'
        bool19 = dtpo1[3] == 'host'
        bool20 = dtpo1[7].isnull()
        allowtohost_dtpo2 = dtpo1[bool13 & bool14 & bool15 & bool16 & bool17 & bool18 & bool19 & bool20]
        allowtohost_dtpo2 = allowtohost_dtpo2.reset_index(drop=True)
        
        bool21 = dtpo1[4] != "any"
        bool22 = dtpo1[4] != "host"
        bool23 = dtpo1[5] != "any"
        bool24 = dtpo1[5] != "host"
        bool25 = dtpo1[3] == "any"
        bool26 = dtpo1[6].isnull()
        allowtohost_dtpo3 = dtpo1[bool21 & bool22 & bool23 & bool24 & bool25 & bool26]
        allowtohost_dtpo3 = allowtohost_dtpo3.reset_index(drop=True)
        
        for s_ip in ssubnet_IPs:
            for d_ip in dsubnet_IPs:
                bool27 = allowtohost_dtpo[4] == d_ip
                bool28 = allowtohost_dtpo[6] == s_ip
                allowedtohost_dtpo =  allowtohost_dtpo[bool27 & bool28]
                
                bool29 = allowtohost_dtpo1[4] == d_ip
                allowedtohost_dtpo1 = allowtohost_dtpo1[bool29]
                
                bool30 = allowtohost_dtpo2[5] == str(subnet_s.network_address)
                bool31 = allowtohost_dtpo2[4] == d_ip
                allowedtohost_dtpo2 = allowtohost_dtpo2[bool30 & bool31]
                
                bool32 = allowtohost_dtpo3[4] == str(subnet_s.network_address)
                allowedtohost_dtpo3 = allowtohost_dtpo3[bool32]
                
                if len(allowedtohost_dtpo) > 0 or len(allowedtohost_dtpo1) > 0:
                    continue
                elif len(allowedtohost_dtpo2) > 0:
                    for row in range(len(allowedtohost_dtpo2)):
                        if subnet_s == ip_network(f"{allowedtohost_dtpo2.loc[row][5]}/{allowedtohost_dtpo2.loc[row][6]}", strict = False) and \
                            allowedtohost_dtpo2.loc[row][4]==d_ip:
                                continue
                elif len(allowedtohost_dtpo3) > 0:
                    for row in range(len(allowedtohost_dtpo3)):
                        row_subnet = ip_network(f"{allowedtohost_dtpo3.loc[row][4]}/{allowedtohost_dtpo3.loc[row][5]}", strict = False)
                        if int(str(row_subnet).split('/')[-1]) > int(str(subnet_s).split('/')[-1]):
                            if row_subnet in list(subnet_s.subnets(new_prefix=int(str(row_subnet).split('/')[-1]))):
                                if IPv4Address(f"{s_ip}") in row_subnet:
                                    continue
                                else: pass
                            else: pass
                        else: pass
                else:
                    print(f"permit ip host {d_ip} host {s_ip}")
                    acl_entries_out.append(f"permit ip host {d_ip} host {s_ip}")                    
        print('\n')
        
    return [acl_entries_in, acl_entries_out]             
        
                                                                                                       
def subtosub(dtpo1, dtpo3, subnet_s, subnet_d):
    comm_presence = {'in_acl_comm' : 'not_present', 'out_acl_comm': 'not_present'}                                                                                                     
    for index, df in enumerate([dtpo1, dtpo3]):
        if type(df)==type(pd.DataFrame([])) and index==0:
            bool1 = df[3] == "any"
            bool2 = df[4] != "any"
            bool3 = df[4] != "host"
            bool4 = df[4] != "eq"
            allow_dtpo = df[bool1 & bool2 & bool3 & bool4]
            
            bool5 = allow_dtpo[4] == str(subnet_d.network_address)
            allowed_dtpo = allow_dtpo[bool5]
            allowed_dtpo = allowed_dtpo.reset_index(drop=True)
            
            bool6 = df[3] != "any"
            bool7 = df[3] != "host"
            bool8 = df[5] != "any"
            bool9 = df[5] != "host"             
            allow_dtpo1 = df[bool6 & bool7 & bool8 & bool9]

            bool10 = allow_dtpo1[3] == str(subnet_s.network_address)
            bool11 = allow_dtpo1[5] == str(subnet_d.network_address)
            allowed_dtpo1 = allow_dtpo1[bool10 & bool11]
            allowed_dtpo1 = allowed_dtpo1.reset_index(drop=True)
            
            bool12 = df[3] != "any"
            bool13 = df[3] != "host"
            bool14 = df[4] != "any"
            bool15 = df[4] != "host"
            bool16 = df[5] == "any"
            bool22 = df[6].isnull()
            allow_dtpo2 = df[bool12 & bool13 & bool14 & bool15 & bool16 & bool22]

            bool17 = allow_dtpo2[3] == str(subnet_s.network_address)
            allowed_dtpo2 = allow_dtpo2[bool17]
            allowed_dtpo2 = allowed_dtpo2.reset_index(drop=True)
            
            bool18 = df[3] == "any"
            bool19 = df[4] == "any"
            allow_dtpo3 = df[bool18 & bool19]

            bool20 = allow_dtpo3[5] != "eq"
            bool21 = allow_dtpo3[5].isnull()
            allowed_dtpo3 = allow_dtpo3[bool20 | bool21]
            allowed_dtpo3 = allowed_dtpo3.reset_index(drop=True)
            
            if len(allowed_dtpo) > 0:
                for row in range(len(allowed_dtpo)):
                    if subnet_d == ip_network(f"{allowed_dtpo.loc[row][4]}/{allowed_dtpo.loc[row][5]}", strict = False):
                        print(f"There is already existing in-comm between these two subnets: {subnet_s} and {subnet_d}")
                        comm_presence['in_acl_comm'] = 'exists'
                    else: pass
            if len(allowed_dtpo1) > 0:
                for row in range(len(allowed_dtpo1)):
                    if subnet_s == ip_network(f"{allowed_dtpo1.loc[row][3]}/{allowed_dtpo1.loc[row][4]}", strict = False) and \
                        subnet_d == ip_network(f"{allowed_dtpo1.loc[row][5]}/{allowed_dtpo1.loc[row][6]}", strict = False):
                            print(f"There is already existing in-comm between these two subnets: {subnet_s} and {subnet_d}")
                            comm_presence['in_acl_comm'] = 'exists'
                    else: pass
            if len(allowed_dtpo2) > 0:
                for row in range(len(allowed_dtpo2)):
                    if subnet_s == ip_network(f"{allowed_dtpo2.loc[row][3]}/{allowed_dtpo2.loc[row][4]}", strict = False):
                        print(f"There is already existing in-comm between these two subnets: {subnet_s} and {subnet_d}")
                        comm_presence['in_acl_comm'] = 'exists'
                    else: pass
            if len(allowed_dtpo3) > 0:
                for row in range(len(allowed_dtpo3)):
                    if allowed_dtpo3.loc[row][1]=="permit" and allowed_dtpo3.loc[row][2]=="ip":
                        print(f"There is already existing in-comm between these two subnets: {subnet_s} and {subnet_d}")
                        comm_presence['in_acl_comm'] = 'exists'
                    else: pass                

        elif type(df)==type(pd.DataFrame([])) and index==1:
            bool1 = df[5] == "any"
            bool2 = df[3] != "any"
            bool3 = df[3] != "host"
            bool4 = df[6] != "eq"
            allow_dtpo = df[bool1 & bool2 & bool3 & bool4]

            bool5 = allow_dtpo[3] == str(subnet_d.network_address)
            allowed_dtpo = allow_dtpo[bool5]
            allowed_dtpo = allowed_dtpo.reset_index(drop=True)
            
            bool6 = df[3] != "any"
            bool7 = df[3] != "host"
            bool8 = df[5] != "any"
            bool9 = df[5] != "host"             
            allow_dtpo1 = df[bool6 & bool7 & bool8 & bool9]


            bool10 = allow_dtpo1[3] == str(subnet_d.network_address)
            bool11 = allow_dtpo1[5] == str(subnet_s.network_address)
            allowed_dtpo1 = allow_dtpo1[bool10 & bool11]
            allowed_dtpo1 = allowed_dtpo1.reset_index(drop=True)
            
            bool12 = df[4] != "any"
            bool13 = df[4] != "host"
            bool14 = df[5] != "any"
            bool15 = df[5] != "host"
            bool16 = df[3] == "any"
            bool22 = df[6].isnull()
            allow_dtpo2 = df[bool12 & bool13 & bool14 & bool15 & bool16 & bool22]

            bool17 = allow_dtpo2[4] == str(subnet_s.network_address)
            allowed_dtpo2 = allow_dtpo2[bool17]
            allowed_dtpo2 = allowed_dtpo2.reset_index(drop=True)
            
            bool18 = df[3] == "any"
            bool19 = df[4] == "any"
            allow_dtpo3 = df[bool18 & bool19]

            bool20 = allow_dtpo3[5] != "eq"
            bool21 = allow_dtpo3[5].isnull()
            allowed_dtpo3 = allow_dtpo3[bool20 | bool21]
            allowed_dtpo3 = allowed_dtpo3.reset_index(drop=True)
            
            if len(allowed_dtpo) > 0:
                for row in range(len(allowed_dtpo)):
                    if subnet_d == ip_network(f"{allowed_dtpo.loc[row][3]}/{allowed_dtpo.loc[row][4]}", strict = False):
                        print(f"There is already existing out-comm between these two subnets: {subnet_s} and {subnet_d}")
                        comm_presence['out_acl_comm'] = 'exists'              
                    else: pass
            if len(allowed_dtpo1) > 0:
                for row in range(len(allowed_dtpo1)):
                    if subnet_s == ip_network(f"{allowed_dtpo1.loc[row][5]}/{allowed_dtpo1.loc[row][6]}", strict = False) and \
                        subnet_d == ip_network(f"{allowed_dtpo1.loc[row][3]}/{allowed_dtpo1.loc[row][4]}", strict = False):
                            print(f"There is already existing out-comm between these two subnets: {subnet_s} and {subnet_d}")
                            comm_presence['out_acl_comm'] = 'exists'
                    else: pass
            if len(allowed_dtpo2) > 0:
                for row in range(len(allowed_dtpo2)):
                    if subnet_s == ip_network(f"{allowed_dtpo2.loc[row][4]}/{allowed_dtpo2.loc[row][5]}", strict = False):
                        print(f"There is already existing out-comm between these two subnets: {subnet_s} and {subnet_d}")
                        comm_presence['out_acl_comm'] = 'exists'
                    else: pass
            if len(allowed_dtpo3) > 0:
                for row in range(len(allowed_dtpo3)):
                    if allowed_dtpo3.loc[row][1]=="permit" and allowed_dtpo3.loc[row][2]=="ip":
                        print(f"There is already existing out-comm between these two subnets: {subnet_s} and {subnet_d}")
                        comm_presence['out_acl_comm'] = 'exists'
                    else: pass   
    return comm_presence

def ipaclchecker(sources_grouped_details, destinations_grouped_details, direction):
    print(f"Lets do the ACL entries checking from {direction} subnets..\n")  
    subnets_entries = {}                          
    for group_s, detail_s in sources_grouped_details.items():
        subnet_s = ip_network(f"{detail_s['group_subnet_svi'][0]}/{detail_s['group_subnet_svi'][1]}", strict = False)
        subnet_s_str = str(subnet_s)
        lthree_connection = reachability(detail_s['group_L3'])
        primary_l3 = lthree_connection.find_prompt().replace("#", "")
        subnets_entries[subnet_s_str] = {'in_acls' : [], 'in_numbering' : [], 'in_acl_name' : '',  'out_acls' : [], \
                                         'out_numbering' : [], 'out_acl_name' : '', 'subnet_primary' : primary_l3}
        
        entries_in, entries_out, dtpo, dtpo1, dtpo2, dtpo3 = '', '', '', '', '', ''
        
        if detail_s['group_acls']['in']!='not_present':
            entries_in = lthree_connection.send_command(f"sh ip access-lists {detail_s['group_acls']['in']}")
            entries_in_list = entries_in.splitlines()
    
            dtpo = pd.DataFrame(entries_in_list)
            list1 = dtpo.values[0][0].split()
            dtpo1 = pd.DataFrame(list1).T
    
            for i in range(1,len(entries_in_list)):
                xx = dtpo.values[i][0].split()
                
                for j in range(len(xx)):
                    dtpo1.loc[i, j] = xx[j] 
            dtpo1 = dtpo1.reset_index(drop=True)
            subnets_entries[subnet_s_str]['in_numbering'].append(dtpo1.iloc[[-3, -2, -1]].reset_index(drop=True).loc[0, 0])
            subnets_entries[subnet_s_str]['in_numbering'].append(dtpo1.iloc[[-3, -2, -1]].reset_index(drop=True).loc[1, 0])
            subnets_entries[subnet_s_str]['in_numbering'].append(dtpo1.iloc[[-3, -2, -1]].reset_index(drop=True).loc[2, 0])
            subnets_entries[subnet_s_str]['in_acl_name'] = detail_s['group_acls']['in']
        elif detail_s['group_acls']['in']=='not_present':
            entries_in = 'not_present'
            dtpo1 = 'not_present'
            print(f"ACL-in entries not required between {subnet_s} and destination subnets.\n")
        
        if detail_s['group_acls']['out']!='not_present':
            entries_out = lthree_connection.send_command(f"sh ip access-lists {detail_s['group_acls']['out']}")
            entries_out_list = entries_out.splitlines()
    
            dtpo2 = pd.DataFrame(entries_out_list)
            list1 = dtpo2.values[0][0].split()
            dtpo3 = pd.DataFrame(list1).T
    
            for i in range(1,len(entries_out_list)):
                xx = dtpo2.values[i][0].split()
                
                for j in range(len(xx)):
                    dtpo3.loc[i, j] = xx[j] 
            dtpo3 = dtpo3.reset_index(drop=True)
            subnets_entries[subnet_s_str]['out_numbering'].append(dtpo3.iloc[[-3, -2, -1]].reset_index(drop=True).loc[0, 0])
            subnets_entries[subnet_s_str]['out_numbering'].append(dtpo3.iloc[[-3, -2, -1]].reset_index(drop=True).loc[1, 0])
            subnets_entries[subnet_s_str]['out_numbering'].append(dtpo3.iloc[[-3, -2, -1]].reset_index(drop=True).loc[2, 0])
            subnets_entries[subnet_s_str]['out_acl_name'] = detail_s['group_acls']['out']
        elif detail_s['group_acls']['out']=='not_present':
            entries_out = 'not_present'
            dtpo3 = 'not_present'
            print(f"ACL-out entries not required between {subnet_s} and destination subnets.\n")
        
        for group_d, detail_d in destinations_grouped_details.items():       
            subnet_d = ip_network(f"{detail_d['group_subnet_svi'][0]}/{detail_d['group_subnet_svi'][1]}", strict = False)
            
            from_subtosub, from_hosttohost = '', ''
            if entries_in!='not_present' and entries_out!='not_present':
                from_subtosub = subtosub(dtpo1, dtpo3, subnet_s, subnet_d)
            elif entries_in!='not_present' and entries_out=='not_present':
                from_subtosub = subtosub(dtpo1, dtpo3, subnet_s, subnet_d)
            elif entries_in=='not_present' and entries_out!='not_present':
                from_subtosub = subtosub(dtpo1, dtpo3, subnet_s, subnet_d)
            elif entries_in=='not_present' and entries_out=='not_present':
                break
            
            print(f"Comm between the {subnet_s} and {subnet_d} subnets for in and out ACLs:\n", from_subtosub, '\n')
            
            if from_subtosub['in_acl_comm']=='exists' and from_subtosub['out_acl_comm']=='exists':
                print(f"Moving on to the next step as all comms already allowed between {subnet_s} and {subnet_d}..")
                continue
            elif from_subtosub['in_acl_comm']=='not_present' and from_subtosub['out_acl_comm']=='not_present':
                from_hosttohost = hosttohost(dtpo1, dtpo3, from_subtosub['in_acl_comm'], from_subtosub['out_acl_comm'], group_s, group_d, subnet_s)
            elif from_subtosub['in_acl_comm']=='exists' and from_subtosub['out_acl_comm']=='not_present':
                from_hosttohost = hosttohost(dtpo1, dtpo3, from_subtosub['in_acl_comm'], from_subtosub['out_acl_comm'], group_s, group_d, subnet_s)
            elif from_subtosub['in_acl_comm']=='not_present' and from_subtosub['out_acl_comm']=='exists':
                from_hosttohost = hosttohost(dtpo1, dtpo3, from_subtosub['in_acl_comm'], from_subtosub['out_acl_comm'], group_s, group_d, subnet_s)
            else: print('new variety seen at ip_aclchecker, contact designer.')
            
            if len(from_hosttohost[0]) > 0 and len(from_hosttohost[-1]) > 0:
                [subnets_entries[subnet_s_str]['in_acls'].append(x) for x in from_hosttohost[0]]
                [subnets_entries[subnet_s_str]['out_acls'].append(x) for x in from_hosttohost[-1]]
            elif len(from_hosttohost[0]) > 0 and len(from_hosttohost[-1]) == 0:
                [subnets_entries[subnet_s_str]['in_acls'].append(x) for x in from_hosttohost[0]]
            elif len(from_hosttohost[0]) == 0 and len(from_hosttohost[-1]) > 0:
                [subnets_entries[subnet_s_str]['out_acls'].append(x) for x in from_hosttohost[-1]]
            elif len(from_hosttohost[0]) == 0 and len(from_hosttohost[-1]) == 0:
                continue
            
    return subnets_entries
    
        
        
        
        

        



