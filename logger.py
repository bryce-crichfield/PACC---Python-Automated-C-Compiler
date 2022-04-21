from dataclasses import dataclass
import math
import os
from typing import Callable

@dataclass
class LoggerSettings:
    verbosity_level: int

LoggerSettingsGlobal = LoggerSettings(0)

VerbosityLow = 0
VerbosityMid = 1
VerbosityHigh = 2

_Loggable = Callable[[None], str]

def Msg(str):
    return Logged(lambda logger : str)

class Logged:
    def __init__(self, loggable):
        self.loggable = loggable

    def apply(self, logger) -> str:
        return self.loggable(logger)

    def _prepended_decoration(self, decoration):
        def decorated(logger):
            return f"{decoration}{self.loggable(logger)}\033[0m"
        return lambda logger : decorated(logger)

    def purple(self):
        return Logged(self._prepended_decoration('\033[95m'))

    def blue(self):
        return Logged(self._prepended_decoration('\033[94m'))

    def cyan(self):
        return Logged(self._prepended_decoration('\033[96m'))

    def green(self):
        return Logged(self._prepended_decoration('\033[92m'))

    def orange(self):
        return Logged(self._prepended_decoration('\033[93m'))

    def red(self):
        return Logged(self._prepended_decoration('\033[91m'))

    def bold(self):
        return Logged(self._prepended_decoration('\033[1m'))
    
    def underline(self):
        return Logged(self._prepended_decoration('\033[4m'))

    def _verbosity(self, level):
        def verbosed(logger):
            if logger.verbosity_level >= level:
                return f"{self.loggable(logger)}\033[0m"
            else:
                return "\033[0m"
        return lambda logger : verbosed(logger)

    def verbose(self):
        return Logged(self._verbosity(VerbosityHigh))

    def semiverbose(self):
        return Logged(self._verbosity(VerbosityMid))

    def nonverbose(self):
        return Logged(self._verbosity(VerbosityLow))

    def padded(self, size):
        normal = math.floor(size) * 10
        return Logged(lambda logger : self.loggable(logger).center(normal, " "))

    def centered(self, seperator=" "):
        term_size = os.get_terminal_size().columns
        return Logged(lambda logger : self.loggable(logger).center(term_size, seperator))

class Logger:
    def __init__(self, verbosity_level):
        self.verbosity_level = verbosity_level
    
    def log(self, *logs: Logged):
        for log in logs:
            out = log.apply(self)
            if out != "":
                print(out, end="")




