# Logger.py

import os

LOGFILE = "{}/suspicious_domains.log".format(os.path.dirname(os.path.abspath(__file__)))


class Logger(object):
    def __init__(self, print_logs: bool = False):
        self._print_logs = print_logs

    def alert(self, message: str):
        with open(LOGFILE, "a") as the_file:
            the_file.write(f"{message}")
            if self._print_logs:
                print(f"{message}")
