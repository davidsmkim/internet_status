
from __future__ import annotations
from mock import patch
import unittest

from src.constants import (
    LOCAL_ROUTER_ERROR,
    RESOLVE_HOST_ERROR,
    PACKET_LOSS_ERROR
)
from src.ping import Ping
from tests.fake_test_data.ping_test_data import (
    GOOGLE_HOST,
    LOCAL_ROUTER_HOST,
    LOCAL_ROUTER_ISSUE_RESPONSE,
    SUCCESSFUL_RESPONSE,
    PACKET_LOSS_RESPONSE,
    RECEIVED_ERRORS_RESPONSE,
    UNABLE_TO_RESOLVE_HOST_RESPONSE
)


class PingTest(unittest.TestCase):
    def setUp(self: PingTest) -> None:
        self.ping = Ping()

    def tearDown(self: PingTest) -> None:
        pass

    @patch('src.logger.Logger.log_verbose')
    @patch('src.ping.Ping.ping_host')
    def test_parse_ping_response_success(
            self: PingTest,
            mock_ping_host: patch,
            mock_logger: patch) -> None:
        mock_ping_host.return_value = SUCCESSFUL_RESPONSE

        parsed_ping_dict = \
            self.ping.ping_host_and_return_parsed_response(GOOGLE_HOST)
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

    @patch('src.logger.Logger.log_verbose')
    @patch('src.ping.Ping.ping_host')
    def test_parse_ping_response_with_packet_loss(
            self: PingTest,
            mock_ping_host: patch,
            mock_logger: patch) -> None:
        mock_ping_host.return_value = PACKET_LOSS_RESPONSE

        parsed_ping_dict = \
            self.ping.ping_host_and_return_parsed_response(GOOGLE_HOST)
        expected_parsed_ping_dict = {
            'host': 'www.google.com',
            'num_packets_sent': 8,
            'packet_loss_percent': 87.5,
            'max_round_trip_time': 38.466,
            'average_round_trip_time': 38.466,
            'able_to_resolve_host': True,
            'error': PACKET_LOSS_ERROR
        }
        self.assertEqual(parsed_ping_dict, expected_parsed_ping_dict)

    @patch('src.logger.Logger.log_verbose')
    @patch('src.ping.Ping.ping_host')
    def test_parse_ping_response_unable_to_resolve_host(
            self: PingTest,
            mock_ping_host: patch,
            mock_logger: patch) -> None:
        mock_ping_host.return_value = UNABLE_TO_RESOLVE_HOST_RESPONSE

        parsed_ping_dict = self.ping.ping_host_and_return_parsed_response(
            GOOGLE_HOST)
        expected_parsed_ping_dict = {
            'host': 'www.google.com',
            'able_to_resolve_host': False,
            'error': RESOLVE_HOST_ERROR
        }
        self.assertEqual(parsed_ping_dict, expected_parsed_ping_dict)

    @patch('src.logger.Logger.log_verbose')
    @patch('src.ping.Ping.ping_host')
    def test_parse_ping_response_with_local_router_error(
            self: PingTest,
            mock_ping_host: patch,
            mock_logger: patch) -> None:
        mock_ping_host.return_value = LOCAL_ROUTER_ISSUE_RESPONSE

        parsed_ping_dict = self.ping.ping_host_and_return_parsed_response(
                LOCAL_ROUTER_HOST)
        expected_parsed_ping_dict = {
            'host': '192.168.86.1',
            'able_to_resolve_host': False,
            'error': LOCAL_ROUTER_ERROR
        }
        self.assertEqual(parsed_ping_dict, expected_parsed_ping_dict)

    @patch('src.logger.Logger.log_verbose')
    @patch('src.ping.Ping.ping_host')
    def test_parse_ping_response_with_received_errors(
            self: PingTest,
            mock_ping_host: patch,
            mock_logger: patch) -> None:
        mock_ping_host.return_value = RECEIVED_ERRORS_RESPONSE

        parsed_ping_dict = self.ping.ping_host_and_return_parsed_response(
                GOOGLE_HOST)
        expected_parsed_ping_dict = {
            'host': 'www.google.com',
            'num_packets_sent': 50,
            'packet_loss_percent': 40.0,
            'max_round_trip_time': 25.651,
            'average_round_trip_time': 15.753,
            'able_to_resolve_host': True,
            'error': PACKET_LOSS_ERROR
        }
        self.assertEqual(parsed_ping_dict, expected_parsed_ping_dict)


if __name__ == '__main__':
    unittest.main()
