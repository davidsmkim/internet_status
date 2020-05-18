from __future__ import annotations

from src.constants import (
    APPLE_HOSTNAME,
    COM_SUFFIX,
    COMMAND_EXIT_ERROR_MESSAGE,
    GOOGLE_HOSTNAME,
    LOCAL_ROUTER,
    LOCAL_ROUTER_ERROR,
    PACKET_LOSS_ERROR,
    RESOLVE_HOST_ERROR,
    RESPONSE_KEY_ERROR,
    RESPONSE_KEY_PACKET_LOSS_PERCENT,
    RESPONSE_KEY_AVERAGE_ROUND_TRIP_TIME,
    ROUND_TRIP_TIME_ERROR,
)
from src.internet_status_util import (
    create_url,
    get_datetime
)
from src.ping import Ping
from src.logger import logger


class InternetStatus():

    def __init__(self: InternetStatus) -> None:
        self.ping = Ping()

        google_url = create_url(GOOGLE_HOSTNAME, COM_SUFFIX)
        apple_url = create_url(APPLE_HOSTNAME, COM_SUFFIX)
        self.external_host_list = [google_url, apple_url]

    def run_internet_status_check(self: InternetStatus) -> None:
        while True:
            self.run_ping_tests()

    def run_ping_tests(self: InternetStatus) -> None:
        '''
        Runs a ping test against the provided external_host_list and local
        router.  The ping test starts with www.google.com and only continues to
        the next host if there is an issue with pinging the current host.

        If we are unable to successfully ping external hosts, we check the
        connection to the local router to see if an issue exists there.

        If there any issues (unable to resolve host, packet loss, high latency)
        are present, the issue is logged and timestamped.  If multiple errors
        are present, the errors will be logged in the following precedence
        order:
        Cannot connect to local router
        Cannot connect to internet: Unable to resolve host
        30% packet loss
        50 ms average round trip time

        Example log entries:
        12/31/18@17:41:00 - Cannot connect to local router
        12/31/18@17:41:00 - Cannot connect to internet: Unable to resolve host
        12/31/18@17:41:00 - 30% packet loss
        12/31/18@17:41:00 - 50 ms average round trip time
        '''

        ping_test_results = {}
        start_time = get_datetime()
        error = None

        # Check if able to successfully ping external hosts
        for host in self.external_host_list:
            parsed_host_response = \
                self.ping.ping_host_and_return_parsed_response(host, 10)
            ping_test_results[host] = parsed_host_response
            ping_to_external_host_was_successful = \
                self.check_if_ping_was_successful(
                    parsed_host_response)
            if ping_to_external_host_was_successful:
                break

        # Check local router
        if not ping_to_external_host_was_successful:
            parsed_router_response = \
                self.ping.ping_host_and_return_parsed_response(
                    LOCAL_ROUTER, 10)
            ping_test_results[LOCAL_ROUTER] = parsed_router_response
            ping_to_local_router_was_successful = \
                self.check_if_ping_was_successful(
                    parsed_router_response)

            if not ping_to_local_router_was_successful:
                error = LOCAL_ROUTER_ERROR
            else:
                # Check final ping statuses
                error = self.get_most_severe_error_and_compile_message(
                    ping_test_results)

            if error:
                logger.log(start_time, error)

    def get_most_severe_error_and_compile_message(
            self: InternetStatus,
            ping_test_results: dict) -> str:

        # Determine most severe error
        error_precedence = [
            COMMAND_EXIT_ERROR_MESSAGE,
            PACKET_LOSS_ERROR,
            RESOLVE_HOST_ERROR,
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
            ping_test_results: dict) -> bool:
        return not bool(ping_test_results[RESPONSE_KEY_ERROR])


if __name__ == "__main__":
    internet_status = InternetStatus()
    internet_status.run_internet_status_check()
