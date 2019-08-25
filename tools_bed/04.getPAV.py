# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-18 11:48:38
# @Last Modified by:   JUN
# @Last Modified time: 2019-01-21 10:32:28

import sys


def func(finame):
    with open(finame) as fi,\
            open(finame + '.genelen', 'w') as fo:
        line = fi.readline()
        Lline = line.strip().split()
        name = Lline[0]
        sumall = 0
        sumtmp = int(Lline[2]) - int(Lline[1]) + 1
        while True:
            line = fi.readline()
            Lline = line.strip().split()
            if not line:
                fo.write(name + '\t' + str(sumtmp) + '\n')
                sumall += sumtmp
                break
            if Lline[0] == name:
                sumtmp += (int(Lline[2]) - int(Lline[1]) + 1)
            else:
                fo.write(name + '\t' + str(sumtmp) + '\n')
                sumall += sumtmp
                name = Lline[0]
                sumtmp = int(Lline[2]) - int(Lline[1]) + 1
        print('%s\t%s' % (finame, sumall))


def main():
    if len(sys.argv) == 1:
        sys.argv = ['', 'result_Pcui.bed']
    finame = sys.argv[1]
    func(finame)

if __name__ == '__main__':
    main()
