#!/usr/bin/env python3

__author__ = "Jerome Kieffer"
__date__ = ""
__license__ = "MIT"

import sys


def is_header(line):
    "return order of the header"
    line = line.strip()
    order = 0
    if line:
        while line[0] == line[-1] == "=":
            order += 1
            line = line[1:-1]
    return order


def fix_header(rline):
    header = is_header(rline)
    if header:
            rline = rline.strip().strip("=")
            h = "="*max(0, 7 - header)
            rline = h + rline + h
    return rline


def bulleted_list(rline):
    sline = rline.strip()
    if sline[0] == "*":
        index = rline.index("*")
        rline = f"<bulleted order={index}>{sline[1:].strip()}"
    return rline


def numbered_list(rline):
    sline = rline.strip()
    if sline.find('.') > 0 and rline[0] == " ":
        rstart = rline.index(".")
        sstart = sline.index(".")
        if " " not in sline[:sstart]:
            index = rstart - sstart
        rline = f"<numbered order={index}>{sline[sstart+1:].strip()}"
    return rline


def formating(line):
    line = line.replace("'''", "**")  # bold
    line = line.replace("''", "//")  # italic
    line = line.replace("`", "''")  # monospaced
    line = line.replace("--(", "<del>")  # deleted
    line = line.replace(")--", "</del>")  # deleted
    return line


if __name__ == "__main__":
    document = {}
    with open(sys.argv[1], "r") as r:
        for line in r:
            rline = line.rstrip()
            document[line] = rline
    for line, rline in document.items():
        if rline:
            rline = formating(numbered_list(bulleted_list(fix_header(rline))))
        document[line] = rline
    print("\n".join(document.values()))

