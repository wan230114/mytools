# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-05-21 12:43:14
# @Last Modified by:   JUN
# @Last Modified time: 2019-05-23 21:36:55

###########################################################
# 功能简介：用于只输出那一行的文库名
###########################################################

import sys


def cleanWenkuName(wenkuname):
    # newwenkuname = '-'.join(wenkuname.split('-')[:2])
    # return newwenkuname
    return wenkuname


def fmain(finame):
    # with open(finame) as fi, open(finame_wenku) as fi_wenku:
    with open(finame) as fi:
        # L = []
        # for line in fi_wenku:
        #     Lline = [line] + line.strip().split('\t')
        for line in fi:
            Lline = line.strip().split()
            Ldir = Lline[-1].split('/')
            if '.' in Ldir[-1]:
                print(cleanWenkuName(Ldir[-2]), '/'.join(Ldir[:-1]), Lline[-1], sep='\t')
                # if Ldir[-1].endswith('.adapter.list.gz') \
                #         or Ldir[-1].endswith('.fq.gz') \
                #         or Ldir[-1].endswith('adap.stat'):
                #     print(cleanWenkuName(Ldir[-2]), '/'.join(Ldir[:-1]), Lline[-1], sep='\t')
                # else:
                #     print(cleanWenkuName(Ldir[-1].split('.')[0]),
                #           '/'.join(Ldir[:-1]), Lline[-1], sep='\t')
            else:
                print(cleanWenkuName(Ldir[-1]),
                      '/'.join(Ldir), Lline[-1], sep='\t')


def main():
    finame = sys.argv[1]
    fmain(finame)

if __name__ == '__main__':
    main()
