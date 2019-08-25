# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-06-09 14:56:42
# @Last Modified by:   JUN
# @Last Modified time: 2019-07-10 10:05:15

import sys
import gzip
import argparse


def fargv():
    parser = argparse.ArgumentParser(description='''本程序用于merge多个vcf文件。
        1.只保留第一个文件的前面#信息; 
        2.从表头#CHROM开始只保留第一个文件前8列，之后的按输入文件顺序后9列合并''')
    parser.add_argument('-i', '--input', type=str, nargs='+',
                        help='输出文件名字')
    parser.add_argument('-o', '--out', type=str,
                        help='输出文件名字')
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.parse_args(['', '--help'])
        sys.exit(1)
    return args.input, args.out


def fmain(finames, foname):
    print(finames, foname)
    Lopenfi = [gzip.open(x) for x in finames]
    fo = gzip.open(foname, 'w')
    Ltmp = [None] * len(Lopenfi)  # 用来存读取的所有文件的某一行
    # 1)表头处理
    p = 1
    while True:
        if not p:
            break
        Ltmp2 = []
        for i, fi in enumerate(Lopenfi):
            line = fi.readline()
            if not line:
                p = 0
            if line.startswith(b'#CHROM'):
                p = 0
                Lline = line.rstrip().split(b'\t', 9)
                Ltmp[i] = Lline[:9]
                Ltmp2.extend(Lline[9:])
            elif i == 0:
                fo.write(line)
    Lbiaotou = Ltmp[0] + Ltmp2
    fo.write(b'\t'.join(Lbiaotou) + b'\n')
    # exit()
    # 2)表身处理
    p = 1
    while True:
        if not p:
            break
        Ltmp = []  # 存储前8列
        Ltmp2 = []  # 存储第9列之后的所有列 [file1, file2, ... ]
        for i, fi in enumerate(Lopenfi):
            line = fi.readline()
            if not line:
                p = 0
                break
            Lline = line.rstrip().split(b'\t', 9)
            Ltmp2.extend(Lline[9:])
            if i == 0:
                Ltmp = Lline[:9]
        if p:
            Lline = Ltmp + Ltmp2
            fo.write(b'\t'.join(Lline) + b'\n')
    fo.close()


def main():
    # sys.argv = ['', '-i', 'a', 'b', 'c', '-o', 'a']
    fi, fo = fargv()
    fmain(fi, fo)


if __name__ == '__main__':
    main()
