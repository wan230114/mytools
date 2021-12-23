#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# @ Author: Chen Jun
# @ Author Email: 1170101471@qq.com
# @ Created Date: 2020-12-24, 15:10:57
# @ Modified By: Chen Jun
# @ Last Modified: 2021-12-23, 00:26:13
#############################################

import os
from multiprocessing import Pool
from pdf2png import *

L_res = []
for p, ds, fs in os.walk("."):
    # print(p, ds, fs)
    for f in fs:
        if f.endswith(".pdf"):
            L_res.append(os.path.join(p, f))

L_res.sort()

# files = os.popen('find ./ -type f -name "*pdf"').read()
p = Pool(5)
for i, file in enumerate(L_res, start=1):
    p.apply_async(main, args=(file,))
    # fmain(fipath + os.sep + fi, fipath + os.sep + fo)
p.close()
p.join()
