import os
import pathlib
import shutil
import subprocess
from loader import load_json
from builder import compile
from data import Settings, Package, PackageUnit
from util import validate_cwd_is_packer
from logger import Logger, VerbosityHigh, VerbosityLow, VerbosityMid
import argparse

arg_parser = argparse.ArgumentParser(
    prog="Packer",
    description="Packaging Build Tool for C++"
)


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

# TODO: Implement proper precondition checking 
# should not overwrite current dir if packer
# should save supplied name to manifest
def run_init():
    class arg_action(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            print(values[0])
            # packer_init()
    return arg_action



def run_build(settings: Settings, packages_manifest, logger: Logger):
    class arg_action(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            validate_cwd_is_packer("Cannot Build")
            compile(settings, packages_manifest, logger)
    return arg_action



def run_execute(settings):
    class arg_action(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            subprocess.run([f"./{settings.executable_name}"])
    return arg_action

def set_verbose(verbosity, logger: Logger):
    class arg_action(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            logger.verbosity_level = verbosity
    return arg_action



def packer_main():
    # TODO: Currently blocks --init from working
    logger = Logger(VerbosityLow)
    validate_cwd_is_packer("From Entry")
    (settings, packages_manifest) = load_json("./packer/json")
    
    arg_parser.add_argument('--verbose', metavar='', nargs=0,
        help="displays all logging information",
        action=set_verbose(VerbosityHigh, logger)
    )

    arg_parser.add_argument('--semiverbose', metavar='', nargs=0,
        help="displays some logging information",
        action=set_verbose(VerbosityMid, logger)
    )

    arg_parser.add_argument('--nonverbose', metavar='', nargs=0,
        help="displays minimal logging information",
        action=set_verbose(VerbosityLow, logger)
    )

    arg_parser.add_argument('--build', metavar="", nargs=0,
        help="executes the build for the current directory's packer.json manifest",
        action=run_build(settings, packages_manifest, logger)
    )

    arg_parser.add_argument('--run', metavar='', nargs=0,
        help='executes the current binary as specifed in the packer.json manifest',
        action=run_execute(settings)
    )

    arg_parser.add_argument('--init', metavar='', nargs=1,
        help='initializes the current directory with the proper file structure and manifest',
        action=run_init()
    )

    

    arg_parser.parse_args()



packer_main()
