#!/usr/bin/env python
# Checks status of IIT Madras DC Hubs

from nmap import PortScanner
from datetime import datetime


def getHubData(hubline):
    'Returns hub data extracted from list'
    name = hubline[0].strip()
    protocol = hubline[1].split('://', 1)[0].strip()
    addr = hubline[1].split('://', 1)[1].strip()
    ip = addr.split(':', 1)[0]
    port = addr.split(':', 1)[1]
    return [name, protocol, ip, port]


def getHubStat(psObj, ip, port):
    'Returns state and status after scanning using nmap'
    hubscan = psObj.scan(ip, port, arguments='-PN')  # Scan using nmap
    status = hubscan['scan'][ip]['status']['state']
    state = hubscan['scan'][ip]['tcp'][int(port)]['state']
    return [status, state]


# Get hub ip and corresponding ports from hublist.csv to variable hublist
with open('hublist.csv', 'r') as hublistfile:
    hublist = [line.split(',') for line in hublistfile]

# Check status of hubs using ping to port
psObj = PortScanner()    # Init PortScanner object
with open('hubstat.md', 'w') as hubstatfile:
    hubstatfile.write('## Last Updated: {:%c}  \n\n'.format(datetime.now()))
    hubstatfile.write('Hubs | Address | Status  \n')
    hubstatfile.write('--- | --- | ---  \n')
    for hubline in hublist:
        # Handle empty lines and comments
        if hubline and (hubline[0][0] != '#'):
            [name, protocol, ip, port] = getHubData(hubline)
            [status, state] = getHubStat(psObj, ip, port)
            mode = 'offline'    # Default assumption
            if (status == 'up'):
                if (state == 'open'):
                    mode = '**online**'
                else:
                    # Check alternate ports - 511, 1209
                    for altport in ['511', '1209']:
                        [status, state] = getHubStat(psObj, ip, altport)
                        if (state == 'open'):
                            port = altport
                            mode = '**online**'
            strout = name+'  |  '+protocol+'://'+ip+':'+port+'\t|'+mode+'   \n'
            hubstatfile.write(strout)

# Write to README file
readmeParts = ['docs/README_head.md', 'hubstat.md', 'docs/README_tail.md']
with open('docs/README.md', 'w') as readmeFile:
    for fname in readmeParts:
        with open(fname, 'r') as infile:
            readmeFile.write(infile.read())
