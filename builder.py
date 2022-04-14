from imp import reload
import os
from packer import packer_validate_src_exists, packer_warning, Settings
from loader import Package, PackageUnit, load_json
from typing import List

def compile(settings: Settings, packages: List[Package]):
    cwd = os.getcwd()
    package_objects = []
    for package in packages:
        path = compile_package(package, f"{cwd}/src/{package.id}", cwd)
        package_objects.append(path)
    final_compile = "g++"
    for package_object in package_objects: 
        final_compile += f" {package_object}"
    main_object_path = f"{cwd}/obj/main.o"
    main_compile_cmd = f"g++ -o {main_object_path} -c {cwd}/src/main.cpp"
    os.system(main_compile_cmd)
    final_compile += f" {main_object_path} -o {cwd}/exe"
    os.system(final_compile)

# Given a a package object and the absolute path of that package,
# compile the package, traversing through the subunit, compiling those
# into object files, then unifying the object files into a single object
# file encompassing the whole package
def compile_package(package: Package, package_path: str, root: str):
    object_file_paths = []
    for unit in package.units:
        object_file_paths.append(compile_package_unit(unit, package_path))
    output_object_path = f"{root}/obj/{package.id}_pkg.o"
    relocation = f"ld -r -o {output_object_path}"
    for path in object_file_paths: 
        relocation += f" {path} "
    os.system(relocation)
    for path in object_file_paths: 
        os.remove(path)
    return output_object_path

def compile_package_unit(unit: PackageUnit, package_path: str):
    object_paths = []
    for object in unit.implementations:
        output_path = f"{package_path}/{object}.o"
        cmd = f"g++ -o {output_path} -c {package_path}/{object}.cpp "
        os.system(cmd)
        object_paths.append(output_path)
    output_object_path = f"{package_path}/{unit.id}.o"
    relocation = f"ld -r -o {output_object_path}"
    for path in object_paths: 
        relocation += f" {path}"
    result = os.system(relocation)
    for path in object_paths: 
        os.remove(path)
    return output_object_path


