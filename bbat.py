import os
import json
import shutil
import argparse
from datetime import datetime

def argDir(path):
    if os.path.isdir(path):
        return path
    else:
        raise NotADirectoryError(path)

def argFile(path):
    if os.path.isfile(path):
        return path
    else:
        raise FileNotFoundError

parser = argparse.ArgumentParser()
parser.add_argument("-i", type=argFile)
parser.add_argument("-o", type=argDir)
args = parser.parse_args()

if args.o == None: args.o = "build"
if os.path.exists(args.o) and os.path.isdir(args.o): shutil.rmtree(args.o)
os.mkdir(args.o)

bundle = {}
with open("bundle.json", encoding="utf-8") as f:
    bundle = json.loads(f.read())

def resolveInserts(path):
    content = ""
    with open(path, encoding="utf-8") as f:
        for line in f.readlines():
            if line.startswith("#insert"):
                insert = line[7:].strip().replace('"', "")
                content += resolveInserts(os.path.dirname(path) + "\\" + insert)
            else:
                content += line
    return content

now = datetime.now().strftime(r"%d/%m/%Y %H:%M:%S")
with open(args.o + "\\bundle.bat", "w", encoding="utf-8") as out:
    out.write("@echo off\n" +
              "setlocal enabledelayedexpansion\n\n" +
              "rem Created using Batch Bundler\n" +
              "rem Copyright (C) Adam Charvát\n" +
              f"rem At {now}\n" +
              "rem --------------------------------\n" +
              f"rem Name: {bundle['name']}\n" +
              f"rem Version: {bundle['version']}\n" +
              f"rem Authors: {', '.join(bundle['authors'])}\n" +
              "rem --------------------------------\n\n")
    out.write(resolveInserts(args.i))
