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
from data import Settings, Package, PackageUnit
from util import OKBLUE, OKGREEN, FAIL, validate_cwd_is_packer


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


def packer_run_build(settings: Settings, packages_manifest):
    validate_cwd_is_packer("Cannot Build")
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
    validate_cwd_is_packer("From Entry")
    (settings, packages_manifest) = load_json("./packer/json")
    if arg == "-b":
        packer_run_build(settings, packages_manifest)
    elif arg == "-r":
        packer_run_execute(settings)
    else:
        print(f"{FAIL}Could Not Parse First Arg : {arg}")


packer_main()
