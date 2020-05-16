
from __future__ import annotations
import unittest

from src.ping import Ping
from src.constants import (
)
from tests.fake_test_data.ping_test_data import (
)


class InternetStatusTest(unittest.TestCase):
    def setUp(self: InternetStatusTest) -> None:
        self.internet_status = InternetStatus()

    def tearDown(self: PingTest) -> None:
        pass

    def test_run_ping_tests_with_success(self: PingTest) -> None:
        pass

    def test_run_ping_tests_with_success_in_second_host(
            self: PingTest) -> None:
        pass

    def test_run_ping_tests_with_local_router_error(self: PingTest) -> None:
        pass

    def test_run_ping_tests_with_resolve_host_error(self: PingTest) -> None:
        pass

    def test_run_ping_tests_with_packet_loss_error(self: PingTest) -> None:
        pass

    def test_run_ping_tests_with_round_trip_time_error(self: PingTest) -> None:
        pass

    def test_run_ping_tests_with_multiple_error_types(self: PingTest) -> None:
        pass

    def test_check_if_ping_was_successful_with_success(self: PingTest) -> None:
        pass

    def test_check_if_ping_was_successful_with_unable_to_resolve_host_error(
            self: PingTest) -> None:
        pass

    def test_check_if_ping_was_successful_with_packet_loss_error(
            self: PingTest) -> None:
        pass

    def test_check_if_ping_was_successful_with_round_trip_time_error(
            self: PingTest) -> None:
        pass

    def test_get_most_severe_error_with_local_router_error(
            self: PingTest) -> None:
        pass

    def test_get_most_severe_error_with_resolve_host_error(
            self: PingTest) -> None:
        pass

    def test_get_most_severe_error_with_packet_loss_error(
            self: PingTest) -> None:
        pass

    def test_get_most_severe_error_with_round_trip_time_error(
            self: PingTest) -> None:
        pass

    def test_get_most_severe_error_with_multiple_error_types(
            self: PingTest) -> None:
        pass

    def test_check_if_ping_was_successful_with_success(
            self: PingTest) -> None:
        pass

    def test_check_if_ping_was_successful_with_unable_to_resolve_host_error(
            self: PingTest) -> None:
        pass

    def test_check_if_ping_was_successful_with_packet_loss_error(
            self: PingTest) -> None:
        pass

    def test_check_if_ping_was_successful_with_round_trip_time_error(
            self: PingTest) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
