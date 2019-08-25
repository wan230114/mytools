# -*- coding: utf-8 -*-
# @Author: JUN
# @Date:   2018-10-30 11:32:40
# @Last Modified by:   JUN
# @Last Modified time: 2018-11-20 18:50:55

import sys


def fclean(Largv):
    fname = Largv[1]
    fname_new = fname + '.clean'
    fi = open(fname, 'rb')
    fo = open(fname_new, 'wb')
    fo.write(b"##gff-version 3\n")

    Nrow = 0  # 记录行数
    seek_old = 0  # 初始变量
    # 设置集合，用于判断基因类型，看gene,mRNA,CDS是否都有
    S_genetype_raw = {b'mRNA', b'CDS'}
    S_genetype = set()

    print('读取中...')
    while True:
        line = fi.readline()
        Nrow += 1
        if line.startswith(b"#"):
            continue
        if not line:  # 判断是否到文件末尾
            break
        # print(line)
        S_genetype = set()  # 每次进入前归零
        Ltmp = []
        # print(line)
        genetype = line.split(b'\t')[2]
        if genetype == b'gene':
            Ltmp.append(line)
            while True:
                line = fi.readline()
                Nrow += 1
                if not line:  # 判断是否到文件末尾
                    break
                genetype = line.split(b'\t')[2]
                if genetype == b'gene':
                    if S_genetype != S_genetype_raw:
                        # print('该基因缺失mRNA或CDS，已跳过该基因，位于行数为 %d 之前的一个基因' % Nrow)
                        # print('%s' % line)
                        # print(S_genetype,S_genetype_raw)
                        Ltmp = []
                    fi.seek(-len(line), 1)  # 回退光标
                    Nrow -= 1
                    break
                if genetype in S_genetype_raw:
                    # print(genetype)
                    S_genetype.add(genetype)
                    Ltmp.append(line)
        if Ltmp:
            Ltmp = sort(Ltmp)
            for line in Ltmp:
                fo.write(line)
def sort()

if __name__ == "__main__":
    sys.argv = ['', "t-raw.gff3"]
    fclean(sys.argv)
