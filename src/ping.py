from __future__ import annotations
import subprocess

from src.constants import (
    LOCAL_ROUTER,
    LOCAL_ROUTER_ERROR_MESSAGE,
    PING_COMMAND,
    PING_COUNT_OPTION,
    PING_QUIET_COMMAND,
    RESPONSE_KEY_HOST,
    RESPONSE_KEY_NUM_PACKETS_SENT,
    RESPONSE_KEY_PACKET_LOSS_PERCENT,
    RESPONSE_KEY_MAX_ROUND_TRIP_TIME,
    RESPONSE_KEY_AVERAGE_ROUND_TRIP_TIME,
    RESPONSE_KEY_ABLE_TO_RESOLVE_HOST
)


class Ping:

    def ping_host_and_return_parsed_response(
            self: Ping,
            url: str,
            num_pings: int) -> dict:
        '''
        Pings a given host and returns a parsed dictionary response.
        Returned dictionary has example format:
        {
            host: 'www.google.com',
            num_packets_sent: 10,
            packet_loss_percent: 5.0,
            max_round_trip_time: 3.723,
            average_round_trip_time: 2.123
            able_to_resolve_host: True
        }
        If ping is unsuccessful and unable to resolve host, the returned
        dictionary has the same format but with only the 'host' and the
        'able_to_resolve_host' field, which is False.
        '''
        response = self.ping_host(url, num_pings)
        parsed_ping_dict = self.parse_ping_response(url, response)
        return parsed_ping_dict

    def ping_host(self: Ping, url: str, num_pings: int) -> str:
        try:
            response = subprocess.check_output(
                [PING_COMMAND, PING_COUNT_OPTION, str(num_pings),
                 PING_QUIET_COMMAND, url],
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
        except subprocess.CalledProcessError as error:
            response = str(error)
        return response

    def parse_ping_response(self: Ping, url: str, response: str) -> dict:
        '''
        Parses an initial response into a dictionary with the parsed ping
        response.
        '''
        parsed_ping_dict = {
            RESPONSE_KEY_HOST: url,
            RESPONSE_KEY_ABLE_TO_RESOLVE_HOST: False
        }
        split_ping_response = response.splitlines()

        if url == LOCAL_ROUTER:
            # For local router, check if able to connect before moving on
            able_to_connect_to_router = \
                self.check_route_to_local_router_and_update_parsed_ping_dict(
                    split_ping_response, parsed_ping_dict)
            if not able_to_connect_to_router:
                return parsed_ping_dict
        else:
            ping_was_able_to_resolve_host = \
                self.determine_if_able_to_resolve_host(
                    url, split_ping_response)
            if not ping_was_able_to_resolve_host:
                return parsed_ping_dict

        parsed_ping_dict[RESPONSE_KEY_ABLE_TO_RESOLVE_HOST] = True

        # Parse appropriate metrics and update parsed_ping_dict
        ping_summary_response = split_ping_response[-2]
        self.parse_ping_summary_and_update_parsed_ping_dict(
            parsed_ping_dict, ping_summary_response)

        ping_timing_response = split_ping_response[-1]
        self.parse_ping_timing_and_update_parsed_ping_dict(
            parsed_ping_dict, ping_timing_response)
        return parsed_ping_dict

    def parse_ping_summary_and_update_parsed_ping_dict(
            self: Ping, parsed_ping_dict: dict, ping_summary: str) -> None:
        '''
        Parses the given ping summary and updates the parsed_ping_dict.

        Example ping summary:
        10 packets transmitted, 10 packets received, 0.0% packet loss
        '''

        split_ping_summary = ping_summary.split(',')

        # Get packets transmitted
        packets_transmitted_data = split_ping_summary[0]
        parsed_ping_dict[RESPONSE_KEY_NUM_PACKETS_SENT] = \
            int(packets_transmitted_data.split(' ')[0])

        # Get packet loss percentage
        packet_loss_data = split_ping_summary[2]
        parsed_ping_dict[RESPONSE_KEY_PACKET_LOSS_PERCENT] = \
            float(packet_loss_data.split('%')[0])

    def parse_ping_timing_and_update_parsed_ping_dict(
            self: Ping, parsed_ping_dict: dict, ping_timing: str) -> None:
        '''
        Parses the given ping timing and updates the parsed_ping_dict.

        Example ping timing:
        round-trip min/avg/max/stddev = 3.084/8.829/11.708/2.290 ms
        '''

        split_ping_timing = ping_timing.split('=')
        split_ping_timing = split_ping_timing[1].split('/')

        # Get average timing
        parsed_ping_dict[RESPONSE_KEY_AVERAGE_ROUND_TRIP_TIME] = \
            float(split_ping_timing[1])

        # Get max timing
        parsed_ping_dict[RESPONSE_KEY_MAX_ROUND_TRIP_TIME] = \
            float(split_ping_timing[2])

    def determine_if_able_to_resolve_host(
            self: Ping,
            url: str,
            split_ping_response: str) -> bool:
        '''
        Determines if ping was able to resolve host.
        Successful pings have a multiline response while unsuccessful pings
        are a single line.
        '''
        if len(split_ping_response) == 1:
            return False
        return True

    def check_route_to_local_router_and_update_parsed_ping_dict(
            self: Ping,
            split_ping_response: str,
            parsed_ping_dict: dict) -> bool:
        '''
        If not able to connect to local router, the ping fails and exits with
        a message that contains the following in the string:
        returned non-zero exit status
        '''
        if LOCAL_ROUTER_ERROR_MESSAGE in split_ping_response[0]:
            return False
        return True
