# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-03-29 12:06:55
# @Last Modified by:   JUN
# @Last Modified time: 2019-03-29 12:14:24

# 用于对整个文件进行替换

import sys


def fmain(fnlist, fni, fno):
    with open(fnlist) as fi1, open(fni) as fi2, open(fno, 'w') as fo:
        D = {}
        for line in fi1:
            Lline = line.strip().split()
            if not Lline:
                continue
            elif Lline[0] not in D:
                D[Lline[0]] = Lline[1]
            elif D[Lline[0]] != Lline[1]:
                print(Lline[0], 'key有误')
        s = fi2.read()
        for key in D:
            s = s.replace(key, D[key])
        fo.write(s)
        print('替换完毕')

def main():
    fnlist, fni, fno = sys.argv[1:4]
    fmain(fnlist, fni, fno)


if __name__ == '__main__':
    main()
