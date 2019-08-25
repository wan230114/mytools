# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  wan230114@qq.com
# @Date:   2018-11-09 15:27:12
# @Last Modified by:   JUN
# @Last Modified time: 2019-04-11 14:52:32
# @Last Modified time: 2018-11-09 23:57:30

import sys

# sys.argv=['','../../dupin.genome.modified.fa']

path_fi = sys.argv[1]
path_fo = path_fi + '.clean'
fi = open(path_fi)
fo = open(path_fo, 'w')

while True:
    line = fi.readline()
    if not line:
        break
    Ltmp = []
    N = 0
    if line.startswith('>'):
        Ltmp.append(line)
        while True:
            line = fi.readline()
            if not line:
                break
            if line.startswith('>'):
                fi.seek(-len(line),1)
                if N < 1:
                    print(Ltmp[0]+'被遗弃，长度为：'+str(N))
                    Ltmp = []
                N = 0
                break
            Ltmp.append(line)
            N += len(line.rstrip())
    if Ltmp:
        for i in Ltmp:
            fo.write(i)
        Ltmp=[]
