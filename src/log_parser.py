from __future__ import annotations
import os
from typing import IO

from src.constants import (
    LOCAL_ROUTER_ERROR,
    LOGGER_STARTING_LOG,
    LOGGER_STATUS_CHECK_RUNNING_MESSAGE,
    MODEM_ERROR,
    PACKET_LOSS_ERROR,
    PARSER_PACKET_LOSS,
    PARSER_ROUND_TRIP_TIME,
    PARSER_MODEM_DOWN,
    PARSER_ROUTER_DOWN,
    ROUND_TRIP_TIME_ERROR
)


class LogParser:

    def run_parser(self: LogParser) -> None:
        log_file_path = self.get_log_file_path()
        log_file_string = self.get_log_file_string(log_file_path)
        internet_status_summary = self.parse_log(log_file_string)
        return internet_status_summary

    def get_log_file_path(self: LogParser) -> IO:
        log_file_path = '~/internet_status/internet_status.log'
        log_file_path = os.path.expanduser(log_file_path)
        return log_file_path

    def get_log_file_string(self: LogParser, log_file_path: str) -> str:
        try:
            log_file_string = open(log_file_path, 'r')
            return log_file_string
        except Exception as e:
            print('Unable to open log file: ' + str(e))

    def parse_log(self: LogParser, log_file_string: str) -> dict:
        internet_status_summary = {}

        log_message_error_to_summary_key_map = {
            PACKET_LOSS_ERROR: PARSER_PACKET_LOSS,
            ROUND_TRIP_TIME_ERROR: PARSER_ROUND_TRIP_TIME,
            MODEM_ERROR: PARSER_MODEM_DOWN,
            LOCAL_ROUTER_ERROR: PARSER_ROUTER_DOWN
        }

        for line in log_file_string.splitlines():
            # Check if empty line or starting log message
            if not line or \
                    LOGGER_STARTING_LOG in line or \
                    LOGGER_STATUS_CHECK_RUNNING_MESSAGE in line:
                continue

            # Get date and check date entry in internet_status_summary
            split_message = line.split('-')
            log_date_time = split_message[0]
            log_date = log_date_time.split('@')[0]
            if log_date not in internet_status_summary:
                internet_status_summary[log_date] = {
                    PARSER_PACKET_LOSS: 0,
                    PARSER_ROUND_TRIP_TIME: 0,
                    PARSER_MODEM_DOWN: 0,
                    PARSER_ROUTER_DOWN: 0
                }

            # Get log data
            log_message = split_message[1]
            for error, internet_status_summary_key in \
                    log_message_error_to_summary_key_map.items():
                if error in log_message:
                    internet_status_summary[
                        log_date][internet_status_summary_key] += 1
                    continue

        return internet_status_summary


if __name__ == '__main__':
    log_parser = LogParser()
    log_parser.run_parser()
