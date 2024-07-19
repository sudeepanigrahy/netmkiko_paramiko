import pandas as pd
from netmiko import ConnectHandler
from ip_reachability import reachability

def ipaclconfirmer(details):
    acls_apparent = details['group_acls']
    vlan_no = details['group_vlan_no.']
    lthree_connection = reachability(details['group_L3'])
        
    run_conf_acls = lthree_connection.send_command("sh access-lists | i Extended")
    run_conf_acls_list = run_conf_acls.splitlines()
    
    dtpo = pd.DataFrame(run_conf_acls_list)
    list1 = dtpo.values[0][0].split()
    dtpo1 = pd.DataFrame(list1).T
    
    for i in range(1,len(run_conf_acls_list)):
        xx = dtpo.values[i][0].split()
        
        for j in range(len(xx)):
            dtpo1.loc[i, j] = xx[j] 
    dtpo1 = dtpo1.reset_index(drop=True)
    
    xx, yy = [], []
    for i in list(dtpo1[4].values):
        xx = [x for x in list(dtpo1[4].values) if vlan_no in x and 'in' in x]
        yy = [y for y in list(dtpo1[4].values) if vlan_no in y and 'out' in y]
    
    xxx = xx
    yyy = yy
    for ind, acls_side in enumerate([xx, yy]):
        for acl in acls_side:
            spleet = acl.split(vlan_no)
            if spleet[0][-1].isdigit()==True and ind==0: xxx.remove(acl)
            elif spleet[-1][0].isdigit()==True and ind==0: xxx.remove(acl)
            elif spleet[0][-1].isdigit()==True and ind==1: yyy.remove(acl)
            elif spleet[-1][0].isdigit()==True and ind==1: yyy.remove(acl)
            else: continue
    
    acls_confirmed = {}
    for i, j in acls_apparent.items():
        if j in xxx: acls_confirmed[i] = j
        elif j in yyy: acls_confirmed[i] = j  
        elif j=="not_present" and i=='in' and len(xxx)==0: acls_confirmed[i] = j
        elif j=="not_present" and i=='out' and len(yyy)==0: acls_confirmed[i] = j
        elif j=="not_present" and i=='in' and len(xxx)==1: acls_confirmed[i] = xxx[0]
        elif j=="not_present" and i=='out' and len(yyy)==1: acls_confirmed[i] = yyy[0]
        else: print("There is a new variety for ACLs under a vlan, contact designer.")
    
    return acls_confirmed
    
def pre_ipaclconfirmer(x, y):
    sources_grouped_details = x
    destinations_grouped_details = y
    for index, details_side in enumerate([sources_grouped_details, destinations_grouped_details]):
        for kee, val in details_side.items():
            if index==0: sources_grouped_details[kee]['group_acls'] = ipaclconfirmer(val)
            elif index==1: destinations_grouped_details[kee]['group_acls'] = ipaclconfirmer(val)
            
    return (sources_grouped_details, destinations_grouped_details)