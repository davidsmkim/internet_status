from __future__ import annotations
import os

from src.internet_status_util import get_datetime


class Logger:

    def __init__(self: Logger) -> None:
        self.log_file = '~/internet_status/internet_status.log'
        self.log_file = os.path.expanduser(self.log_file)
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        current_time = get_datetime()
        self.write_to_file(self.log_file, 'Starting Log at: ' + current_time)

        self.verbose_log_file = '~/internet_status/internet_status_verbose.log'
        self.verbose_log_file = os.path.expanduser(self.verbose_log_file)
        os.makedirs(os.path.dirname(self.verbose_log_file), exist_ok=True)
        self.write_to_file(
            self.verbose_log_file,
            'Starting Log at: ' + current_time)

    def log(self: Logger, time_stamp: str, error_message: str) -> None:
        write_content = time_stamp + ' - ' + str(error_message)
        self.write_to_file(self.log_file, write_content)

    def log_verbose(self: Logger, write_content: str) -> None:
        time_stamp = get_datetime()
        write_content = time_stamp + ' - ' + str(write_content)
        self.write_to_file(self.verbose_log_file, write_content)

    def write_to_file(
            self: Logger,
            file_name: str,
            write_content: str) -> None:
        with open(file_name, 'a') as write_file:
            write_file.write(write_content)
            write_file.write('\n')


logger = Logger()
