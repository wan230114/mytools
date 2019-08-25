# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-04-27 00:18:22
# @Last Modified by:   JUN
# @Last Modified time: 2019-04-27 00:27:38


# 分割原文件每一列去替换，默认去除每个单词首尾空格

import time
import sys


def fmain(filist, finame, foname):
    t0 = time.time()
    D = {}
    with open(filist) as fi:
        for line in fi:
            Lline = line.strip().split('\t')
            D[Lline[0].strip()] = Lline[1].strip()
    with open(finame) as fi, open(foname, 'w') as fo:
        for line in fi:
            Lline = line.split('\t')
            Lline = [x.strip() for x in Lline]
            for i, x in enumerate(Lline):
                if x in D:
                    Lline[i] = D[x]
            newline = '\t'.join(Lline) + '\n'
            fo.write(newline)
    print('替换完成, 耗时 %s 秒' % (time.time() - t0))


def main():
    filist, finame, foname = sys.argv[1:4]
    fmain(filist, finame, foname)


if __name__ == '__main__':
    main()
