# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-14 09:43:39
# @Last Modified by:   JUN
# @Last Modified time: 2019-01-14 10:02:45

import sys


def fmain(finame, foname):
    print(finame, foname)
    with open(finame) as fi,\
            open(foname, 'w') as fo:
        L = []
        for line in fi:
            Lline = line.strip().split()
            L.append(Lline)
        print('排序中...')
        newL = sorted(L, key=lambda x: (x[0], int(x[1]), int(x[2])))
        for Lline in newL:
            fo.write('\t'.join(Lline) + '\n')
        print(foname, '写入完成')


def main():
    finame, foname = sys.argv[1:]
    fmain(finame, foname)

if __name__ == '__main__':
    main()
