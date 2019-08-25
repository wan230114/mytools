# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-08-17 11:59:37
# @Last Modified by:   11701
# @Last Modified time: 2019-08-17 21:21:11


import sys
import argparse


def fargv():
    parser = argparse.ArgumentParser(description='Process introduction.')
    parser.add_argument('prjlist', type=str,
                        help='输入需要运行的prjlist')
    parser.add_argument('dnums', type=str,
                        help='输入需要运行的dnums，如0216,1908,1919,1920')
    # parser.add_argument('-w', '--win', type=int,
    #                     help='-w/-win的使用帮助')
    # parser.add_argument('-t', '--thread', type=int,
    #                     help='-t/--thread的帮助')
    # parser.add_argument('-k', '--iskeep', action='store_true',
    #                     default=False,
    #                     help='是否怎样怎样')
    args = parser.parse_args()
    return args.__dict__


def fmain(prjlist, dnums):
    Sdums = set(dnums.split(','))
    with open(prjlist) as fi:
        for line in fi:
            Lline = line.strip().split('\t')
            if len(Lline) >= 24 and Lline[23] in Sdums:
                print(Lline[2], Lline[3], sep='\t')


def main():
    # sys.argv = ['', 'file', 'file2']
    kwargs = fargv()
    # print(kwargs)
    # print(*list(kwargs.keys()),sep=", ")
    fmain(**kwargs)


if __name__ == '__main__':
    main()
