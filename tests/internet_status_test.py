
from __future__ import annotations
import unittest
from mock import patch

from src.internet_status import InternetStatus
from src.logger import Logger
from tests.fake_test_data.internet_status_test_data import (
    APPLE_DESTINATION_HOST_UNREACHABLE_RESPONSE,
    APPLE_PACKET_LOSS_RESPONSE,
    APPLE_ROUND_TRIP_TIME_ERROR_RESPONSE,
    APPLE_SUCCESSFUL_RESPONSE,
    APPLE_UNABLE_TO_RESOLVE_HOST_RESPONSE,
    GOOGLE_DESTINATION_HOST_UNREACHABLE_RESPONSE,
    GOOGLE_PACKET_LOSS_RESPONSE,
    GOOGLE_ROUND_TRIP_TIME_ERROR_RESPONSE,
    GOOGLE_SUCCESSFUL_RESPONSE,
    GOOGLE_UNABLE_TO_RESOLVE_HOST_RESPONSE,
    LOCAL_ROUTER_PACKET_LOSS_RESPONSE,
    LOCAL_ROUTER_ROUND_TRIP_TIME_ERROR_RESPONSE,
    LOCAL_ROUTER_SUCCESSFUL_RESPONSE,
    LOCAL_ROUTER_ISSUE_RESPONSE
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
            mock_response: dict,
            mock_logger: Logger) -> None:
        mock_response.side_effect = [
            LOCAL_ROUTER_SUCCESSFUL_RESPONSE,
            GOOGLE_SUCCESSFUL_RESPONSE
        ]
        self.assertEqual(mock_logger.call_count, 0)

    @patch('src.ping.Ping.ping_host')
    def test_run_ping_tests_with_success_in_second_host(
            self: InternetStatusTest,
            mock_response: dict) -> None:
        mock_response.side_effect = [
            GOOGLE_PACKET_LOSS_RESPONSE,
            APPLE_SUCCESSFUL_RESPONSE
        ]
        pass

    @patch('src.ping.Ping.ping_host')
    def test_run_ping_tests_with_local_router_error(
            self: InternetStatusTest,
            mock_response: dict) -> None:
        mock_response.side_effect = [
            GOOGLE_UNABLE_TO_RESOLVE_HOST_RESPONSE,
            APPLE_UNABLE_TO_RESOLVE_HOST_RESPONSE,
            LOCAL_ROUTER_ISSUE_RESPONSE
        ]
        pass

    @patch('src.ping.Ping.ping_host')
    def test_run_ping_tests_with_resolve_host_error(
            self: InternetStatusTest,
            mock_response: dict) -> None:
        mock_response.side_effect = [
            GOOGLE_UNABLE_TO_RESOLVE_HOST_RESPONSE,
            APPLE_UNABLE_TO_RESOLVE_HOST_RESPONSE,
            LOCAL_ROUTER_SUCCESSFUL_RESPONSE
        ]
        pass

    @patch('src.ping.Ping.ping_host')
    def test_run_ping_tests_with_packet_loss_error(
            self: InternetStatusTest,
            mock_response: dict) -> None:
        mock_response.side_effect = [
            GOOGLE_PACKET_LOSS_RESPONSE,
            APPLE_PACKET_LOSS_RESPONSE,
            LOCAL_ROUTER_SUCCESSFUL_RESPONSE
        ]
        pass

    @patch('src.ping.Ping.ping_host')
    def test_run_ping_tests_with_round_trip_time_error(
            self: InternetStatusTest,
            mock_response: dict) -> None:
        mock_response.side_effect = [
            GOOGLE_ROUND_TRIP_TIME_ERROR_RESPONSE,
            APPLE_ROUND_TRIP_TIME_ERROR_RESPONSE,
            LOCAL_ROUTER_SUCCESSFUL_RESPONSE
        ]
        pass

    @patch('src.ping.Ping.ping_host')
    def test_run_ping_tests_with_multiple_error_types(
            self: InternetStatusTest,
            mock_response: dict) -> None:

        # Check first host is most severe
        mock_response.side_effect = [
            GOOGLE_UNABLE_TO_RESOLVE_HOST_RESPONSE,
            APPLE_ROUND_TRIP_TIME_ERROR_RESPONSE,
            LOCAL_ROUTER_SUCCESSFUL_RESPONSE
        ]

        # Check second host is most severe
        mock_response.side_effect = [
            GOOGLE_UNABLE_TO_RESOLVE_HOST_RESPONSE,
            APPLE_ROUND_TRIP_TIME_ERROR_RESPONSE,
            LOCAL_ROUTER_SUCCESSFUL_RESPONSE
        ]

        # Check local router is most severe
        mock_response.side_effect = [
            GOOGLE_UNABLE_TO_RESOLVE_HOST_RESPONSE,
            APPLE_ROUND_TRIP_TIME_ERROR_RESPONSE,
            LOCAL_ROUTER_SUCCESSFUL_RESPONSE
        ]
        pass

    def test_check_if_ping_was_successful_with_success(
            self: InternetStatusTest) -> None:
        pass

    def test_check_if_ping_was_successful_with_unable_to_resolve_host_error(
            self: InternetStatusTest) -> None:
        pass

    def test_check_if_ping_was_successful_with_packet_loss_error(
            self: InternetStatusTest) -> None:
        pass

    def test_check_if_ping_was_successful_with_round_trip_time_error(
            self: InternetStatusTest) -> None:
        pass

    def test_get_most_severe_error_with_local_router_error(
            self: InternetStatusTest) -> None:
        pass

    def test_get_most_severe_error_with_resolve_host_error(
            self: InternetStatusTest) -> None:
        pass

    def test_get_most_severe_error_with_packet_loss_error(
            self: InternetStatusTest) -> None:
        pass

    def test_get_most_severe_error_with_round_trip_time_error(
            self: InternetStatusTest) -> None:
        pass

    def test_get_most_severe_error_with_multiple_error_types(
            self: InternetStatusTest) -> None:
        pass

    def test_check_if_ping_was_successful_with_success(
            self: InternetStatusTest) -> None:
        pass

    def test_check_if_ping_was_successful_with_unable_to_resolve_host_error(
            self: InternetStatusTest) -> None:
        pass

    def test_check_if_ping_was_successful_with_packet_loss_error(
            self: InternetStatusTest) -> None:
        pass

    def test_check_if_ping_was_successful_with_round_trip_time_error(
            self: InternetStatusTest) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
