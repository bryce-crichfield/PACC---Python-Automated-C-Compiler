from ast import Call
from ctypes import Union
from dataclasses import dataclass
from enum import Enum, auto
from functools import partial
import math
import os
from types import NoneType
from typing import Callable


_ENDC = '\033[0m'

@dataclass
class LoggerSettings:
    verbosity_level: int

settings = LoggerSettings(0)

VerbosityLow = 0
VerbosityMid = 1
VerbosityHigh = 2


_Loggable = Callable[[None], str]


# A string thunk constructor
def msg(input) -> _Loggable:
    return lambda : input


def decorator(decoration):
    def apply(input):
        return lambda : f"{decoration}{input()}\033[0m"
    return apply

purple = decorator('\033[95m')
blue = decorator('\033[94m')
cyan = decorator('\033[96m')
green = decorator('\033[92m')
orange = decorator('\033[93m')
red = decorator('\033[91m')
bold = decorator('\033[1m')
underline = decorator('\033[4m')

def padded(size, input):
    normal = (math.floor(size) * 10)
    return lambda : input().center(normal, " ")

def centered(input, seperator = " "):
    term_size = os.get_terminal_size().columns
    return lambda : input().center(term_size, seperator)

# VERBOSITY 
def verbosity(level) -> _Loggable:
    def apply(input):
        if settings.verbosity_level >= level:
            return lambda : f"{input()}"
        else: 
            return lambda: ""
    return apply
# Verbosity Loggables
nonverbose = verbosity(VerbosityLow)
semiverbose = verbosity(VerbosityMid)
verbose = verbosity(VerbosityHigh)


def log(*logs):
    for log in logs:
        out = log()
        if out != "":
            print(out, end="")

# def preface(color):
#     return f"{color}{_BOLD}PACKER{_ENDC} : {color}"


__all__ = ['log', 'nonverbose', 'semiverbose', 'verbose', 'purple', 'centered',
'blue', 'cyan', 'green', 'orange', 'red', 'bold', 'underline', 'msg', 'padded']


term_size = os.get_terminal_size().columns
test = "Hello World".center(15, " ")
test2 = test.center(term_size, "=")



