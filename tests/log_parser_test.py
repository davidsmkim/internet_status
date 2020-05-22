from __future__ import annotations
from mock import patch
import unittest

from src.log_parser import LogParser
from tests.fake_test_data.log_parser_test_data import fake_internet_status_log


class LogParserTest(unittest.TestCase):
    def setUp(self: LogParserTest) -> None:
        self.log_parser = LogParser()

    def tearDown(self: LogParserTest) -> None:
        pass

    @patch('src.log_parser.LogParser.get_log_file_string')
    def test_parse_log(
            self: LogParserTest,
            mock_get_log_file_string: patch) -> None:
        mock_get_log_file_string.return_value = fake_internet_status_log

        internet_status_summary = self.log_parser.run_parser()
        expected_summary = {
            '05/21/20': {
                'packet_loss': 34,
                'round_trip_time': 1,
                'modem_down': 17,
                'router_down': 1
            },
            '05/22/20': {
                'packet_loss': 3,
                'round_trip_time': 4,
                'modem_down': 2,
                'router_down': 1
            }
        }
        self.assertEqual(expected_summary, internet_status_summary)
