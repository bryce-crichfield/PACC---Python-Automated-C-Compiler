import os
from loader import load_json
from typing import List
from data import Settings, Package, PackageUnit
import util
from logger import *


def compile(settings: Settings, packages: List[Package], logger: Logger):
    cwd = os.getcwd()
    package_objects = []
    for package in packages:
        path = compile_package(package, f"{cwd}/src/{package.id}", cwd, logger)
        logger.log(Msg("").centered("-").purple().verbose())
        package_objects.append(path)
    final_compile = "g++"
    for package_object in package_objects:
        final_compile += f" {package_object}"
    main_object_path = f"{cwd}/obj/main.o"
    main_compile_cmd = f"g++ -o {main_object_path} -c {cwd}/src/main.cpp"
    logger.log(
        Msg("Compiling Main\n").bold().orange().nonverbose(),
        Msg(f"\t{main_compile_cmd}\n").verbose(),
    )
    util.attempt(main_compile_cmd, logger)
    final_compile += f" {main_object_path} -o {cwd}/exe"
    logger.log(
        Msg("Linking Package Objects\n").bold().orange().nonverbose(),
        Msg(f"\t{final_compile}\n").verbose(),
    )
    util.attempt(final_compile, logger)


# Given a a package object and the absolute path of that package,
# compile the package, traversing through the subunit, compiling those
# into object files, then unifying the object files into a single object
# file encompassing the whole package
def compile_package(package: Package, package_path: str, root: str, logger: Logger):
    logger.log(
        Msg(f"Compiling Package ").bold().orange().nonverbose(),
        Msg(f"'{package.id}'\n").bold().blue().nonverbose(),
    )

    object_file_paths = []
    for unit in package.units:
        object_file_paths.append(
            compile_package_unit(unit, package_path, package, logger)
        )
    output_object_path = f"{root}/obj/{package.id}_pkg.o"
    relocation = f"ld -r -o {output_object_path}"
    for path in object_file_paths:
        relocation += f" {path} "
    logger.log(
        Msg("Unifying Package ").bold().orange().semiverbose(),
        Msg(f"{package.id}\n").bold().blue().semiverbose(),
        Msg(f"\t{relocation}\n").cyan().verbose(),
    )
    util.attempt(relocation, logger)
    for path in object_file_paths:
        logger.log(
            Msg(f"\tRemoving Package Object ").blue().verbose(),
            Msg(f"'{package.id}.o'\n").blue().verbose(),
        )
        util.attempt(f"rm -r {path}", logger)
    return output_object_path


def compile_package_unit(
    unit: PackageUnit, package_path: str, package: Package, logger: Logger
):
    logger.log(
        Msg(f"Compiling Package Subunit ").orange().bold().semiverbose(),
        Msg(f"'{unit.id}'\n").blue().bold().semiverbose(),
    )
    object_paths = []
    for object in unit.implementations:
        output_path = f"{package_path}/{object}.o"
        cmd = f"g++ -o {output_path} -c {package_path}/{object}.cpp"
        logger.log(Msg(f"\t{cmd}\n").verbose())
        util.attempt(cmd, logger)
        object_paths.append(output_path)
    output_object_path = f"{package_path}/{unit.id}_unit.o"
    relocation = f"ld -r -o {output_object_path}"
    for path in object_paths:
        relocation += f" {path}"
    logger.log(
        Msg(f"Unifying Subunit ").bold().orange().semiverbose(),
        Msg(f"'{unit.id}'").bold().blue().semiverbose(),
        Msg(f" of Package ").bold().orange().semiverbose(),
        Msg(f"'{package.id}'\n").bold().blue().semiverbose(),
        Msg(f"\t{relocation}\n").cyan().verbose(),
    )
    util.attempt(relocation, logger)
    for path in object_paths:
        logger.log(Msg(f"\tRemoving Subunit Object '{unit.id}.o'\n").blue().verbose())
        util.attempt(f"rm -r {path}", logger)
    return output_object_path
