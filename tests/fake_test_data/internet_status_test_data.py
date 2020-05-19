GOOGLE_SUCCESSFUL_RESPONSE = '''
PING www.google.com (172.217.6.68): 56 data bytes

--- www.google.com ping statistics ---
10 packets transmitted, 10 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 17.328/21.855/30.101/3.413 ms
'''

GOOGLE_PACKET_LOSS_RESPONSE = '''
PING www.google.com (172.217.6.68): 56 data bytes

--- www.google.com ping statistics ---
8 packets transmitted, 1 packets received, 87.5% packet loss
round-trip min/avg/max/stddev = 38.466/38.466/38.466/0.000 ms
'''

GOOGLE_ROUND_TRIP_TIME_ERROR_RESPONSE = '''
PING www.google.com (172.217.6.68): 56 data bytes

--- www.google.com ping statistics ---
8 packets transmitted, 8 packets received, 0% packet loss
round-trip min/avg/max/stddev = 100/100/100/0.000 ms
'''

GOOGLE_UNABLE_TO_RESOLVE_HOST_RESPONSE = \
    'ping: cannot resolve www.google.com: Unknown host'

GOOGLE_DESTINATION_HOST_UNREACHABLE_RESPONSE = '''
PING www.google.com (216.58.194.196): 56 data bytes
92 bytes from 73.162.229.233: Destination Host Unreachable
Vr HL TOS  Len   ID Flg  off TTL Pro  cks      Src      Dst
 4  5  00 5400 845f   0 0000  3f  01 44d7 192.168.86.203  216.58.194.196


--- www.google.com ping statistics ---
10 packets transmitted, 9 packets received, 10.0% packet loss
round-trip min/avg/max/stddev = 12.675/19.868/26.924/5.168 ms
'''

APPLE_SUCCESSFUL_RESPONSE = '''
PING www.apple.com (172.217.6.68): 56 data bytes

--- www.apple.com ping statistics ---
10 packets transmitted, 10 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 17.328/21.855/30.101/3.413 ms
'''

APPLE_PACKET_LOSS_RESPONSE = '''
PING www.apple.com (172.217.6.68): 56 data bytes

--- www.apple.com ping statistics ---
8 packets transmitted, 1 packets received, 90.0% packet loss
round-trip min/avg/max/stddev = 38.466/38.466/38.466/0.000 ms
'''

APPLE_ROUND_TRIP_TIME_ERROR_RESPONSE = '''
PING www.apple.com (172.217.6.68): 56 data bytes

--- www.google.com ping statistics ---
8 packets transmitted, 8 packets received, 0% packet loss
round-trip min/avg/max/stddev = 50/50/50/0.000 ms
'''

APPLE_UNABLE_TO_RESOLVE_HOST_RESPONSE = \
    'ping: cannot resolve www.apple.com: Unknown host'

APPLE_DESTINATION_HOST_UNREACHABLE_RESPONSE = '''
PING www.apple.com (216.58.194.196): 56 data bytes
92 bytes from 73.162.229.233: Destination Host Unreachable
Vr HL TOS  Len   ID Flg  off TTL Pro  cks      Src      Dst
 4  5  00 5400 845f   0 0000  3f  01 44d7 192.168.86.203  216.58.194.196


--- www.apple.com ping statistics ---
10 packets transmitted, 9 packets received, 10.0% packet loss
round-trip min/avg/max/stddev = 12.675/19.868/26.924/5.168 ms
'''

LOCAL_ROUTER_SUCCESSFUL_RESPONSE = '''
PING 192.168.86.1 (192.168.86.1): 56 data bytes

--- 192.168.86.1ping statistics ---
10 packets transmitted, 10 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 17.328/21.855/30.101/3.413 ms
'''

LOCAL_ROUTER_PACKET_LOSS_RESPONSE = '''
PING 192.168.86.1 (192.168.86.1): 56 data bytes

--- 192.168.86.1 ping statistics ---
8 packets transmitted, 1 packets received, 87.5% packet loss
round-trip min/avg/max/stddev = 38.466/38.466/38.466/0.000 ms
'''

LOCAL_ROUTER_ROUND_TRIP_TIME_ERROR_RESPONSE = '''
PING 192.168.86.1 (192.168.86.1): 56 data bytes

--- 192.168.86.1 ping statistics ---
8 packets transmitted, 8 packets received, 0% packet loss
round-trip min/avg/max/stddev = 100/100/100/0.000 ms
'''

COMMAND_EXIT_ISSUE_RESPONSE = \
    "Command '['ping', '-c', '10', '-q', '192.168.86.1']' returned " + \
    "non-zero exit status 2."
