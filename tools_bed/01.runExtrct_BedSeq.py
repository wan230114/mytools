# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2018-12-28 16:55:29
# @Last Modified by:   JUN
# @Last Modified time: 2019-01-10 10:37:26

# 提取bed文件中的序列
# bed文件可乱序
# fa文件可为多行

import sys
import gzip


def fmain(fi_bed, fi_fa, fo_fa):
    # 1) 读取bed文件
    L = []
    with open(fi_bed, 'rb') as fi:
        for line in fi:
            Lline = line.rstrip().split(b'\t')
            L.append(Lline)

    # 2) 建立长度的字典
    D = dict([[x[0],[]] for x in L])
    for Lline in L:
        D[Lline[0]].append(Lline[1:])
    # print(D)

    # 3) 读取序列文件，遍历每一个在字典中的基因
    fo = open(fo_fa, 'wb')

    def f(ID, seq):
        if ID in D:
            for Ltmp in D[ID]:
                fo.write(b'>%s_%s_%s\n' % (ID, Ltmp[0], Ltmp[1]))
                fo.write(b'%s\n' % (seq[int(Ltmp[0]) - 1:int(Ltmp[1])]))

    def getseq(fi):
        L = []
        while True:
            line = fi.readline()
            if not line.startswith(b'>'):
                L.append(line.rstrip())
            else:
                fi.seek(-len(line), 1)
                break
            if not line:
                break
        return b''.join(L)

    if fi_fa.endswith('.gz'):
        fi = gzip.open(fi_fa, 'rb')
    else:
        fi = open(fi_fa, 'rb')

    ID = fi.readline().strip().replace(b'>', b'')
    seq = getseq(fi)
    f(ID, seq)
    while True:
        ID = fi.readline().strip().replace(b'>', b'')
        seq = getseq(fi)
        if not ID:
            break
        f(ID, seq)

    fi.close()
    fo.close()


def main():
    # sys.argv = ['', 'all.chain.filter.tnet.synnet.axt.tp.bed.merge.unmap', 'tar.fa', '01.result.fa']
    fi_bed, fi_fa, fo_fa = sys.argv[1:]
    fmain(fi_bed, fi_fa, fo_fa)

if __name__ == '__main__':
    main()
