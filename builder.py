from asyncio.log import logger
from imp import reload
import os
from subprocess import PIPE, Popen
from time import sleep
from loader import load_json
from typing import List
from data import Settings, Package, PackageUnit
from util import packer_warning, packer_error
from util import OKBLUE, OKCYAN

from logger import *

def id_string(id: str, color = blue) -> str:
    return bold(color(msg(f"'{id}'")))()


def compile(settings: Settings, packages: List[Package]):
    cwd = os.getcwd()
    package_objects = []
    for package in packages:
        path = compile_package(package, f"{cwd}/src/{package.id}", cwd)
        log(verbose(purple(centered(msg(""), "-"))))
        package_objects.append(path)
    final_compile = "g++"
    for package_object in package_objects: 
        final_compile += f" {package_object}"
    main_object_path = f"{cwd}/obj/main.o"
    main_compile_cmd = f"g++ -o {main_object_path} -c {cwd}/src/main.cpp"

    log (
        nonverbose(orange(bold(msg("Compiling Main\n")))),
        verbose(cyan(msg(f"\t{main_compile_cmd}\n")))
    )

    os.system(main_compile_cmd)
    final_compile += f" {main_object_path} -o {cwd}/exe"

    log (
        nonverbose(orange(bold(msg("Linking Package Objects\n")))),
        verbose(cyan(msg(f"\t{final_compile}\n")))
    )
    os.system(final_compile)


# Given a a package object and the absolute path of that package,
# compile the package, traversing through the subunit, compiling those
# into object files, then unifying the object files into a single object
# file encompassing the whole package
def compile_package(package: Package, package_path: str, root: str):
    
    log (
        nonverbose(bold(orange(
            msg(f"Compiling Package {id_string(package.id)}\n")
    ))))

    object_file_paths = []
    for unit in package.units:
        object_file_paths.append(compile_package_unit(unit, package_path, package))
    output_object_path = f"{root}/obj/{package.id}_pkg.o"
    relocation = f"ld -r -o {output_object_path}"
    for path in object_file_paths: 
        relocation += f" {path} "
    log (
        semiverbose(orange(bold(msg(f"Unifying Package {id_string(package.id)}\n")))),
        verbose(cyan(msg(f"\t{relocation}\n")))
    )
    os.system(relocation)
    for path in object_file_paths: 
        log ( verbose(blue(msg(f"\tRemoving Package Object '{package.id}.o'\n"))) )
        os.remove(path)
    return output_object_path

def compile_package_unit(unit: PackageUnit, package_path: str, package: Package):
    log (
        semiverbose(bold(orange(
            msg(f"Compiling Package SubUnit {id_string(unit.id)}\n")
    ))))
    # packer_warning(f"Compiling Package Unit '{unit.id}'")
    object_paths = []
    for object in unit.implementations:
        output_path = f"{package_path}/{object}.o"
        cmd = f"g++ -o {output_path} -c {package_path}/{object}.cpp "
        log ( verbose(cyan(msg(f"\t{cmd}\n"))) )
        os.system(cmd)
        object_paths.append(output_path)
    output_object_path = f"{package_path}/{unit.id}_unit.o"
    relocation = f"ld -r -o {output_object_path}"
    for path in object_paths: 
        relocation += f" {path}"

    log (
        semiverbose(orange(bold(msg(f"Unifying Subunit {id_string(unit.id)}")))),
        semiverbose(orange(bold(msg(f" of Package {id_string(package.id)}\n")))),
        verbose(cyan(msg(f"\t{relocation}\n")))
    )

    result = os.system(relocation)
    for path in object_paths: 
        log ( verbose(blue(msg(f"\tRemoving Subunit Object '{unit.id}.o'\n"))) )
        os.remove(path)
    return output_object_path


