from __future__ import annotations
import subprocess

from constants import (
    PING_COMMAND,
    PING_COUNT_OPTION,
)


class Ping:

    def ping_host(self: Ping,
                  url: str) -> str:
        """
        Pings a given host and returns response.  Each ping is done
        individually in order to allow for more up to date data.
        """

        for _ in range(num_pings):
            try:
                response = subprocess.check_output(
                    [PING_COMMAND, PING_COUNT_OPTION, str(num_pings), url],
                    stderr=subprocess.STDOUT,
                    universal_newlines=True
                )
            except subprocess.CalledProcessError as error:
                response = error
        return response

    def ping_host_and_return_status(self: Ping,
                                    url: str,
                                    num_pings: int) -> bool:
        for _ in range(num_pings):
            response = self.ping_host(url)
            response = parse_response(response)
        return True
