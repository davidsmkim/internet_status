from __future__ import annotations

from constants import (
    APPLE_HOSTNAME,
    COM_SUFFIX,
    GOOGLE_HOSTNAME,
    LOCAL_ROUTER
)
from internet_status_util import create_url
from ping import Ping


class InternetStatus():

    def run_internet_status_check(self: InternetStatus) -> None:
        ping = Ping()

        router_response = ping.ping_host(LOCAL_ROUTER, 1)
        print(router_response)

        google_url = create_url(GOOGLE_HOSTNAME, COM_SUFFIX)
        google_response = ping.ping_host(google_url, 1)
        print(google_response)

        apple_url = create_url(APPLE_HOSTNAME, COM_SUFFIX)
        apple_response = ping.ping_host(apple_url, 1)
        print(apple_response)


if __name__ == "__main__":
    internet_status = InternetStatus()
    internet_status.run_internet_status_check()
