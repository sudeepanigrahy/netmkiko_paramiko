import pandas as pd

def ipcsvcreator(from_ip_aclchecker_s_to_d, from_ip_aclchecker_d_to_s, Source_IPs, Destination_IPs, Down_Source_IPs, Down_Dest_IPs, ticket_no):
    dtpo = pd.DataFrame(columns = ["Source_IPs", "Destination_IPs", "Down_Source_IPs", "Down_Dest_IPs", "Implementations:", "Rollbacks:"])
    dtpo_L3s = pd.read_csv("redundants.csv")
    
    for i, j in enumerate(Source_IPs):
        dtpo.loc[i, "Source_IPs"] = j
    
    for i, j in enumerate(Destination_IPs):
        dtpo.loc[i, "Destination_IPs"] = j
        
    for i, j in enumerate(Down_Source_IPs):
        dtpo.loc[i, "Down_Source_IPs"] = j
    
    for i, j in enumerate(Down_Dest_IPs):
        dtpo.loc[i, "Down_Dest_IPs"] = j
    
    Implementations_Column = []
    for i in [from_ip_aclchecker_s_to_d, from_ip_aclchecker_d_to_s]:
        for kee, val in i.items():
            mask = dtpo_L3s['switchname'] == val['subnet_primary'].lower()
            find = dtpo_L3s[mask]
            subnet_secondary = list(dtpo_L3s.iloc[int(str(list(find.index.values)[0]))+1].values)[0]
            
            if len(val['in_acls']) > 0 and len(val['out_acls']) > 0:
                reqd_in_diff = int(val['in_numbering'][1]) - int(val['in_numbering'][0])
                reqd_in_gap = len(val['in_acls'])*(reqd_in_diff)
                reqd_out_diff = int(val['out_numbering'][1]) - int(val['out_numbering'][0])
                reqd_out_gap = len(val['out_acls'])*(reqd_out_diff)
                if (int(val['in_numbering'][-1]) - int(val['in_numbering'][-2])) > 2*(reqd_in_gap) and \
                    (int(val['out_numbering'][-1]) - int(val['out_numbering'][-2])) > 2*(reqd_out_gap):
                    Implementations_Column.append(f"{val['subnet_primary']}/{subnet_secondary}")
                    Implementations_Column.append("config t")
                    Implementations_Column.append(f"ip access-list extended {val['in_acl_name']}")
                    Implementations_Column.append(f"remark {ticket_no}")
                    #[Implementations_Column.append(f"{int(val['in_numbering'][-2])+reqd_in_diff} {x}") for x in val['in_acls']]
                    for n, x in enumerate(val['in_acls']):
                        Implementations_Column.append(f"{int(val['in_numbering'][-2])+(n+1)*reqd_in_diff} {x}")
                    Implementations_Column.append("exit")
                    Implementations_Column.append(f"ip access-list extended {val['out_acl_name']}")
                    Implementations_Column.append(f"remark {ticket_no}")
                    #[Implementations_Column.append(f"{int(val['out_numbering'][-2])+reqd_out_diff} {x}") for x in val['out_acls']]
                    for n, x in enumerate(val['out_acls']):
                        Implementations_Column.append(f"{int(val['out_numbering'][-2])+(n+1)*reqd_out_diff} {x}")
                    Implementations_Column.append('end')
                    Implementations_Column.append('wr')       
                    Implementations_Column.append("")
                elif (int(val['in_numbering'][-1]) - int(val['in_numbering'][-2])) <= 2*(reqd_in_gap) and \
                    (int(val['out_numbering'][-1]) - int(val['out_numbering'][-2])) <= 2*(reqd_out_gap):
                        Implementations_Column.append(f"{val['subnet_primary']}/{subnet_secondary}")
                        Implementations_Column.append("config t")
                        Implementations_Column.append(f"ip access-list extended {val['in_acl_name']}")
                        Implementations_Column.append(f"remark {ticket_no}")
                        Implementations_Column.append(f"no {val['in_numbering'][-1]}")
                        Implementations_Column.append(f"{int(val['in_numbering'][-1])+10*reqd_in_gap} deny ip any any")
                        #[Implementations_Column.append(f"{int(val['in_numbering'][-2])+reqd_in_diff} {x}") for x in val['in_acls']]
                        for n, x in enumerate(val['in_acls']):
                            Implementations_Column.append(f"{int(val['in_numbering'][-2])+(n+1)*reqd_in_diff} {x}")
                        Implementations_Column.append("exit")
                        Implementations_Column.append(f"ip access-list extended {val['out_acl_name']}")
                        Implementations_Column.append(f"remark {ticket_no}")
                        Implementations_Column.append(f"no {val['out_numbering'][-1]}")
                        Implementations_Column.append(f"{int(val['out_numbering'][-1])+10*reqd_out_gap} deny ip any any")
                        #[Implementations_Column.append(f"{int(val['out_numbering'][-2])+reqd_out_diff} {x}") for x in val['out_acls']]
                        for n, x in enumerate(val['out_acls']):
                            Implementations_Column.append(f"{int(val['out_numbering'][-2])+(n+1)*reqd_out_diff} {x}")
                        Implementations_Column.append('end')
                        Implementations_Column.append('wr')       
                        Implementations_Column.append("")
                elif (int(val['in_numbering'][-1]) - int(val['in_numbering'][-2])) > 2*(reqd_in_gap) and \
                    (int(val['out_numbering'][-1]) - int(val['out_numbering'][-2])) <= 2*(reqd_out_gap):
                        Implementations_Column.append(f"{val['subnet_primary']}/{subnet_secondary}")
                        Implementations_Column.append("config t")
                        Implementations_Column.append(f"ip access-list extended {val['in_acl_name']}")
                        Implementations_Column.append(f"remark {ticket_no}")
                        #[Implementations_Column.append(f"{int(val['in_numbering'][-2])+reqd_in_diff} {x}") for x in val['in_acls']]
                        for n, x in enumerate(val['in_acls']):
                            Implementations_Column.append(f"{int(val['in_numbering'][-2])+(n+1)*reqd_in_diff} {x}")
                        Implementations_Column.append("exit")
                        Implementations_Column.append(f"ip access-list extended {val['out_acl_name']}")
                        Implementations_Column.append(f"remark {ticket_no}")
                        Implementations_Column.append(f"no {val['out_numbering'][-1]}")
                        Implementations_Column.append(f"{int(val['out_numbering'][-1])+10*reqd_out_gap} deny ip any any")
                        #[Implementations_Column.append(f"{int(val['out_numbering'][-2])+reqd_out_diff} {x}") for x in val['out_acls']]
                        for n, x in enumerate(val['out_acls']):
                            Implementations_Column.append(f"{int(val['out_numbering'][-2])+(n+1)*reqd_out_diff} {x}")
                        Implementations_Column.append('end')
                        Implementations_Column.append('wr')       
                        Implementations_Column.append("")
                elif (int(val['in_numbering'][-1]) - int(val['in_numbering'][-2])) <= 2*(reqd_in_gap) and \
                    (int(val['out_numbering'][-1]) - int(val['out_numbering'][-2])) > 2*(reqd_out_gap):
                        Implementations_Column.append(f"{val['subnet_primary']}/{subnet_secondary}")
                        Implementations_Column.append("config t")
                        Implementations_Column.append(f"ip access-list extended {val['in_acl_name']}")
                        Implementations_Column.append(f"remark {ticket_no}")
                        Implementations_Column.append(f"no {val['in_numbering'][-1]}")
                        Implementations_Column.append(f"{int(val['in_numbering'][-1])+10*reqd_in_gap} deny ip any any")
                        #[Implementations_Column.append(f"{int(val['in_numbering'][-2])+reqd_in_diff} {x}") for x in val['in_acls']]
                        for n, x in enumerate(val['in_acls']):
                            Implementations_Column.append(f"{int(val['in_numbering'][-2])+(n+1)*reqd_in_diff} {x}")
                        Implementations_Column.append("exit")
                        Implementations_Column.append(f"ip access-list extended {val['out_acl_name']}")
                        Implementations_Column.append(f"remark {ticket_no}")
                        #[Implementations_Column.append(f"{int(val['out_numbering'][-2])+reqd_out_diff} {x}") for x in val['out_acls']]
                        for n, x in enumerate(val['out_acls']):
                            Implementations_Column.append(f"{int(val['out_numbering'][-2])+(n+1)*reqd_out_diff} {x}")
                        Implementations_Column.append('end')
                        Implementations_Column.append('wr')       
                        Implementations_Column.append("")
            elif len(val['in_acls']) > 0 and len(val['out_acls']) == 0:
                reqd_in_diff = int(val['in_numbering'][1]) - int(val['in_numbering'][0])
                reqd_in_gap = len(val['in_acls'])*(reqd_in_diff)
                if (int(val['in_numbering'][-1]) - int(val['in_numbering'][-2])) > 2*(reqd_in_gap):
                    Implementations_Column.append(f"{val['subnet_primary']}/{subnet_secondary}")
                    Implementations_Column.append("config t")
                    Implementations_Column.append(f"ip access-list extended {val['in_acl_name']}")
                    Implementations_Column.append(f"remark {ticket_no}")
                    #[Implementations_Column.append(f"{int(val['in_numbering'][-2])+reqd_in_diff} {x}") for x in val['in_acls']]
                    for n, x in enumerate(val['in_acls']):
                        Implementations_Column.append(f"{int(val['in_numbering'][-2])+(n+1)*reqd_in_diff} {x}")
                    Implementations_Column.append('end')
                    Implementations_Column.append('wr')       
                    Implementations_Column.append("")
                elif (int(val['in_numbering'][-1]) - int(val['in_numbering'][-2])) <= 2*(reqd_in_gap):
                    Implementations_Column.append(f"{val['subnet_primary']}/{subnet_secondary}")
                    Implementations_Column.append("config t")
                    Implementations_Column.append(f"ip access-list extended {val['in_acl_name']}")
                    Implementations_Column.append(f"remark {ticket_no}")
                    Implementations_Column.append(f"no {val['in_numbering'][-1]}")
                    Implementations_Column.append(f"{int(val['in_numbering'][-1])+10*reqd_in_gap} deny ip any any")
                    #[Implementations_Column.append(f"{int(val['in_numbering'][-2])+reqd_in_diff} {x}") for x in val['in_acls']]
                    for n, x in enumerate(val['in_acls']):
                        Implementations_Column.append(f"{int(val['in_numbering'][-2])+(n+1)*reqd_in_diff} {x}")
                    Implementations_Column.append('end')
                    Implementations_Column.append('wr')       
                    Implementations_Column.append("")
            elif len(val['in_acls']) == 0 and len(val['out_acls']) > 0:
                reqd_out_diff = int(val['out_numbering'][1]) - int(val['out_numbering'][0])
                reqd_out_gap = len(val['out_acls'])*(reqd_out_diff)
                if (int(val['out_numbering'][-1]) - int(val['out_numbering'][-2])) > 2*(reqd_out_gap):
                    Implementations_Column.append(f"{val['subnet_primary']}/{subnet_secondary}")
                    Implementations_Column.append("config t")
                    Implementations_Column.append(f"ip access-list extended {val['out_acl_name']}")
                    Implementations_Column.append(f"remark {ticket_no}")
                    #[Implementations_Column.append(f"{int(val['out_numbering'][-2])+reqd_out_diff} {x}") for x in val['out_acls']]
                    for n, x in enumerate(val['out_acls']):
                        Implementations_Column.append(f"{int(val['out_numbering'][-2])+(n+1)*reqd_out_diff} {x}")
                    Implementations_Column.append('end')
                    Implementations_Column.append('wr')       
                    Implementations_Column.append("")
                elif (int(val['out_numbering'][-1]) - int(val['out_numbering'][-2])) <= 2*(reqd_out_gap):
                    Implementations_Column.append(f"{val['subnet_primary']}/{subnet_secondary}")
                    Implementations_Column.append("config t")
                    Implementations_Column.append(f"ip access-list extended {val['out_acl_name']}")
                    Implementations_Column.append(f"remark {ticket_no}")
                    Implementations_Column.append(f"no {val['out_numbering'][-1]}")
                    Implementations_Column.append(f"{int(val['out_numbering'][-1])+10*reqd_out_gap} deny ip any any")
                    #[Implementations_Column.append(f"{int(val['out_numbering'][-2])+reqd_out_diff} {x}") for x in val['out_acls']]
                    for n, x in enumerate(val['out_acls']):
                        Implementations_Column.append(f"{int(val['out_numbering'][-2])+(n+1)*reqd_out_diff} {x}")
                    Implementations_Column.append('end')
                    Implementations_Column.append('wr')       
                    Implementations_Column.append("")
                                    
    Rollbacks_Column = []
    for i in [from_ip_aclchecker_s_to_d, from_ip_aclchecker_d_to_s]:
        for kee, val in i.items():
            mask = dtpo_L3s['switchname'] == val['subnet_primary'].lower()
            find = dtpo_L3s[mask]
            subnet_secondary = list(dtpo_L3s.iloc[int(str(list(find.index.values)[0]))+1].values)[0]
            
            if len(val['in_acls']) > 0 and len(val['out_acls']) > 0:
                reqd_in_diff = int(val['in_numbering'][1]) - int(val['in_numbering'][0])
                reqd_in_gap = len(val['in_acls'])*(reqd_in_diff)
                reqd_out_diff = int(val['out_numbering'][1]) - int(val['out_numbering'][0])
                reqd_out_gap = len(val['out_acls'])*(reqd_in_diff)
                if (int(val['in_numbering'][-1]) - int(val['in_numbering'][-2])) > 2*(reqd_in_gap) and \
                    (int(val['out_numbering'][-1]) - int(val['out_numbering'][-2])) > 2*(reqd_out_gap):
                    Rollbacks_Column.append(f"{val['subnet_primary']}/{subnet_secondary}")
                    Rollbacks_Column.append("config t")
                    Rollbacks_Column.append(f"ip access-list extended {val['in_acl_name']}")
                    Rollbacks_Column.append(f"no remark {ticket_no}")
                    #[Rollbacks_Column.append(f"no {int(val['in_numbering'][-2])+reqd_in_diff} {x}") for x in val['in_acls']]
                    for n, x in enumerate(val['in_acls']):
                        Rollbacks_Column.append(f"no {int(val['in_numbering'][-2])+(n+1)*reqd_in_diff} {x}")
                    Rollbacks_Column.append("exit")
                    Rollbacks_Column.append(f"ip access-list extended {val['out_acl_name']}")
                    Rollbacks_Column.append(f"remark {ticket_no}")
                    #[Rollbacks_Column.append(f"no {int(val['out_numbering'][-2])+reqd_out_diff} {x}") for x in val['out_acls']]
                    for n, x in enumerate(val['out_acls']):
                        Rollbacks_Column.append(f"no {int(val['out_numbering'][-2])+(n+1)*reqd_out_diff} {x}")
                    Rollbacks_Column.append('end')
                    Rollbacks_Column.append('wr')       
                    Rollbacks_Column.append("")
                elif (int(val['in_numbering'][-1]) - int(val['in_numbering'][-2])) <= 2*(reqd_in_gap) and \
                    (int(val['out_numbering'][-1]) - int(val['out_numbering'][-2])) <= 2*(reqd_out_gap):
                        Rollbacks_Column.append(f"{val['subnet_primary']}/{subnet_secondary}")
                        Rollbacks_Column.append("config t")
                        Rollbacks_Column.append(f"ip access-list extended {val['in_acl_name']}")
                        Rollbacks_Column.append(f"no remark {ticket_no}")
                        #Rollbacks_Column.append(f"no {val['in_numbering'][-1]}")
                        #Rollbacks_Column.append(f"{int(val['in_numbering'][-1])+10*reqd_in_gap} deny ip any any")
                        #[Rollbacks_Column.append(f"no {int(val['in_numbering'][-2])+reqd_in_diff} {x}") for x in val['in_acls']]
                        for n, x in enumerate(val['in_acls']):
                            Rollbacks_Column.append(f"no {int(val['in_numbering'][-2])+(n+1)*reqd_in_diff} {x}")
                        Rollbacks_Column.append("exit")
                        Rollbacks_Column.append(f"ip access-list extended {val['out_acl_name']}")
                        Rollbacks_Column.append(f"remark {ticket_no}")
                        #Rollbacks_Column.append(f"no {val['out_numbering'][-1]}")
                        #Rollbacks_Column.append(f"{int(val['out_numbering'][-1])+10*reqd_out_gap} deny ip any any")
                        #[Rollbacks_Column.append(f"no {int(val['out_numbering'][-2])+reqd_out_diff} {x}") for x in val['out_acls']]
                        for n, x in enumerate(val['out_acls']):
                            Rollbacks_Column.append(f"no {int(val['out_numbering'][-2])+(n+1)*reqd_out_diff} {x}")
                        Rollbacks_Column.append('end')
                        Rollbacks_Column.append('wr')       
                        Rollbacks_Column.append("")
                elif (int(val['in_numbering'][-1]) - int(val['in_numbering'][-2])) > 2*(reqd_in_gap) and \
                    (int(val['out_numbering'][-1]) - int(val['out_numbering'][-2])) <= 2*(reqd_out_gap):
                        Rollbacks_Column.append(f"{val['subnet_primary']}/{subnet_secondary}")
                        Rollbacks_Column.append("config t")
                        Rollbacks_Column.append(f"ip access-list extended {val['in_acl_name']}")
                        Rollbacks_Column.append(f"no remark {ticket_no}")
                        #[Rollbacks_Column.append(f"no {int(val['in_numbering'][-2])+reqd_in_diff} {x}") for x in val['in_acls']]
                        for n, x in enumerate(val['in_acls']):
                            Rollbacks_Column.append(f"no {int(val['in_numbering'][-2])+(n+1)*reqd_in_diff} {x}")
                        Rollbacks_Column.append("exit")
                        Rollbacks_Column.append(f"ip access-list extended {val['out_acl_name']}")
                        Rollbacks_Column.append(f"no remark {ticket_no}")
                        #Rollbacks_Column.append(f"no {val['out_numbering'][-1]}")
                        #Rollbacks_Column.append(f"{int(val['out_numbering'][-1])+10*reqd_out_gap} deny ip any any")
                        #[Rollbacks_Column.append(f"no {int(val['out_numbering'][-2])+reqd_out_diff} {x}") for x in val['out_acls']]
                        for n, x in enumerate(val['out_acls']):
                            Rollbacks_Column.append(f"no {int(val['out_numbering'][-2])+(n+1)*reqd_out_diff} {x}")
                        Rollbacks_Column.append('end')
                        Rollbacks_Column.append('wr')       
                        Rollbacks_Column.append("")
                elif (int(val['in_numbering'][-1]) - int(val['in_numbering'][-2])) <= 2*(reqd_in_gap) and \
                    (int(val['out_numbering'][-1]) - int(val['out_numbering'][-2])) > 2*(reqd_out_gap):
                        Rollbacks_Column.append(f"{val['subnet_primary']}/{subnet_secondary}")
                        Rollbacks_Column.append("config t")
                        Rollbacks_Column.append(f"ip access-list extended {val['in_acl_name']}")
                        Rollbacks_Column.append(f"no remark {ticket_no}")
                        #Rollbacks_Column.append(f"no {val['in_numbering'][-1]}")
                        #Rollbacks_Column.append(f"{int(val['in_numbering'][-1])+10*reqd_in_gap} deny ip any any")
                        #[Rollbacks_Column.append(f"no {int(val['in_numbering'][-2])+reqd_in_diff} {x}") for x in val['in_acls']]
                        for n, x in enumerate(val['in_acls']):
                            Rollbacks_Column.append(f"no {int(val['in_numbering'][-2])+(n+1)*reqd_in_diff} {x}")
                        Rollbacks_Column.append("exit")
                        Rollbacks_Column.append(f"ip access-list extended {val['out_acl_name']}")
                        Rollbacks_Column.append(f"no remark {ticket_no}")
                        #[Rollbacks_Column.append(f"no {int(val['out_numbering'][-2])+reqd_out_diff} {x}") for x in val['out_acls']]
                        for n, x in enumerate(val['out_acls']):
                            Rollbacks_Column.append(f"no {int(val['out_numbering'][-2])+(n+1)*reqd_out_diff} {x}")
                        Rollbacks_Column.append('end')
                        Rollbacks_Column.append('wr')       
                        Rollbacks_Column.append("")
            elif len(val['in_acls']) > 0 and len(val['out_acls']) == 0:
                reqd_in_diff = int(val['in_numbering'][1]) - int(val['in_numbering'][0])
                reqd_in_gap = len(val['in_acls'])*(reqd_in_diff)
                if (int(val['in_numbering'][-1]) - int(val['in_numbering'][-2])) > 2*(reqd_in_gap):
                    Rollbacks_Column.append(f"{val['subnet_primary']}/{subnet_secondary}")
                    Rollbacks_Column.append("config t")
                    Rollbacks_Column.append(f"ip access-list extended {val['in_acl_name']}")
                    Rollbacks_Column.append(f"no remark {ticket_no}")
                    #[Rollbacks_Column.append(f"no {int(val['in_numbering'][-2])+reqd_in_diff} {x}") for x in val['in_acls']]
                    for n, x in enumerate(val['in_acls']):
                        Rollbacks_Column.append(f"no {int(val['in_numbering'][-2])+(n+1)*reqd_in_diff} {x}")
                    Rollbacks_Column.append('end')
                    Rollbacks_Column.append('wr')       
                    Rollbacks_Column.append("")
                elif (int(val['in_numbering'][-1]) - int(val['in_numbering'][-2])) <= 2*(reqd_in_gap):
                    Rollbacks_Column.append(f"{val['subnet_primary']}/{subnet_secondary}")
                    Rollbacks_Column.append("config t")
                    Rollbacks_Column.append(f"ip access-list extended {val['in_acl_name']}")
                    Rollbacks_Column.append(f"no remark {ticket_no}")
                    #Rollbacks_Column.append(f"no {val['in_numbering'][-1]}")
                    #Rollbacks_Column.append(f"{int(val['in_numbering'][-1])+10*reqd_in_gap} deny ip any any")
                    #[Rollbacks_Column.append(f"no {int(val['in_numbering'][-2])+reqd_in_diff} {x}") for x in val['in_acls']]
                    for n, x in enumerate(val['in_acls']):
                        Rollbacks_Column.append(f"no {int(val['in_numbering'][-2])+(n+1)*reqd_in_diff} {x}")
                    Rollbacks_Column.append('end')
                    Rollbacks_Column.append('wr')       
                    Rollbacks_Column.append("")
            elif len(val['in_acls']) == 0 and len(val['out_acls']) > 0:
                reqd_out_diff = int(val['out_numbering'][1]) - int(val['out_numbering'][0])
                reqd_out_gap = len(val['out_acls'])*(reqd_out_diff)
                if (int(val['out_numbering'][-1]) - int(val['out_numbering'][-2])) > 2*(reqd_out_gap):
                    Rollbacks_Column.append(f"{val['subnet_primary']}/{subnet_secondary}")
                    Rollbacks_Column.append("config t")
                    Rollbacks_Column.append(f"ip access-list extended {val['out_acl_name']}")
                    Rollbacks_Column.append(f"no remark {ticket_no}")
                    #[Rollbacks_Column.append(f"no {int(val['out_numbering'][-2])+reqd_out_diff} {x}") for x in val['out_acls']]
                    for n, x in enumerate(val['out_acls']):
                        Rollbacks_Column.append(f"no {int(val['out_numbering'][-2])+(n+1)*reqd_out_diff} {x}")
                    Rollbacks_Column.append('end')
                    Rollbacks_Column.append('wr')       
                    Rollbacks_Column.append("")
                elif (int(val['out_numbering'][-1]) - int(val['out_numbering'][-2])) <= 2*(reqd_out_gap):
                    Rollbacks_Column.append(f"{val['subnet_primary']}/{subnet_secondary}")
                    Rollbacks_Column.append("config t")
                    Rollbacks_Column.append(f"ip access-list extended {val['out_acl_name']}")
                    Rollbacks_Column.append(f"no remark {ticket_no}")
                    #Rollbacks_Column.append(f"no {val['out_numbering'][-1]}")
                    #Rollbacks_Column.append(f"{int(val['out_numbering'][-1])+10*reqd_out_gap} deny ip any any")
                    #[Rollbacks_Column.append(f"no {int(val['out_numbering'][-2])+reqd_out_diff} {x}") for x in val['out_acls']]
                    for n, x in enumerate(val['out_acls']):
                        Rollbacks_Column.append(f"no {int(val['out_numbering'][-2])+(n+1)*reqd_out_diff} {x}")
                    Rollbacks_Column.append('end')
                    Rollbacks_Column.append('wr')       
                    Rollbacks_Column.append("")
            else: pass
        
    for i,j in enumerate(Implementations_Column):
        dtpo.loc[i, "Implementations:"] = j
    
    for i,j in enumerate(Rollbacks_Column):
        dtpo.loc[i, "Rollbacks:"] = j       
    
    dtpo.to_csv(f"{ticket_no}.csv")
    
    return f'Output file {ticket_no}.csv is created in the working folder, please help to send it to L3 for approval.'