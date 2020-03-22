#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import re
import os
import subprocess
import tempfile
from shutil import copyfile
from typing import Dict, List, Tuple, Union  # , Any, Callable


def main():
    parser = argparse.ArgumentParser(prog='hs.py', description="gerador haskell to vpl", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('input', type=str, help='arquivo de entrada')
    args = parser.parse_args()

    with open(args.input) as f:
        text = f.read()


    regex = r"(^#+[ \S]*?`(\S+)`[ \S]*?)\n(.*?)```\n"
    match_list = re.findall(regex, text, re.MULTILINE | re.DOTALL)
    for match in match_list:
        header = match[0]
        solver = match[1]
        content = header + "\n" + match[2] + "\n```"
        solver_file = "__" + solver + ".hs"
        if os.path.isfile(solver_file):
            folder = tempfile.mkdtemp()
            print(folder)
            solver_dest: str = os.path.join(folder, "solver.hs")
            copyfile(solver_file, solver_dest)
            with open(os.path.join(folder, "Readme.md"), "w") as f:
                f.write(content)
            subprocess.run(["htest.sh", folder])
            subprocess.run(["pandoc", os.path.join(folder, "Readme.md"), "--metadata", "title=" + solver, "--standalone", "-o", "." + solver + ".html"])
            copyfile(os.path.join(folder, ".vpl"), "." + solver + ".vpl")

if __name__ == '__main__':
    main()


