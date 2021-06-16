#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# @ Author: Chen Jun
# @ Author Email: 1170101471@qq.com
# @ Created Date: 2021-06-16, 11:28:55
# @ Modified By: Chen Jun
# @ Last Modified: 2021-06-17, 00:14:29
#############################################

import sys
import os
import argparse
from collections import OrderedDict


def fargv():
    parser = argparse.ArgumentParser(description='Process introduction.')
    parser.add_argument('inputfile', type=str, nargs="?",
                        help='输入需要运行的inputfile')
    parser.add_argument('-s', '--sep', type=str, default="\t",
                        help='表格分隔符')
    # parser.add_argument('-k', '--iskeep', action='store_true',
    #                     default=False,
    #                     help='是否怎样怎样')
    args = parser.parse_args()
    return args.__dict__


def fmain(inputfile, sep):
    def do(line, Lline):
        try:
            line = line.decode('utf8')
        except UnicodeDecodeError:
            line = line.decode('gbk')
        Lline.append(line.strip(os.linesep).split(sep))
    Lline = []
    if not inputfile:
        while True:
            line = sys.stdin.buffer.readline()
            if not line:
                break
            do(line, Lline)
    else:
        with open(inputfile, 'rb') as fi:
            for line in fi:
                if not line.strip():
                    continue
                do(line, Lline)
    D = OrderedDict()
    for line in Lline:
        for i, x in enumerate(line):
            LEN = len(x.strip())
            if LEN > D.get(i, 0):
                D[i] = LEN
    for line in Lline:
        for i, x in enumerate(line):
            sys.stdout.write(("%%-%ds  " % D[i]) % x.strip())
        sys.stdout.write("\n")


def main():
    # sys.argv = ['', 'file', 'file2']
    kwargs = fargv()
    # print(kwargs)
    # print(*list(kwargs.keys()),sep=", ")
    fmain(**kwargs)


if __name__ == '__main__':
    main()
