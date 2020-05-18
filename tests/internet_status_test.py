
from __future__ import annotations
from mock import patch
import unittest

from src.constants import (
    LOCAL_ROUTER_ERROR,
    PACKET_LOSS_ERROR,
    RESOLVE_HOST_ERROR,
    ROUND_TRIP_TIME_ERROR
)
from src.internet_status import InternetStatus
from src.logger import Logger
from tests.fake_test_data.internet_status_test_data import (
    APPLE_DESTINATION_HOST_UNREACHABLE_RESPONSE,
    APPLE_PACKET_LOSS_RESPONSE,
    APPLE_ROUND_TRIP_TIME_ERROR_RESPONSE,
    APPLE_SUCCESSFUL_RESPONSE,
    APPLE_UNABLE_TO_RESOLVE_HOST_RESPONSE,
    COMMAND_EXIT_ISSUE_RESPONSE,
    GOOGLE_DESTINATION_HOST_UNREACHABLE_RESPONSE,
    GOOGLE_PACKET_LOSS_RESPONSE,
    GOOGLE_ROUND_TRIP_TIME_ERROR_RESPONSE,
    GOOGLE_SUCCESSFUL_RESPONSE,
    GOOGLE_UNABLE_TO_RESOLVE_HOST_RESPONSE,
    LOCAL_ROUTER_PACKET_LOSS_RESPONSE,
    LOCAL_ROUTER_ROUND_TRIP_TIME_ERROR_RESPONSE,
    LOCAL_ROUTER_SUCCESSFUL_RESPONSE,
)


class InternetStatusTest(unittest.TestCase):
    def setUp(self: InternetStatusTest) -> None:
        self.internet_status = InternetStatus()

    def tearDown(self: InternetStatusTest) -> None:
        pass

    @patch('src.logger.Logger.log')
    @patch('src.ping.Ping.ping_host')
    def test_run_ping_tests_with_success(
            self: InternetStatusTest,
            mock_response: patch,
            mock_logger: Logger) -> None:
        mock_response.side_effect = [
            GOOGLE_SUCCESSFUL_RESPONSE
        ]

        self.internet_status.run_ping_tests()
        self.assertEqual(mock_logger.call_count, 0)

    @patch('src.logger.Logger.log')
    @patch('src.ping.Ping.ping_host')
    def test_run_ping_tests_with_success_in_second_host(
            self: InternetStatusTest,
            mock_response: patch,
            mock_logger: Logger) -> None:
        mock_response.side_effect = [
            GOOGLE_PACKET_LOSS_RESPONSE,
            APPLE_SUCCESSFUL_RESPONSE
        ]

        self.internet_status.run_ping_tests()
        self.assertEqual(mock_logger.call_count, 0)

    @patch('src.logger.Logger.log')
    @patch('src.ping.Ping.ping_host')
    def test_run_ping_tests_with_local_router_error(
            self: InternetStatusTest,
            mock_response: patch,
            mock_logger: Logger) -> None:
        mock_response.side_effect = [
            COMMAND_EXIT_ISSUE_RESPONSE,
            COMMAND_EXIT_ISSUE_RESPONSE,
            COMMAND_EXIT_ISSUE_RESPONSE,
        ]

        self.internet_status.run_ping_tests()
        self.assertEqual(mock_logger.call_count, 1)
        args, _ = mock_logger.call_args_list[0]
        self.assertIn(LOCAL_ROUTER_ERROR, args)

    @patch('src.logger.Logger.log')
    @patch('src.ping.Ping.ping_host')
    def test_run_ping_tests_with_resolve_host_error(
            self: InternetStatusTest,
            mock_response: patch,
            mock_logger: Logger) -> None:
        mock_response.side_effect = [
            GOOGLE_UNABLE_TO_RESOLVE_HOST_RESPONSE,
            APPLE_UNABLE_TO_RESOLVE_HOST_RESPONSE,
            LOCAL_ROUTER_SUCCESSFUL_RESPONSE
        ]

        self.internet_status.run_ping_tests()
        self.assertEqual(mock_logger.call_count, 1)
        args, _ = mock_logger.call_args_list[0]
        self.assertIn(RESOLVE_HOST_ERROR, args)

    @patch('src.logger.Logger.log')
    @patch('src.ping.Ping.ping_host')
    def test_run_ping_tests_with_packet_loss_error(
            self: InternetStatusTest,
            mock_response: patch,
            mock_logger: Logger) -> None:
        mock_response.side_effect = [
            GOOGLE_PACKET_LOSS_RESPONSE,
            APPLE_PACKET_LOSS_RESPONSE,
            LOCAL_ROUTER_SUCCESSFUL_RESPONSE
        ]

        self.internet_status.run_ping_tests()
        self.assertEqual(mock_logger.call_count, 1)
        args, _ = mock_logger.call_args_list[0]
        args = args[1]
        self.assertIn(PACKET_LOSS_ERROR, args)

    @patch('src.logger.Logger.log')
    @patch('src.ping.Ping.ping_host')
    def test_run_ping_tests_with_round_trip_time_error(
            self: InternetStatusTest,
            mock_response: patch,
            mock_logger: Logger) -> None:
        mock_response.side_effect = [
            GOOGLE_ROUND_TRIP_TIME_ERROR_RESPONSE,
            APPLE_ROUND_TRIP_TIME_ERROR_RESPONSE,
            LOCAL_ROUTER_SUCCESSFUL_RESPONSE
        ]

        self.internet_status.run_ping_tests()
        self.assertEqual(mock_logger.call_count, 1)
        args, _ = mock_logger.call_args_list[0]
        args = args[1]
        self.assertIn(ROUND_TRIP_TIME_ERROR, args)

    @patch('src.logger.Logger.log')
    @patch('src.ping.Ping.ping_host')
    def test_run_ping_tests_with_multiple_error_types(
            self: InternetStatusTest,
            mock_response: patch,
            mock_logger: Logger) -> None:

        # Check first host is most severe
        mock_response.side_effect = [
            GOOGLE_UNABLE_TO_RESOLVE_HOST_RESPONSE,
            APPLE_ROUND_TRIP_TIME_ERROR_RESPONSE,
            LOCAL_ROUTER_SUCCESSFUL_RESPONSE
        ]

        self.internet_status.run_ping_tests()
        self.assertEqual(mock_logger.call_count, 1)
        args, _ = mock_logger.call_args_list[0]
        args = args[1]
        self.assertIn(RESOLVE_HOST_ERROR, args)

        # Check second host is most severe
        mock_response.side_effect = [
            GOOGLE_ROUND_TRIP_TIME_ERROR_RESPONSE,
            APPLE_PACKET_LOSS_RESPONSE,
            LOCAL_ROUTER_SUCCESSFUL_RESPONSE
        ]

        self.internet_status.run_ping_tests()
        self.assertEqual(mock_logger.call_count, 2)
        args, _ = mock_logger.call_args_list[1]
        args = args[1]
        self.assertIn(PACKET_LOSS_ERROR, args)

        # Check local router is most severe
        mock_response.side_effect = [
            GOOGLE_UNABLE_TO_RESOLVE_HOST_RESPONSE,
            APPLE_ROUND_TRIP_TIME_ERROR_RESPONSE,
            COMMAND_EXIT_ISSUE_RESPONSE
        ]

        self.internet_status.run_ping_tests()
        self.assertEqual(mock_logger.call_count, 3)
        args, _ = mock_logger.call_args_list[2]
        args = args[1]
        self.assertIn(LOCAL_ROUTER_ERROR, args)


if __name__ == '__main__':
    unittest.main()
