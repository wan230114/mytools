# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-07-05 14:59:26
# @Last Modified by:   JUN
# @Last Modified time: 2019-07-05 16:20:37


import sys


def fmain(fitiqu):
    # D = {x.strip(): [] for x in open(filst)}
    D = {}
    with open(fitiqu, encoding='utf8') as fi:
        for line in fi:
            if line.startswith('#'):
                continue
            Lline = line.strip().split('\t')
            name = Lline[3].strip('|')
            if '|' in Lline[3].strip('|'):
                name = Lline[3].strip('|').split('|')[-1]
            if name not in D:
                D[name] = [Lline]
            else:
                D[name].append(Lline)
    for x in sorted(D):
        for Lline in D[x]:
            print(x, *Lline, sep='\t')


def main():
    fmain(sys.argv[1])
    # fmain('tongji-keep')


if __name__ == '__main__':
    main()
