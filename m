#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import re
import os
import tempfile
import sys
import shutil
import subprocess
from typing import Dict, List, Tuple, Union  # , Any, Callable
from subprocess import PIPE

def prepare_exec(solver, param):
    if solver.endswith(".c"):
        cmd = ["gcc", "-Wall", "-fsanitize=address", "-Wuninitialized", "-Wparentheses", "-Wreturn-type", "-Werror"]
        cmd += ["-fno-diagnostics-color", solver, "-lm", "-lutil"] + param
        if not "-o" in param:
            cmd += ["-o", solver + ".out"]
        print(" ".join(cmd))
        result = subprocess.run(cmd)
        if result.returncode != 0:
            exit(1)
        return solver + ".out"
    elif solver.endswith(".cpp"):
        cmd = ["g++", "-std=c++17", "-Wshadow", "-Wall", "-g", "-fsanitize=address", "-fsanitize=undefined", "-D_GLIBCXX_DEBUG"]
        cmd += [solver]
        cmd += param
        if not "-o" in param:
            cmd += ["-o", solver + ".out"]
        print(" ".join(cmd))
        result = subprocess.run(cmd)
        if result.returncode != 0:
            exit(1)
        return solver + ".out"
    else:
        print("  fail: language not supported:", solver)


def main():
    if len(sys.argv) < 2:
        print("Usage: m file.c")
        exit(1)
    prepare_exec(sys.argv[1], sys.argv[2:])

if __name__ == '__main__':
    main()
    exit(0)


