import os
import pathlib


OKBLUE = "\033[94m"
OKCYAN = "\033[96m"
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


def validate_cwd_is_packer(msg=""):
    dir = os.getcwd() + "/packer.json"
    settings_exist = os.path.exists(pathlib.Path(dir))
    if not settings_exist:
        err = f"{FAIL}Current Directory {dir} does not contain a packer.json file"
        if msg != "":
            err += "\n {msg}"
        raise Exception(err)
    else:
        return


def validate_src_exists(msg=""):
    dir = os.getcwd()
    src_exists = os.path.exists(pathlib.Path(dir + "/src"))
    if not src_exists:
        err = f"{FAIL}Current Directory {dir} does not contain an src directory"
        if msg != "":
            err += "\n {msg}"
        raise Exception(err)
    else:
        return


def validate_main(settings: str, msg=""):
    validate_src_exists("Cannot Validate Existence of main.cpp")
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


def check_has_package(pkgs, id):
    l = list(filter(lambda p: p.id == id, pkgs))
    return len(l) != 0


def check_has_target(pkg, target):
    t = list(filter(lambda t: t.name == target, pkg.targets))
    return len(t) != 0