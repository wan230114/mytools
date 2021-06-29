#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# @ Author: Chen Jun
# @ Author Email: 1170101471@qq.com
# @ Created Date: 2021-06-17, 00:00:15
# @ Modified By: Chen Jun
# @ Last Modified: 2021-06-17, 00:27:33
#############################################

import sys
import argparse
import os


def fargv():
    parser = argparse.ArgumentParser(description='Process introduction.')
    parser.add_argument('inputfile', type=str, nargs="?",
                        help='输入需要运行的inputfile')
    parser.add_argument('-c', '--Cols', type=str,
                        help='cols，如"colname1,colname3,colname2')
    parser.add_argument('-sc', '--sepCols', type=str, default=",",
                        help='sepCols, 输入筛选列的参数的分隔符, 默认 “,”')
    parser.add_argument('-si', '--sepInfile', type=str, default="\t",
                        help='sepInfile, Infile\'s sep, default: “\\t”')
    parser.add_argument('-so', '--sepOutfile', type=str, default="\t",
                        help='sepOutfile, 输出文件的分隔符, 默认 “\\t”')
    parser.add_argument('-o', '--outfile', type=str,
                        help='outfile, 输出文件路径。 默认输出到标准输出')
    parser.add_argument('-H', '--Header', action="store_true",
                        help='Header, 输出的文件是否打印Header。 默认 False')
    # parser.add_argument('-k', '--iskeep', action='store_true',
    #                     default=False,
    #                     help='是否怎样怎样')
    args = parser.parse_args()
    return args.__dict__


def fmain(inputfile, Cols, sepCols=",", sepInfile="\t", sepOutfile="\t",
          outfile=None, Header=False):
    def do(line, Lline):
        try:
            line = line.decode('utf8')
        except UnicodeDecodeError:
            line = line.decode('gbk')
        Lline.append(line.strip(os.linesep).split(sepInfile))
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
    HEADER = dict(zip(Lline[0], range(len(Lline[0]))))
    HEADER_index = [HEADER[x] for x in Cols.split(sepCols)]
    it = Lline if Header else Lline[1:]
    for line in it:
        sys.stdout.write(line[HEADER_index[0]])
        for ii in HEADER_index[1:]:
            sys.stdout.write(sepOutfile)
            sys.stdout.write(line[ii])
        sys.stdout.write("\n")
        # sys.stdout.write(("%%-%ds  " % D[i]) % x.strip())


def main():
    # sys.argv = ['', 'file', 'file2']
    kwargs = fargv()
    # print(kwargs)
    # print(*list(kwargs.keys()),sep=", ")
    fmain(**kwargs)


if __name__ == '__main__':
    main()
