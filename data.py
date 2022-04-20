from dataclasses import dataclass
from typing import List


@dataclass
class Settings:
    compiler: str
    compiler_args: str
    compiler_libs: str
    executable_name: str
    ignores: List[str]

    def __init__(self, c: str, a: str, l: str, e: str, ignores: List[str]):
        self.compiler = c
        self.compiler_args = a
        self.compiler_libs = l
        self.executable_name = e
        self.ignores = ignores

@dataclass 
class PackageUnit:
    id: str
    implementations: List[str]

@dataclass
class Package:
    id: str
    units: List[PackageUnit]