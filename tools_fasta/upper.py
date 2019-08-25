# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-04-08 21:14:09
# @Last Modified by:   JUN
# @Last Modified time: 2019-04-15 17:37:20

import sys


def fmain(finame, foname=None):
    if not foname:
        foname = finame + '.upper'
    with open(finame) as fi, open(foname, 'w') as fo:
        for line in fi:
            if not line.startswith('>'):
                line = line.upper()
            fo.write(line)
    print('转换大写完毕，', finame, '-->', foname)


def main():
    finame = sys.argv[1]
    foname = None
    if len(sys.argv) > 2:
        foname = sys.argv[2]
    fmain(finame, foname)


if __name__ == '__main__':
    main()
