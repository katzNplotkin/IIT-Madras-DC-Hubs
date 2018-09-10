#!/usr/bin/env python
# Checks status of IIT Madras DC Hubs

import nmap
import datetime

# Get hub ip and corresponding ports from hublist.txt to variable hublist
with open('hublist.txt','r') as hublistfile:
    hublist=[line.split() for line in hublistfile]

# Check status of hubs using ping to port
nm=nmap.PortScanner()    # Init PortScanner object
with open('hubstat.txt','w') as hubstatfile:
    hubstatfile.write('Last Updated: {:%c}\n\n'.format(datetime.datetime.now()))
    for hub in hublist:
        if hub:    # Handle empty lines
            if hub[0] !='#':    # Handle comments
                hubName=hub[0]
                hubAddr=hub[1].split('://',1)[1]
                hubIP=hubAddr.split(':',1)[0]
                hubPort=hubAddr.split(':',1)[1]
                hubscan=nm.scan(hubIP,hubPort,arguments='-PN')  # Scan using nmap
                hubstatus=hubscan['scan'][hubIP]['status']['state']
                hubstate=hubscan['scan'][hubIP]['tcp'][int(hubPort)]['state'] 
                if (hubstatus=='up') and (hubstate=='open'):
                    hubmode='online'
                else:
                    hubmode='offline'
                hubstatfile.write(hubName+'\t'+hub[1]+'\t'+hubmode+'\n')

# Write to README file
readmeParts=['docs/README_head.md','hubstat.txt','docs/README_tail.md']
with open('docs/README.md','w') as readmeFile:
    for fname in readmeParts:
        with open(fname,'r') as infile:
            readmeFile.write(infile.read())
