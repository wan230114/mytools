# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-16 14:00:11
# @Last Modified by:   JUN
# @Last Modified time: 2019-01-18 12:57:44

import os
import sys

sys.path.append('/ifs/TJPROJ3/Plant/chenjun/mytools/tools_fasta')
sys.path.append('E:\\我的云同步\\ALLdata\\mytools\\tools_fasta')


def mkdir(mkpath, p=0):
    if p not in {0, 1}:
        print('参数传入错误')
        sys.exit(1)
    isExists = os.path.exists(mkpath)
    if not isExists:
        print('文件夹%s创建成功' % mkpath)
        os.makedirs(mkpath)
    elif p == 1:
        print('Error: 文件夹%s已存在' % mkpath)
        sys.exit(1)
    elif p == 0:
        print('Warning: 文件夹%s已存在' % mkpath)
