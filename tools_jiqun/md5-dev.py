# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2018-12-27 13:50:49
# @Last Modified by:   JUN
# @Last Modified time: 2018-12-27 19:21:55


import os
import sys
import hashlib
import datetime
from multiprocessing import Pool


def fmain(filepath):
    s = os.popen('md5sum "%s"' % filepath).read().strip()
    print(s)
    # print(os.popen('md5sum "%s"' % filepath).read().strip())
    # global L
    # L.append(s)


def main():
    if len(sys.argv) == 1:
        x = 4
    else:
        x = int(sys.argv[1])
    p = Pool(x)
    L = []
    workpath = "."
    Iter = os.walk(workpath)
    for path, Ldic, Lfile in Iter:
        for filename in Lfile:
            filepath = '%s%s%s' % (path, os.sep, filename)
            p.apply_async(fmain, args=(filepath,))
    p.close()
    p.join()


if __name__ == '__main__':
    main()
