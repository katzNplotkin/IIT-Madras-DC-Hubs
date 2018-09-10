#!/usr/bin/env python
# Checks status of IIT Madras Hubs

import nmap

# Get hub ip and corresponding ports from hublist.txt to variable hublist
with open('hublist.txt','r') as hublistfile:
    hublist=[line.split() for line in hublistfile]

# Check status of hubs using ping to port
nm=nmap.PortScanner()    # Init PortScanner object
with open('hubstat.txt','w') as hubstatfile:
    for hub in hublist:
        if hub:    # Handle empty lines
            if hub[0] !='#':    # Handle comments
                print(hub)
                hubName=hub[0]
                hubIP=hub[1]
                hubPort=hub[2]
                hubscan=nm.scan(hubIP,hubPort,arguments='-PN')  # Scan using nmap
                hubstatus=hubscan['scan'][hubIP]['status']['state']
                hubstate=hubscan['scan'][hubIP]['tcp'][int(hubPort)]['state'] 
                if (hubstatus=='up') and (hubstate=='open'):
                    hubmode='online'
                else:
                    hubmode='offline'
                hubstatfile.write(hubName+'\t'+hubIP+'\t'+hubPort+'\t'+hubmode+'\n')

