from __future__ import annotations
import os

from src.internet_status_util import get_datetime


class Logger:

    def __init__(self: Logger) -> None:
        self.file_name = '~/internet_status/internet_status_log.txt'
        self.file_name = os.path.expanduser(self.file_name)
        os.makedirs(os.path.dirname(self.file_name), exist_ok=True)
        current_time = get_datetime()
        self.write_to_file('Starting Log at: ' + current_time)

    def log(self: Logger, time_stamp: str, error_message: str) -> None:
        write_content = time_stamp + ' - ' + error_message
        self.write_to_file(write_content)

    def write_to_file(self: Logger, write_content: str) -> None:
        with open(self.file_name, 'a') as write_file:
            write_file.write(write_content)
            write_file.write('\n')


logger = Logger()
