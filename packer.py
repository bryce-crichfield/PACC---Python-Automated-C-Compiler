from compileall import compile_dir
from dataclasses import dataclass
import json
import os
import pathlib
import shutil
import sys
import subprocess
from typing import List, Tuple
from loader import load_json
from builder import compile

# Utility And Error ========================================================== #
OKBLUE = "\033[94m"
OKGREEN = "\033[92m"
WARNING = "\033[93m"
FAIL = "\033[91m"


def packer_error(msg):
    print(FAIL + "PACKER : " + msg)


def packer_warning(msg):
    print(WARNING + "PACKER : " + msg)


def packer_panic(msg):
    print(FAIL + "PACKER : " + msg)
    exit(-1)


def packer_validate_cwd_is_packer(msg=""):
    dir = os.getcwd() + "/packer.json"
    settings_exist = os.path.exists(pathlib.Path(dir))
    if not settings_exist:
        err = f"{FAIL}Current Directory {dir} does not contain a packer.json file"
        if msg != "":
            err += "\n {msg}"
        raise Exception(err)
    else:
        return


def packer_validate_src_exists(msg=""):
    dir = os.getcwd()
    src_exists = os.path.exists(pathlib.Path(dir + "/src"))
    if not src_exists:
        err = f"{FAIL}Current Directory {dir} does not contain an src directory"
        if msg != "":
            err += "\n {msg}"
        raise Exception(err)
    else:
        return


def packer_validate_main(settings: str, msg=""):
    packer_validate_src_exists("Cannot Validate Existence of main.cpp")
    dir = os.getcwd()
    target_main = ""
    if settings.compiler == "gcc":
        target_main = "c"
    if settings.compiler == "g++":
        target_main = "cpp"
    main_exists = os.path.exists(pathlib.Path(dir + f"/src/main.{target_main}"))
    if not main_exists:
        err = f"{FAIL}Current Directory {dir} does not contain a main file"
        if msg != "":
            err += "\n {msg}"
        raise Exception(err)
    else:
        return


def packer_has_package(pkgs, id):
    l = list(filter(lambda p: p.id == id, pkgs))
    return len(l) != 0


def packer_has_target(pkg, target):
    t = list(filter(lambda t: t.name == target, pkg.targets))
    return len(t) != 0


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


def packer_init():
    absolute = os.getcwd()
    print(f"{OKGREEN}Creating Project at {OKBLUE}{absolute}")
    os.mkdir(f"{absolute}/src")
    os.mkdir(f"{absolute}/obj")
    main_path = f"{absolute}/src/main.cpp"
    pathlib.Path(main_path).touch()
    with open(main_path, "a") as file:
        file.write("int main(void)\n{\n\treturn 0;\n}")
    packer_path = os.path.dirname(os.path.abspath(__file__))
    settings_path = f"{absolute}/packer.json"
    def_sets = f"{packer_path}/default_settings.json"
    shutil.copyfile(def_sets, settings_path)
    os.chdir(absolute)


def packer_run_init():
    packer_init()
    exit(1)


def packer_run_build(settings: Settings, manifest):
    packer_validate_cwd_is_packer("Cannot Build")
    compile(settings, packages_manifest)


def packer_run_execute(settings):
    subprocess.run([f"./{settings.executable_name}"])


def packer_main():
    if len(sys.argv) == 1:
        print(f"{FAIL}No Arguments Provided")
        return
    arg = sys.argv[1]
    if arg == "-i":
        packer_run_init()
    packer_validate_cwd_is_packer("From Entry")
    (settings, packages_manifest) = load_json("./packer/json")
    if arg == "-b":
        packer_run_build(settings, packages_manifest)
    elif arg == "-r":
        packer_run_execute(settings)
    else:
        print(f"{FAIL}Could Not Parse First Arg : {arg}")


packer_main()
