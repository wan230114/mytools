# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-05-22 15:35:52
# @Last Modified by:   JUN
# @Last Modified time: 2019-05-22 16:55:22
import sys
from collections import OrderedDict


def fmain(keyname, num1, finame, num2, sep="\t"):
    num1 = int(num1) - 1
    num2 = int(num2) - 1
    D = OrderedDict()
    with open(finame) as fi:
        for line in fi:
            Lline = line.strip().split(sep)
            D[Lline[num2]] = line
    with open(keyname) as fi:
        for line in fi:
            line = line.strip()
            Lline = line.split(sep)
            if Lline[num1] in D:
                print(line, D[Lline[num1]], sep=sep)
            else:
                print(line)


def main():
    keyname, num1, finame, num2 = sys.argv[1:]
    fmain(keyname, num1, finame, num2)


if __name__ == '__main__':
    main()
