# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-03-25 10:53:52
# @Last Modified by:   JUN
# @Last Modified time: 2019-03-25 11:04:12

import sys
import re


def fmain(finame):
    with open(finame) as fi:
        for line in fi:
            Lline = line.split('\t')
            if line.startswith('#'):
                continue
            if Lline[2] == 'mRNA':
                ID = re.findall('ID=(.*?);', Lline[8])[0]
                print(Lline[0], Lline[3], Lline[4], ID, sep='\t')


def main():
    finame = sys.argv[1]
    fmain(finame)


if __name__ == '__main__':
    main()
