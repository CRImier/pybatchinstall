import json
import sys
import os
import shlex
import subprocess

def execute(*args):
    try:
        output = subprocess.check_output(args, stderr=subprocess.STDOUT, shell=True)
        result = [0, output]
    except subprocess.CalledProcessError as e:
        result = [int(e.returncode), e.output]
    return result

def transform(filename):
    output = filename+".json"
    f = open(filename, 'r')
    name = f.readline().strip("\n")
    description = f.readline().strip("\n")
    packages = f.readline().strip("\n")
    #pre_install = shlex.split(f.readline().strip("\n"))
    #post_install = shlex.split(f.readline().strip("\n"))
    json_dict = {"name":name, "description":description, "packages":[package for package in packages.split(" ") if package], "pre-install":[], "post-install":[]}
    json.dump(json_dict, open(output, "w"))

if __name__ == "__main__":
    files = [file for file in os.listdir(".") if not (file.endswith(".py") or file.endswith(".json"))]
    for file in files:
        transform(file)

    
