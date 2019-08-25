# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-02 12:01:25
# @Last Modified by:   JUN
# @Last Modified time: 2019-01-11 15:23:15

# 提取2,7,8列，其中第二列去除末尾--

import sys


def fmain(finame, foname):
    fi = open(finame)
    fo = open(foname, 'w')
    for line in fi:
        Lline = line.rstrip().split('\t')
        # Lline_new = ['_'.join(Lline[1].split('_')[:-2]), Lline[6], Lline[7]]
        Lline_new = ['_'.join(Lline[0].split('_')[:-2]), Lline[1], Lline[2]]
        fo.write('\t'.join(Lline_new) + '\n')


def main():
    finame, foname = sys.argv[1:3]
    fmain(finame, foname)

if __name__ == '__main__':
    main()
