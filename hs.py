#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import re
from typing import Dict, List, Tuple, Union  # , Any, Callable

class Case:
    def __init__(self, cmd, input, output):
        self.cmd = cmd
        self.input = input
        self.output = output

    @staticmethod
    def load_from_line(line: str):
        parts = line.split("==")
        #remove first word
        
        _input = parts[0].strip().split(" ")
        _cmd = _input[0]
        del _input[0]
        #remove empty words
        _input = [item for item in _input if item != ""]
        _input  = "\n".join(_input)
        _output = parts[1].strip()
        return Case(_cmd, _input, _output)
    
    def to_tio(self):
        return ">>>>>>>>\n" + self.input + "\n========\n" + self.output + "\n<<<<<<<<"

    def to_vpl(self):
        return "case=\ninput=" + self.input + "\noutput=\"" + self.output + "\n\"\n"
    
    def __eq__(self, test):
        return (self.cmd == test.cmd) and (test.input == self.input) and (test.output == self.output)



class HFile:
    @staticmethod
    def __filter_lines(lines: List[str]) -> List[str] :
        lines = [line.strip() for line in lines]
        lines = [line for line in lines if not line.startswith("--")]
        lines = [line for line in lines if not line.startswith("```")]
        lines = [line for line in lines if "==" in line]
        return lines

    @staticmethod
    def __extract_hs(text: str) -> str:
        regex = r"```hs(.*?)\n```"
        match_list = re.findall(regex, text, re.MULTILINE | re.DOTALL)
        return "\n".join(match_list)


    @staticmethod
    def load_from_text(text: str) -> List[Case]:
        text = HFile.__extract_hs(text)
        lines = text.split("\n")
        lines = HFile.__filter_lines(lines)
        tests = []
        for line in lines:
            tests.append(Case.load_from_line(line))
        return tests


class HMain:
    @staticmethod
    def is_int(token):
        try: 
            int(token)
            return True
        except ValueError:
            return False

    @staticmethod
    def _convert_token(token: str) -> str:
        if token.startswith("["):
            return "<- readLn :: IO [Int]"
        elif HMain.is_int(token):
            return "<- readLn :: IO Int"
        else:
            return "<- getLine"

    @staticmethod
    def format_main(test: Case) -> str:
        out = "main = do\n"
        var = "a"
        tab = "    "
        print_cmd = tab + "print $ " + test.cmd
        lines = test.input.split("\n")
        for line in lines:
            out += tab + var + " " + HMain._convert_token(line) + "\n"
            print_cmd += " " + var
            var = chr(ord(var) + 1)
        return out + print_cmd + "\n"

def read_from_file(path: str):
    with open(path, "r") as f:
        return f.read()

def add_main(readme, readme_file, main_str):
    regex = r"<!--MAIN_BEGIN-->(.*)<!--MAIN_END-->"
    found = re.search(regex, readme, re.MULTILINE | re.DOTALL)
    subst = "<!--MAIN_BEGIN-->\\n### Main\\n```hs\\n" + main_str + "\\n```\\n<!--MAIN_END-->\n"
    if found:
        result = re.sub(regex, subst, readme, 0, re.MULTILINE | re.DOTALL)
        if result != readme:
            print("changed, replacing Main")
            with open(readme_file, "w") as f:
                f.write(result)
    else:
        print("Not found, adding Main")
        add = "\n\n<!--MAIN_BEGIN-->\n### Main\n```hs\n" + main_str + "\n```\n<!--MAIN_END-->\n"
        with open(readme_file, "w") as f:
            f.write(readme + add)

def main():
    parser = argparse.ArgumentParser(prog='hs.py', description="gerador haskell to vpl", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('input', type=str, help='arquivo de entrada')
    parser.add_argument('--vpl', '-v', action='store', type=str, help="arquivo para salvar o vpl")
    parser.add_argument('--main', '-m', action='store', type=str, help="arquivo para salvar a main")
    parser.add_argument("--update", action='store_true', help="Update main inside Readme")
    args = parser.parse_args()

    readme = read_from_file(args.input)

    tests = HFile.load_from_text(readme)
    output = ""
    for test in tests:
        output += test.to_vpl() + "\n" + "\n"
    main_str = HMain.format_main(tests[-1])
    if args.update:
        add_main(readme, args.input, main_str)

    if args.vpl:
        with open(args.vpl, "w") as f:
            f.write(output)
    else:
        print(output)
        
    if args.main:
        with open(args.main, "w") as f:
            f.write(main_str)
    else:
        print(main_str)


if __name__ == '__main__':
    main()


