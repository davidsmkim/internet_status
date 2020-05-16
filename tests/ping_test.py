
from __future__ import annotations
import unittest

from src.ping import Ping
from src.constants import (
    DESTINATION_HOST_UNREACHABLE,
    PACKET_LOSS,
    UNABLE_TO_RESOLVE_HOST
)
from tests.fake_test_data.ping_test_data import (
    DESTINATION_HOST_UNREACHABLE_RESPONSE,
    GOOGLE_HOST,
    SUCCESSFUL_RESPONSE,
    PACKET_LOSS_RESPONSE,
    UNABLE_TO_RESOLVE_HOST_RESPONSE
)


class PingTest(unittest.TestCase):
    def setUp(self: PingTest) -> None:
        self.ping = Ping()

    def tearDown(self: PingTest) -> None:
        pass

    def test_parse_ping_response_success(self: PingTest) -> None:
        parsed_ping_dict = \
            self.ping.parse_ping_response(GOOGLE_HOST, SUCCESSFUL_RESPONSE)
        expected_parsed_ping_dict = {
            'host': 'www.google.com',
            'num_packets_sent': 10,
            'packet_loss_percent': 0.0,
            'max_round_trip_time': 30.101,
            'average_round_trip_time': 21.855,
            'able_to_resolve_host': True,
            'error': ''
        }
        self.assertEqual(parsed_ping_dict, expected_parsed_ping_dict)

    def test_parse_ping_response_with_packet_loss(self: PingTest) -> None:
        parsed_ping_dict = \
            self.ping.parse_ping_response(GOOGLE_HOST, PACKET_LOSS_RESPONSE)
        expected_parsed_ping_dict = {
            'host': 'www.google.com',
            'num_packets_sent': 8,
            'packet_loss_percent': 87.5,
            'max_round_trip_time': 38.466,
            'average_round_trip_time': 38.466,
            'able_to_resolve_host': True,
            'error': PACKET_LOSS
        }
        self.assertEqual(parsed_ping_dict, expected_parsed_ping_dict)

    def test_parse_ping_response_unable_to_resolve_host(
            self: PingTest) -> None:
        parsed_ping_dict = self.ping.parse_ping_response(
            GOOGLE_HOST, UNABLE_TO_RESOLVE_HOST_RESPONSE)
        expected_parsed_ping_dict = {
            'host': 'www.google.com',
            'able_to_resolve_host': False,
            'error': UNABLE_TO_RESOLVE_HOST
        }
        self.assertEqual(parsed_ping_dict, expected_parsed_ping_dict)

    def test_parse_ping_response_with_destination_host_unreachable(
            self: PingTest) -> None:
        parsed_ping_dict = self.ping.parse_ping_response(
                GOOGLE_HOST,
                DESTINATION_HOST_UNREACHABLE_RESPONSE)
        expected_parsed_ping_dict = {
            'host': 'www.google.com',
            'num_packets_sent': 10,
            'packet_loss_percent': 10.0,
            'max_round_trip_time': 26.924,
            'average_round_trip_time': 19.868,
            'able_to_resolve_host': True,
            'error': DESTINATION_HOST_UNREACHABLE
        }
        self.assertEqual(parsed_ping_dict, expected_parsed_ping_dict)


if __name__ == '__main__':
    unittest.main()