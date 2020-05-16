from __future__ import annotations

from src.constants import (
    APPLE_HOSTNAME,
    COM_SUFFIX,
    GOOGLE_HOSTNAME,
    LOCAL_ROUTER,
    LOCAL_ROUTER_ERROR,
    MAX_ACCEPTABLE_PACKET_LOSS,
    MAX_ACCEPTABLE_AVERAGE_ROUND_TRIP_TIME,
    PACKET_LOSS,
    PACKET_LOSS_ERROR,
    RESOLVE_HOST_ERROR,
    RESPONSE_KEY_PACKET_LOSS_PERCENT,
    RESPONSE_KEY_AVERAGE_ROUND_TRIP_TIME,
    RESPONSE_KEY_ABLE_TO_RESOLVE_HOST,
    RESPONSE_KEY_ERROR,
    ROUND_TRIP_TIME_ERROR,
    UNABLE_TO_RESOLVE_HOST,
    UNACCEPTABLE_ROUND_TRIP_TIME
)
from src.internet_status_util import create_url
from src.ping import Ping


class InternetStatus():

    def run_internet_status_check(self: InternetStatus) -> None:
        self.run_ping_tests()

    def run_ping_tests(self: InternetStatus) -> None:
        '''
        Runs a ping test against www.google.com, www.apple.com, and local
        router.  The ping test starts with www.google.com and only continues to
        the next host if there is an issue with pinging the current host.

        If there any issues (unable to resolve host, packet loss, high latency)
        are present, the issue is logged and timestamped.  If multiple errors
        are present, the errors will be logged in the following precedence
        order:
        Cannot connect to local router: Unable to resolve host
        Cannot connect to internet: Unable to resolve host
        30% packet loss
        50 ms average round trip time

        Example log entries:
        5/15/20@9:20pm - Cannot connect to local router: Unable to resolve host
        5/15/20@9:20pm - Cannot connect to internet: Unable to resolve host
        5/15/20@9:20pm - 30% packet loss
        5/15/20@9:20pm - 50 ms average round trip time
        '''
        ping_test_results = {}
        ping = Ping()

        google_url = create_url(GOOGLE_HOSTNAME, COM_SUFFIX)
        apple_url = create_url(APPLE_HOSTNAME, COM_SUFFIX)
        external_host_list = [google_url, apple_url]

        # Check if able to successfully ping external hosts
        for host in external_host_list:
            parsed_host_response = \
                ping.ping_host_and_return_parsed_response(host, 100)
            ping_test_results[host] = parsed_host_response
            ping_to_external_host_was_successful = \
                self.check_if_ping_was_successful(parsed_host_response)
            if ping_to_external_host_was_successful:
                break

        # Unable to successfully ping external hosts.  Check if local router
        # can be successfully pinged
        if not ping_to_external_host_was_successful:
            parsed_router_response = \
                ping.ping_host_and_return_parsed_response(LOCAL_ROUTER, 100)
            ping_test_results[LOCAL_ROUTER] = parsed_router_response
            ping_to_local_router_was_successful = \
                self.check_if_ping_was_successful(parsed_router_response)

        # Check final ping statuses
        error = None
        if not ping_to_external_host_was_successful:
            if not ping_to_local_router_was_successful:
                error = LOCAL_ROUTER_ERROR
            else:
                error_message = self.get_most_severe_error_and_compile_message(
                    ping_test_results)
        if error:
            logger.log(start_time, error_message)

    def get_most_severe_error_and_compile_message(
            self: InternetStatus,
            ping_test_results: dict) -> str:

        # Determine most severe error
        error_precedence = [
            LOCAL_ROUTER_ERROR,
            RESOLVE_HOST_ERROR,
            PACKET_LOSS_ERROR,
            ROUND_TRIP_TIME_ERROR
        ]

        most_severe_error = None
        additional_error_data = None
        for parsed_host_response in ping_test_results.values():
            current_error = parsed_host_response[RESPONSE_KEY_ERROR]
            if current_error in error_precedence and \
                (most_severe_error is None or
                    error_precedence.index(most_severe_error) >
                    error_precedence.index(current_error)):
                most_severe_error = current_error

                if most_severe_error == PACKET_LOSS_ERROR:
                    additional_error_data = parsed_host_response[
                            RESPONSE_KEY_PACKET_LOSS_PERCENT]
                elif most_severe_error == ROUND_TRIP_TIME_ERROR:
                    additional_error_data = parsed_host_response[
                            RESPONSE_KEY_AVERAGE_ROUND_TRIP_TIME]

        # Add numeric data for packet loss and round trip time errors
        if most_severe_error == PACKET_LOSS_ERROR or \
                most_severe_error == ROUND_TRIP_TIME_ERROR:
            most_severe_error = str(additional_error_data) + most_severe_error

        return most_severe_error

    def check_if_ping_was_successful(
            self: InternetStatus,
            parsed_host_response: dict) -> bool:

        if not self.check_if_ping_resolve_host(parsed_host_response):
            parsed_host_response[RESPONSE_KEY_ERROR] = UNABLE_TO_RESOLVE_HOST
            return False

        elif not self.check_if_ping_packet_loss_acceptable(
                parsed_host_response):
            parsed_host_response[RESPONSE_KEY_ERROR] = PACKET_LOSS
            return False

        elif not self.check_if_ping_round_trip_time_acceptable(
                parsed_host_response):
            parsed_host_response[RESPONSE_KEY_ERROR] = \
                UNACCEPTABLE_ROUND_TRIP_TIME
            return False

        parsed_host_response[RESPONSE_KEY_ERROR] = ''
        return True

    def check_if_ping_resolve_host(
            self: InternetStatus,
            parsed_host_response: dict) -> bool:
        return parsed_host_response[RESPONSE_KEY_ABLE_TO_RESOLVE_HOST]

    def check_if_ping_packet_loss_acceptable(
            self: InternetStatus,
            parsed_host_response: dict) -> bool:
        if (parsed_host_response[RESPONSE_KEY_PACKET_LOSS_PERCENT] >
                MAX_ACCEPTABLE_PACKET_LOSS):
            return False
        return True

    def check_if_ping_round_trip_time_acceptable(
            self: InternetStatus,
            parsed_host_response: dict) -> bool:
        if (parsed_host_response[RESPONSE_KEY_AVERAGE_ROUND_TRIP_TIME] >
                MAX_ACCEPTABLE_AVERAGE_ROUND_TRIP_TIME):
            return False
        return True


if __name__ == "__main__":
    internet_status = InternetStatus()
    internet_status.run_internet_status_check()
