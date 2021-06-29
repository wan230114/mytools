#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# @ Author: Chen Jun
# @ Author Email: 1170101471@qq.com
# @ Created Date: 2021-06-16, 11:28:55
# @ Modified By: Chen Jun
# @ Last Modified: 2021-06-21, 16:28:33
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
    parser.add_argument('-c', '--clean', action='store_true',
                        help='纯净打印，不打印描述title')
    parser.add_argument('-S', '--Simplifys', type=int, default=None,
                        help='简化打印，限定最长长度字符数')
    args = parser.parse_args()
    return args.__dict__


def fmain(inputfile, sep, clean=False, Simplifys=True):
    if Simplifys:
        def do(line, Lline):
            try:
                line = line.decode('utf8')
            except UnicodeDecodeError:
                line = line.decode('gbk')
            L_tmp = []
            for x in line.strip(os.linesep).split(sep):
                if len(x) > Simplifys:
                    L_tmp.append(x[:Simplifys] + "...")
                else:
                    L_tmp.append(x)
            Lline.append(L_tmp)
    else:
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
            LEN = 2 if LEN < 2 else LEN
            if LEN > D.get(i, 0):
                D[i] = LEN
    if not clean:
        sys.stdout.write(("#dim: %s x %s\n" % (len(Lline), len(D))))
        Lline.insert(0, ["#%s" % (x+1) for x in list(D)])
        # print(Lline[:2])
    for line in Lline:
        for i, x in enumerate(line):
            sys.stdout.write(("%%-%ds  " % D[i]) % x.strip())
        sys.stdout.write("\n")


def main():
    # sys.argv = ['', 'file', 'file2']
    kwargs = fargv()
    # print(kwargs)
    # print(*list(kwargs.keys()),sep=", ")
    try:
        fmain(**kwargs)
    except BrokenPipeError:
        pass


if __name__ == '__main__':
    main()
