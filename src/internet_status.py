from __future__ import annotations

from src.constants import (
    APPLE_HOSTNAME,
    COM_SUFFIX,
    GOOGLE_HOSTNAME,
    LOCAL_ROUTER
)
from src.internet_status_util import create_url
from src.ping import Ping


class InternetStatus():

    def run_internet_status_check(self: InternetStatus) -> None:
        ping_test_results = self.run_ping_tests()

    def run_ping_tests(self: InternetStatus) -> dict:
        '''
        Runs a ping test against local router, www.google.com, and
        www.apple.com.  Returns a dictionary with parsed metrics for each host.
        Example return dictionary:
        {
            LOCAL_ROUTER: {
                'host': '192.168.86.1',
                'num_packets_sent': 10,
                'packet_loss_percent': 0.0,
                'max_round_trip_time': 30.101,
                'average_round_trip_time': 21.855,
                'able_to_resolve_host': True
            },
            google_url: {
                'host': 'www.google.com',
                'num_packets_sent': 10,
                'packet_loss_percent': 0.0,
                'max_round_trip_time': 30.101,
                'average_round_trip_time': 21.855,
                'able_to_resolve_host': True
            },
            apple_url: {
                'host': 'www.apple.com',
                'able_to_resolve_host': False
            }
        }
        '''
        ping_test_results = {}
        ping = Ping()

        router_response = \
            ping.ping_host_and_return_parsed_response(LOCAL_ROUTER, 100)
        ping_test_results[LOCAL_ROUTER] = router_response

        google_url = create_url(GOOGLE_HOSTNAME, COM_SUFFIX)
        google_response = \
            ping.ping_host_and_return_parsed_response(google_url, 100)
        ping_test_results[google_url] = google_response

        apple_url = create_url(APPLE_HOSTNAME, COM_SUFFIX)
        apple_response = \
            ping.ping_host_and_return_parsed_response(apple_url, 100)
        ping_test_results[apple_url] = apple_response

        return ping_test_results


if __name__ == "__main__":
    internet_status = InternetStatus()
    internet_status.run_internet_status_check()
