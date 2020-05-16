from __future__ import annotations
import subprocess

from src.constants import (
    PING_COMMAND,
    PING_COUNT_OPTION,
    PING_QUIET_COMMAND
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
            packet_loss_percent: 5.0%,
            max_round_trip_time: 3.723,
            average_round_trip_time: 2.123
            able_to_resolve_host: True
        }
        If ping is unsuccessful and unable to resolve host, the returned
        dictionary has the same format but with only the 'host' and the
        'able_to_resolve_host' field, which is False.
        '''
        try:
            response = subprocess.check_output(
                [PING_COMMAND, PING_COUNT_OPTION, str(num_pings),
                 PING_QUIET_COMMAND, url],
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
        except subprocess.CalledProcessError as error:
            response = str(error)
        parsed_ping_dict = self.parse_ping_response(url, response)
        return parsed_ping_dict

    def parse_ping_response(self: Ping, url: str, response: str) -> dict:
        '''
        Parses an initial response into a dictionary with the parsed ping
        response.
        '''
        parsed_ping_dict = {
            'host': url,
            'able_to_resolve_host': False
        }
        split_ping_response = response.splitlines()

        ping_was_able_to_resolve_host = \
            self.determine_if_able_to_resolve_host(split_ping_response)
        if not ping_was_able_to_resolve_host:
            return parsed_ping_dict

        parsed_ping_dict['able_to_resolve_host'] = True
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
        parsed_ping_dict['num_packets_sent'] = \
            int(packets_transmitted_data.split(' ')[0])

        # Get packet loss percentage
        packet_loss_data = split_ping_summary[2]
        parsed_ping_dict['packet_loss_percent'] = \
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
        parsed_ping_dict['average_round_trip_time'] = \
            float(split_ping_timing[1])

        # Get max timing
        parsed_ping_dict['max_round_trip_time'] = \
            float(split_ping_timing[2])

    def determine_if_able_to_resolve_host(
            self: Ping,
            split_ping_response: str) -> bool:
        '''
        Determines if ping was able to resolve host.
        Successful pings have a multiline response while unsuccessful pings
        are a single line.
        '''
        if len(split_ping_response) == 1:
            return False
        else:
            return True
