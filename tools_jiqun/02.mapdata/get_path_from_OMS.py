# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-06-09 14:56:42
# @Last Modified by:   JUN
# @Last Modified time: 2019-07-01 15:13:14

# 获取指定部门编号的路径

import sys
import re


def fmain(finame, bumen):
    '''所有下机文库父目录路径  部门编号（逗号隔开）'''
    Sbumen = set(bumen.split(','))
    with open(finame) as fi:
        for line in fi:
            L = re.findall('(/.*?/(\d\d\d\d)/)', line)
            if L:
                if L[0][1] in Sbumen:
                    print(L[0][0])


def main():
    fmain(*sys.argv[1:])


if __name__ == '__main__':
    main()
