#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# @ Author: Chen Jun
# @ Author Email: 1170101471@qq.com
# @ Created Date: 2021-06-16, 11:28:55
# @ Modified By: Chen Jun
# @ Last Modified: 2023-01-13, 02:32:13
#############################################

# v0.0.1 增加 comment 参数，过滤注释行
# 下一步改进计划， 当列过短时，会破坏标题与结果的对齐，需改进
# 还有，有时候行显示不完全，很奇怪了，在一次paste的管道后接该命令

import sys
import os
import argparse


def fargv():
    parser = argparse.ArgumentParser(description='Process introduction.')
    parser.add_argument('inputfile', type=str, nargs="?",
                        help='输入需要运行的inputfile')
    parser.add_argument('-s', '--sep', type=str, default="\t",
                        help='表格分隔符')
    parser.add_argument('-n', '--headlines', type=int, default=10000,
                        help='仅打印前10000行。设置为0时，打印所有')
    parser.add_argument('--number', action='store_true',
                        help='纯净打印，不打印描述title')
    parser.add_argument('-c', '--comment', type=str, default="##",
                        help='''注释行开头标识符, shell中可以参考次语法 $'xxx', 如 : `echo $'#' $'!' !`''')
    parser.add_argument('-p', '--printclean', action='store_true',
                        help='纯净打印，不打印描述title')
    parser.add_argument('-S', '--Simplifys', type=int, default=None,
                        help='简化打印，限定最长长度字符数')
    parser.add_argument('-a', '--align', type=str, default="l", choices=["l", "r", "c"],
                        help='每一个单元格的位置。左对齐，右对齐，居中？')
    args = parser.parse_args()
    return args.__dict__


# %%
def get_str_len(word):
    LEN0 = 0
    LEN1 = 0
    for ch in word:
        # if '\u4e00' <= ch <= '\u9fff':  # "\uff08"  "\u9f01"
        if ch >= '\u3001':
            LEN1 += 1
        else:
            LEN0 += 1
    return (LEN0, LEN1)


get_str_len("测试文字（abc")

# %%
def fmain(inputfile, sep, headlines=10000, number=False, comment="#", printclean=False, Simplifys=True, align="l"):
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
    n = 0
    if not inputfile:
        while True:
            line = sys.stdin.buffer.readline()
            n += 1
            if n == headlines:
                break
            if not line:
                break
            if line.startswith(comment):
                continue
            do(line, Lline)
    else:
        with open(inputfile, 'rb') as fi:
            for line in fi:
                n += 1
                if n == headlines:
                    break
                if not line.strip():
                    continue
                do(line, Lline)
    # {行1.index: {列1:(LEN0, LEN1), 列2:(LEN0, LEN1), ... }, 行2....}
    LEN_INFO = {}
    LEN_INFO_MAX = {}
    # print(Lline)
    for n, line in enumerate(Lline):
        LEN_INFO[n] = {}
        for i, x in enumerate(line):
            # print(i, x, line, LEN_INFO[n], LEN_INFO)
            LEN_INFO[n][i] = get_str_len(x)
            LEN = LEN_INFO[n][i][0] + LEN_INFO[n][i][1]*2
            LEN = 2 if LEN < 2 else LEN
            if LEN > LEN_INFO_MAX.get(i, 0):
                LEN_INFO_MAX[i] = LEN
    LEN_number = len(str(len(Lline)))
    if not printclean:
        sys.stdout.write(("#dim: %s x %s\n" % (len(Lline), len(LEN_INFO_MAX))))
        if number:
            sys.stdout.write(("%%%dd    " % LEN_number) % 0)
        for i in LEN_INFO_MAX:
            sys.stdout.write(("#%%-%ds  " % (LEN_INFO_MAX[i]-1)) % (i+1))
        sys.stdout.write("\n")
    # 你好  4   8,(0, 2)  --> 6
    # xx好  4   8,(1, 1)  --> 7
    # xxxx  4   8,(4, 0)  --> 8
    if align == "c":
        s2 = '{:^%d}  '
        for n, line in enumerate(Lline):
            if number:
                sys.stdout.write(("%%%dd    " % LEN_number) % (n+1))
            for i, x in enumerate(line):
                sys.stdout.write(
                    (s2 % (LEN_INFO_MAX[i] - LEN_INFO[n][i][1])).format(x.strip()))
            sys.stdout.write("\n")
    else:
        # 不知道为什么format的执行效率要比%s慢一点，所以这一块单独抽离出来
        if align == "l":
            s2 = "%%-%ds  "  # s2 = '{:<%d}  '
        elif align == "r":
            s2 = "%%%ds  "  # s2 = '{:>%d}  '
        for n, line in enumerate(Lline):
            if number:
                sys.stdout.write(("%%%dd    " % LEN_number) % (n+1))
            for i, x in enumerate(line):
                sys.stdout.write(
                    (s2 % (LEN_INFO_MAX[i] - LEN_INFO[n][i][1])) % x.strip())
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
