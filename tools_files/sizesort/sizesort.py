# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-03-09 15:48:17
# @Last Modified by:   JUN
# @Last Modified time: 2019-03-09 16:08:17

import sys


def fmain(finame, col):
    col = int(col) - 1
    with open(finame) as fi:
        D = {'T': 1024**3, 'G': 1024**2, 'M': 1024, 'K': 1}
        L = fi.readlines()
        L = [x.strip().split('\t')for x in L]
        # print(L)
        Lnew = []
        for Lline in L:
            size = Lline[col]
            x = float(size[:-1]) * D[size[-1]]
            Lnew.append([x, Lline])
        Lnewsort = sorted(Lnew, key=lambda x: -x[0])
        Llines = [x[1] for x in Lnewsort]
        [print('\t'.join(x)) for x in Llines]


def main():
    finame, col = sys.argv[1:3]
    fmain(finame, col)


if __name__ == '__main__':
    main()
