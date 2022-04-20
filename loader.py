
from dataclasses import dataclass
import json
import os
from typing import List, Set, Tuple
from util import validate_cwd_is_packer
from data import Settings, Package, PackageUnit




# TODO: Add proper error checking for differences in JSON and Directory
def load_json(path) -> Tuple[Settings, List[Package]]:
    validate_cwd_is_packer("Cannot Load Settings")
    with open(os.getcwd() + "/packer.json") as file:
        data = json.loads(file.read())
        settings = load_settings(data)
        packages_json = load_packages_json(data)
        packages_dir = load_packages_directory(path)
        # if len(packages_dir) != len(packages_json):
            # raise Exception("Load JSON failed: pkgs dir and pkgs mismatch")
        for pkg_json in packages_json:
            pkg_dir = filter(lambda p: p.id == pkg_json.id, packages_dir)
            # compare_directory_and_report(pkg_json, pkg_dir)
        return (settings, packages_json)

def load_settings(data) -> Settings:
    c = data["compiler"]
    a = " ".join(data["compiler-args"])
    l = " ".join(data["compiler-libs"])
    exe = data["executable-name"]
    ign = data["ignores"]
    return Settings(c, a, l, exe, ign)

# Load the Packages as they are listed in the JSON
# Note: loads only the names, not the extensions
def load_packages_json(data) -> List[Package]:   
    pkgs = []
    for json_pkg in data["packages"]:
        defs = []
        for json_def in json_pkg["defs"]:
            impls = json_def["impls"]
            defs.append(PackageUnit(json_def["id"], impls))
        pkgs.append(Package(json_pkg["id"], defs))
    return pkgs

# Load the Packages as they appear in the directory
# Note: loads both the names and the extensions
def load_packages_directory(path) -> List[Package]:
    pkgs = []
    dirs = [dir[1] for dir in os.walk(os.getcwd() + "/src")][0]
    for dir_name in dirs:
        files = [file[2] for file in os.walk(os.getcwd() + f"/src/{dir_name}")][0]
        objects = [name for name in files]
        # pkgs.append(CompilationUnit(dir_name, objects))
    return pkgs

# Compare the reported packages as per the JSON and Directory
# If they match this will return safely, otherwise throw error
def compare_directory_and_report(from_json, from_dir):
    unique_names = Set()
    for object in from_dir.objects:
        unique_names.append(object.split(".", 1)[0])
    if len(unique_names) != len(from_json.objects):
        raise Exception("Directory and JSON don't match")

