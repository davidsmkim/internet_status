# Possible responses
SUCCESSFUL_RESPONSE = '''
PING www.google.com (172.217.6.68): 56 data bytes

--- www.google.com ping statistics ---
10 packets transmitted, 10 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 17.328/21.855/30.101/3.413 ms
'''

PACKET_LOSS_RESPONSE = '''
PING www.google.com (172.217.6.68): 56 data bytes

--- www.google.com ping statistics ---
8 packets transmitted, 1 packets received, 87.5% packet loss
round-trip min/avg/max/stddev = 38.466/38.466/38.466/0.000 ms
'''

UNABLE_TO_RESOLVE_HOST_RESPONSE = \
    'ping: cannot resolve www.google.com: Unknown host'

DESTINATION_HOST_UNREACHABLE_RESPONSE = '''
PING www.google.com (216.58.194.196): 56 data bytes
92 bytes from 73.162.229.233: Destination Host Unreachable
Vr HL TOS  Len   ID Flg  off TTL Pro  cks      Src      Dst
 4  5  00 5400 845f   0 0000  3f  01 44d7 192.168.86.203  216.58.194.196


--- www.google.com ping statistics ---
10 packets transmitted, 9 packets received, 10.0% packet loss
round-trip min/avg/max/stddev = 12.675/19.868/26.924/5.168 ms
'''

LOCAL_ROUTER_ISSUE_RESPONSE = \
    "Command '['ping', '-c', '10', '-q', '192.168.86.1']' returned " + \
    "non-zero exit status 2."

# Hosts
GOOGLE_HOST = 'www.google.com'
LOCAL_ROUTER_HOST = '192.168.86.1'
