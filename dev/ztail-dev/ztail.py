# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2018-12-24 15:00:11
# @Last Modified by:   JUN
# @Last Modified time: 2018-12-24 15:35:44

import sys
import gzip


def ztail(Largv):
    print(Largv)
    finame, N = Largv
    fi = gzip.open(finame)
    N = int(N.replace('-', ''))
    Ncount = 0
    offset = 0
    Llines = []
    # while True:
    #     if Ncount > N:
    #         break
    #     offset += -128
    #     fi.seek(offset, 2)
    #     line = fi.read()
    #     ncount = line.count(b'\n')
    #     print(ncount)
    #     Ncount += ncount
    fi.seek(-300, 2)
    print(fi.read())
    line = ''.join(Llines)
    print(line)
    # print(b'\n' in line)


def main():
    sys.argv = ['', 'Programming_exercise_1.data.fa.gz', '-10']
    sys.argv = ['', 'Programming_exercise_1.data-x7.fa.gz', '-10']
    ztail(sys.argv[1:])

if __name__ == '__main__':
    main()
