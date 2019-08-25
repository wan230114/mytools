# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-05-26 22:43:01
# @Last Modified by:   JUN
# @Last Modified time: 2019-05-26 22:54:47


def fprint(*args, sep=' ', end='\n', file=[]):
    for fo in file:
        args = [str(x) for x in args]
        fo.write(sep.join(args) + end)


with open('test.txt', 'w') as fo:
    fprint(1, 2, 3, 4, file=[fo, fo])
