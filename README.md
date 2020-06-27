# Internet Status

### Background
This project was created to help log and record my home's internet status.

After moving into a new home, I quickly noticed my internet connection was abysmal.  There were frequent times when my modem would reset, I would experience high packet loss, or experience ridiculously high latency.  After contacting my internet provider (over 30 phone calls and 5 technician visits), the issue was still not resolved.  The vast majority of the time, the support agents did not believe that I was facing any issue as whenever a technician came or the agents checked their signal on their end, everything looked good.

After much frustration, I decided to create this program to log my internet status in order to have definitive proof that my internet status was terrible.  Interestingly enough, this revealed that the problem was significantly worse than I had originally thought with my internet going down for hours at a time during the night.

After showing the next visiting technician the logs, the case was escalated multiple times until the issue was finally resolved. For the curious reader, it was a bad node in my neighborhood.  To be honest, I'm surprised that the ISP did not receive more calls from others in my neighborhood.

This project was run on a Raspberry Pi.  There is a plan to dockerize it in the future, but as the issue is now resolved, this has taken a back seat.

### Prerequisites
- Python3 is needed on the machine that this code is to be run on.
- A file called "sec_constants.py" in internet_status/src/ needs to be created.  Within this file, the following line must be added: (This will eventually be changed to use environment variables.)
```
LOCAL_ROUTER = '<local router ip>'
```

### Usage
Because this was to solve a quick issue, this project's deployment is rather crude.  In order to not limit our terminal, we run the command:
```
nohup python3 -m src.internet_status &
```
from within the root directory of the project.

This will create the following:
- internet_status/nohup.out - This file will print any statements from the script itself (including any crashes, which there hopefully aren't any of).
- ~/internet_status/ - This directory contains two log files:
   - internet_status.log - This file is the primary log.  If any issues arise, they will be logged in this file with their time and date.  Occasionally, a message stating that the internet status program is still running is logged to show that the program is still running in the absence of any errors.
   - internet_status_verbose.log - This file shows every call that is made to test the internet status as well as a brief summary of each call's status.
 
 A summary is also provided by executing the following command in the root directory of the project:
 ```
 python3 -m src.log_parser
 ```
 This summary parses the aforementioned internet_status.log file and displays any dates that had issues along with their counts.  If no issues arose on a given date, the date is absente from the resulting summary.

As the summary parses the aforementioned log file, this file obviously needs to exist.

### Other Notes
This program works by pinging two random hosts out of a list of hosts (currently comprised of www.apple.com, www.amazon.com, www.google.com). If there is no issue with the first host, we consider that a good result.  If there is any issue with the ping result, we ping the second host to double check that there isn't an issue with the first host.  If there is an issue with both hosts, we check the local router. Depending on the errors received from both hosts and the local router (if any), we log the most severe error. We deem the errors from most severe to least severe to be:
1. An issue with the local router
2. An issue with the modem or being unable to connect to the internet as a whole
3. Packet loss
4. High latency

### Usage Examples
This is what the program looks like while running.

internet_status.log with no errors:
```
Starting Log at: 06/03/20@00:51:20
06/03/20@01:07:45 - --- Internet Status Check Running ---
06/03/20@01:24:08 - --- Internet Status Check Running ---
06/03/20@01:40:31 - --- Internet Status Check Running ---
06/03/20@01:56:54 - --- Internet Status Check Running ---
```

internet_status.log with errors:
```
05/26/20@16:56:22 - 28.0% packet loss
05/26/20@16:58:54 - 48.0% packet loss
05/26/20@17:01:29 - 76.0% packet loss
05/26/20@17:04:05 - Cannot connect to internet: Modem down
05/26/20@17:05:16 - Cannot connect to internet: Modem down
05/26/20@17:06:45 - 80.0% packet loss
05/26/20@17:09:32 - Cannot connect to internet: Modem down
05/26/20@17:15:58 - 72.0% packet loss
05/26/20@17:18:34 - Cannot connect to internet: Modem down
05/26/20@17:19:45 - 60.0% packet loss
05/26/20@17:22:24 - 30.0% packet loss
05/26/20@17:25:01 - 94.0% packet loss
05/26/20@17:27:42 - 6.0% packet loss
05/26/20@17:30:14 - Cannot connect to internet: Modem down
05/26/20@17:32:05 - 6.0% packet loss
05/26/20@17:34:37 - --- Internet Status Check Running ---
05/26/20@17:34:37 - Cannot connect to internet: Modem down
05/26/20@17:36:35 - Cannot connect to internet: Modem down
05/26/20@17:44:19 - 42.0% packet loss
05/26/20@17:50:16 - 80.0% packet loss
05/26/20@18:00:15 - --- Internet Status Check Running ---
05/26/20@18:15:01 - Cannot connect to internet: Modem down
05/26/20@18:16:53 - Cannot connect to internet: Modem down
05/26/20@18:18:20 - --- Internet Status Check Running ---
05/26/20@18:19:09 - 10.0% packet loss
05/26/20@18:24:57 - 46.0% packet loss
```

internet_status_verbose.log
```
06/26/20@23:48:08 - --- Running Ping Test ---
06/26/20@23:48:57 - PING d3ag4hukkh62yn.cloudfront.net (13.35.125.224) 56(84) bytes of data.

--- d3ag4hukkh62yn.cloudfront.net ping statistics ---
50 packets transmitted, 50 received, 0% packet loss, time 126ms
rtt min/avg/max/mdev = 10.597/17.539/73.389/10.186 ms

06/26/20@23:48:57 - {'www.amazon.com': {'host': 'www.amazon.com', 'able_to_resolve_host': True, 'error': '', 'num_packets_sent': 50, 'packet_loss_percent': 0.0, 'average_round_trip_time': 17.539, 'max_round_trip_time': 73.389}}
06/26/20@23:48:57 - --- Running Ping Test ---
06/26/20@23:49:46 - PING e6858.dsce9.akamaiedge.net (184.51.49.16) 56(84) bytes of data.

--- e6858.dsce9.akamaiedge.net ping statistics ---
50 packets transmitted, 50 received, 0% packet loss, time 122ms
rtt min/avg/max/mdev = 10.423/15.540/34.310/4.374 ms

06/26/20@23:49:46 - {'www.apple.com': {'host': 'www.apple.com', 'able_to_resolve_host': True, 'error': '', 'num_packets_sent': 50, 'packet_loss_percent': 0.0, 'average_round_trip_time': 15.54, 'max_round_trip_time': 34.31}}
06/26/20@23:49:46 - --- Running Ping Test ---
06/26/20@23:50:35 - PING www.google.com (216.58.194.196) 56(84) bytes of data.

--- www.google.com ping statistics ---
50 packets transmitted, 50 received, 0% packet loss, time 121ms
rtt min/avg/max/mdev = 10.893/15.818/30.854/4.688 ms

06/26/20@23:50:35 - {'www.google.com': {'host': 'www.google.com', 'able_to_resolve_host': True, 'error': '', 'num_packets_sent': 50, 'packet_loss_percent': 0.0, 'average_round_trip_time': 15.818, 'max_round_trip_time': 30.854}}
```

summary
```
{'06/03/20': {'packet_loss': 0, 'round_trip_time': 5, 'modem_down': 0, 'router_down': 0}, '06/04/20': {'packet_loss': 0, 'round_trip_time': 7, 'modem_down': 0, 'router_down': 0}, '06/05/20': {'packet_loss': 0, 'round_trip_time': 1, 'modem_down': 0, 'router_down': 0}, '06/06/20': {'packet_loss': 0, 'round_trip_time': 2, 'modem_down': 0, 'router_down': 0}, '06/07/20': {'packet_loss': 0, 'round_trip_time': 11, 'modem_down': 0, 'router_down': 0}, '06/08/20': {'packet_loss': 1, 'round_trip_time': 1, 'modem_down': 0, 'router_down': 0}, '06/10/20': {'packet_loss': 1, 'round_trip_time': 0, 'modem_down': 0, 'router_down': 0}, '06/11/20': {'packet_loss': 0, 'round_trip_time': 3, 'modem_down': 3, 'router_down': 0}, '06/15/20': {'packet_loss': 0, 'round_trip_time': 1, 'modem_down': 0, 'router_down': 0}, '06/16/20': {'packet_loss': 0, 'round_trip_time': 1, 'modem_down': 0, 'router_down': 0}, '06/19/20': {'packet_loss': 0, 'round_trip_time': 1, 'modem_down': 0, 'router_down': 0}, '06/21/20': {'packet_loss': 0, 'round_trip_time': 0, 'modem_down': 0, 'router_down': 933}, '06/23/20': {'packet_loss': 1, 'round_trip_time': 2, 'modem_down': 0, 'router_down': 878}, '06/24/20': {'packet_loss': 0, 'round_trip_time': 1, 'modem_down': 0, 'router_down': 505}}
```
