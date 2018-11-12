#!/usr/bin/env python
# Checks status of IIT Madras DC Hubs

import nmap
import datetime

def getHubData(hubline):
    'Returns hub data extracted from list'
    hubName = hub[0].strip()
    hubProtocol = hub[1].split('://', 1)[0].strip()
    hubAddr = hub[1].split('://', 1)[1].strip()
    hubIP = hubAddr.split(':', 1)[0]
    hubPort = hubAddr.split(':', 1)[1]
    return [hubName, hubProtocol, hubIP, hubPort]

def getHubStat(hubIP, hubPort):
    'Returns hubstate and hubstatus after scanning using nmap'
    hubscan = nm.scan(hubIP, hubPort, arguments='-PN')  # Scan using nmap
    hubstatus = hubscan['scan'][hubIP]['status']['state']
    hubstate = hubscan['scan'][hubIP]['tcp'][int(hubPort)]['state']
    return [hubstatus, hubstate]

# Get hub ip and corresponding ports from hublist.csv to variable hublist
with open('hublist.csv', 'r') as hublistfile:
    hublist = [line.split(',') for line in hublistfile]

# Check status of hubs using ping to port
nm = nmap.PortScanner()    # Init PortScanner object
with open('hubstat.md', 'w') as hubstatfile:
    hubstatfile.write('## Last Updated: {:%c}  \n\n'.format(datetime.datetime.now()))
    hubstatfile.write('Hubs | Address | Status  \n')
    hubstatfile.write('--- | --- | ---  \n')
    for hubline in hublist:
        if hubline:    # Handle empty lines
            if hubline[0][0] != '#':    # Handle comments
                [hubName, hubProtocol, hubIP, hubPort] = getHubData(hubline)
                print([hubName, hubProtocol, hubIP, hubPort])
                [hubstatus, hubstate] = getHubStat(hubIP, hubPort)
                hubmode = 'offline'    # Default assumption
                if (hubstatus == 'up'):
                    if (hubstate == 'open'):
                        hubmode = '**online**'
                    else:
                        # Check alternate ports - 511, 1209
                        for althubPort in ['511', '1209']:
                            [hubstatus, hubstate] = getHubStat(hubIP, althubPort)
                            if (hubstate == 'open'):
                                hubPort = althubPort
                                hubmode = '**online**'
                hubstatfile.write(hubName+'  |  '+hubProtocol+'://'+hubIP+':'+hubPort+'\t|'+hubmode+'   \n')

# Write to README file
#readmeParts = ['docs/README_head.md', 'hubstat.md', 'docs/README_tail.md']
#with open('docs/README.md', 'w') as readmeFile:
#    for fname in readmeParts:
#        with open(fname, 'r') as infile:
#            readmeFile.write(infile.read())
