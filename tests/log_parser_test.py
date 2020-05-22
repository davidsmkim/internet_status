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

    @patch('src.log_parser.get_log_file_string')
    def test_parse_log(
            self: LogParserTest,
            mock_get_log_file_string: patch) -> None:
        mock_get_log_file_string.return_value = fake_internet_status_log

        self.log_parser.run_parser()
