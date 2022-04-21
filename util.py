import os
import pathlib
import subprocess

from logger import Logger, Msg


def attempt(cmd, logger):
    split = list(filter(lambda string: string != '' or string != ' ', cmd.split(" ")))
    split2 = list(filter(lambda string: string != '', split))
    process = subprocess.Popen(split2, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    out = stdout.decode('utf-8')
    err = stderr.decode('utf-8')
    if out != "":
        logger.log (
            Msg(f"Subprocess Out: \n").bold().green().semiverbose(),
            Msg(f"{out}").semiverbose()
        )
    if err != "":
        logger.log (
            Msg(f"Subprocess Error: \n").red().nonverbose(),
            Msg(f"{err}").red().nonverbose()
        )
        exit(-1)
    



def packer_panic(msg, logger: Logger):
    logger.log(
        Msg(msg).red().blue().nonverbose()
    )
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