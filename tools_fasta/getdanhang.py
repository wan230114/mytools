# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-03-21 19:07:52
# @Last Modified by:   JUN
# @Last Modified time: 2019-04-09 17:42:00

import os
import sys


def fmain(finame):
    with open(finame) as fi, \
            open(finame.split(os.sep)[-1] + '.oneline', 'w') as fo:
        Lline = []
        line_name = fi.readline()
        while True:
            line = fi.readline()
            if not line:
                fo.write(line_name)
                fo.write(''.join(Lline) + '\n')
                break
            if line.startswith('>'):
                fo.write(line_name)
                line_name = line
                if Lline:
                    fo.write(''.join(Lline) + '\n')
                    Lline = []
                continue
            Lline.append(line.upper().strip())


def main():
    finame = sys.argv[1]
    fmain(finame)


if __name__ == '__main__':
    main()
