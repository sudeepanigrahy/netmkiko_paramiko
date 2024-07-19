import sys
import subprocess
import ipaddress

def ipchecker():
    
    with open("source.txt", "r") as sourcefiletypeobject:
        sources_list = list(set(sourcefiletypeobject.read().splitlines()))
    with open("destination.txt") as destinationfiletypeobject:
        destinations_list = list(set(destinationfiletypeobject.read().splitlines()))
    
    IPs_stripped_sources = []
    IPs_stripped_destinations = []
    IPs_corrected_sources = []
    IPs_corrected_destinations = []
    try:
        IPs_stripped_sources = list(set(list(map(lambda x: x.strip(), sources_list))))
        IPs_stripped_destinations = list(set(list(map(lambda x: x.strip(), destinations_list))))
        IPs_corrected_sources = list(map(lambda x: str(ipaddress.ip_address(x)), IPs_stripped_sources))
        IPs_corrected_destinations = list(map(lambda x: str(ipaddress.ip_address(x)), IPs_stripped_destinations))
    except ValueError as e:
        print(f"{e},", "please rectify it.")
        quit()
    except:
        print("Exception Occurred: ", sys.exc_info()[0])
    
    reachables_sources = []
    reachables_destinations = []
    unreachables_sources = []
    unreachables_destinations = []
    print('\nLets check the reachability of the IPs:\n')
    for index, l in enumerate([IPs_corrected_sources, IPs_corrected_destinations]):
        for i in l:
            try:
                output = subprocess.check_output(f"ping {i} -n 2", shell=True).decode('utf-8')
                if index == 0:
                    reachables_sources.append(i)
                elif index == 1:
                    reachables_destinations.append(i)
                print(output.splitlines()[2])
            except Exception as e:
                print(e)
                if index == 0:
                    unreachables_sources.append(i)
                elif index == 1:
                    unreachables_destinations.append(i)
    
    user = subprocess.check_output('echo %USERNAME%', shell=True).decode('utf-8').replace('\r\n', '')
    
    if unreachables_sources: 
        print(f"\nHi {user.capitalize()}, these IP/s are unreachable from the source side, please check with the user, or remove from the files and run code again:\n", unreachables_sources, '\n')
    
    if unreachables_destinations:
        print(f"\nHi {user.capitalize()}, these IP/s are unreachable from the destination side, please check with the user, or remove from the files and run code again:\n", unreachables_destinations, '\n')
        
        
    print(f"\nHi {user.capitalize()}, these below IPs are UP and Okay, but passing all the IPs(even unreachable ones, if any) to the next section:\n"+"\nSource_IPs:\n",\
                reachables_sources,"\n"+"Destination_IPs:\n",reachables_destinations, sep="")
    
    return (reachables_sources+unreachables_sources, reachables_destinations+unreachables_destinations, unreachables_sources, unreachables_destinations)




