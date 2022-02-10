#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# @ Author: Chen Jun
# @ Author Email: 1170101471@qq.com
# @ Created Date: 2021-06-16, 11:28:55
# @ Modified By: Chen Jun
# @ Last Modified: 2022-02-08, 10:05:48
#############################################

# v0.0.1 增加 comment 参数，过滤注释行
# 下一步改进计划， 当列过短时，会破坏标题与结果的对齐，需改进
# 还有，有时候行显示不完全，很奇怪了，在一次paste的管道后接该命令

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
    parser.add_argument('-c', '--comment', type=str, default="#",
                        help='''注释行开头标识符, shell中可以参考次语法 $'xxx', 如 : `echo $'#' $'!' !`''')
    parser.add_argument('-p', '--printclean', action='store_true',
                        help='纯净打印，不打印描述title')
    parser.add_argument('-S', '--Simplifys', type=int, default=None,
                        help='简化打印，限定最长长度字符数')
    parser.add_argument('-a', '--align', type=str, default="l", choices=["l", "r", "c"],
                        help='每一个单元格的位置。左对齐，右对齐，居中？')
    args = parser.parse_args()
    return args.__dict__


def fmain(inputfile, sep, comment="#", printclean=False, Simplifys=True, align="l"):
    comment = comment.encode()
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
            if line.startswith(comment):
                continue
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
    if not printclean:
        sys.stdout.write(("#dim: %s x %s\n" % (len(Lline), len(D))))
        Lline.insert(0, ["#%s" % (x+1) for x in list(D)])
        # print(Lline[:2])
    if align == "c":
        s2 = '{:^%d}  '
        for line in Lline:
            for i, x in enumerate(line):
                # 我不知道为什么format的执行效率要比%s慢一点，所以这一块单独抽离出来
                sys.stdout.write((s2 % D[i]).format(x.strip()))
            sys.stdout.write("\n")
    else:
        if align == "l":
            s2 = "%%-%ds  "  # s2 = '{:<%d}  '
        elif align == "r":
            s2 = "%%%ds  "  # s2 = '{:>%d}  '
        for line in Lline:
            for i, x in enumerate(line):
                sys.stdout.write((s2 % D[i]) % x.strip())
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
