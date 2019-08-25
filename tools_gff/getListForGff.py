# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-22 16:32:01
# @Last Modified by:   JUN
# @Last Modified time: 2019-02-15 16:57:25

import sys
import re


def fmain(finame, foname):
    fi = open(finame)
    fo = open(foname, 'w')
    for line in fi:
        Lline = line.rstrip().split('\t')
        if Lline[2] == 'gene':
            genename = re.findall('ID=(.*?);', Lline[8])[0]
            fo.write('\t'.join(['.', genename, Lline[0],
                                Lline[3], Lline[4], Lline[6]]) + '\n')
    print('提取列表完毕，%s --> %s' % (finame, foname))


def main():
    finame, foname = sys.argv[1:]
    fmain(finame, foname)


if __name__ == '__main__':
    main()
