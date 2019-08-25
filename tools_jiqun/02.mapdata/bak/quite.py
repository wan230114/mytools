# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-05-22 15:35:52
# @Last Modified by:   JUN
# @Last Modified time: 2019-05-22 18:04:35
import sys
from collections import OrderedDict


def fmain(keyname, num1, finame, num2, sep="\t"):
    num1 = int(num1) - 1
    num2 = int(num2) - 1
    D = OrderedDict()
    with open(keyname) as fi, open(finame) as fi2:
        for line in fi2:
            line = line.strip()
            Lline = line.split(sep)
            if Lline[0] not in D:
                D[Lline[num2]] = [[Lline[19], line]]
            else:
                D[Lline[num2]].append([Lline[19], line])
        for line in fi:
            line = line.strip()
            Lline = line.split(sep)
            # 判断文库
            if Lline[num1] in D:
                p = 0
                for Lline2 in D[Lline[num1]]:
                    if p == 0:
                        # 判断路径 wenku lujing lujing2  # lujing line...
                        if Lline[1] in Lline2[0]:
                            print(line, Lline2[1], sep=sep)
                            p = 1
                    else:
                        print('!%s' % line, Lline2[1], sep=sep)
            else:
                print(line)


def main():
    keyname, num1, finame, num2 = sys.argv[1:]
    fmain(keyname, num1, finame, num2)


if __name__ == '__main__':
    main()
