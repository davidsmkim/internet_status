from __future__ import annotations


class Logger:

    def log(self: Logger, time_stamp: str, input: str) -> bool:
        pass

    def write_to_file(self: Logger, file_name: str, input: str) -> bool:
        pass


logger = Logger()
