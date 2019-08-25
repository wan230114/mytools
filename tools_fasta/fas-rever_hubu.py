# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2018-12-12 10:21:16
# @Last Modified by:   JUN
# @Last Modified time: 2018-12-12 11:40:31

# 获取所有序列的反向互补序列，输出到新文件


def reverse_complement(seq):
    ntComplement = {'A': 'T', 'C': 'G', 'T': 'A', 'G': 'C', 'N': 'N'}
    revSeqList = list(reversed(seq))
    revComSeqList = [ntComplement[k] for k in revSeqList]
    revComSeq = ''.join(revComSeqList)
    return revComSeq


def main(finame, foname):
    fi = open(finame)
    fo = open(foname, 'w')
    Lseq = []  # [[key,value],[]]
    seq = ''
    oldname = fi.readline()
    while True:
        line = fi.readline()
        if not line:
            seq = reverse_complement(seq)
            Lseq.append([oldname, seq])
            break
        if line.startswith('>'):
            seq = reverse_complement(seq)
            Lseq.append([oldname, seq])
            oldname = line
            seq = ''
        line = line.rstrip()
        seq += line.upper()
    for Li in Lseq:
        fo.write(Li[0])
        fo.write(Li[1])
        # i_old = 0
        # for i in range(79, len(Li[1]), 80):
        #     fo.write(Li[1][i_old:i]+'\n')
    fi.close()
    fo.close()


if __name__ == '__main__':
    finame = 'scaffold40_BIA.fa'
    foname = 'scaffold40_BIA.fa.new'
    main(finame, foname)
