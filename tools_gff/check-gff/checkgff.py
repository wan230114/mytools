# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  wan230114@qq.com
# @Date:   2018-11-13 11:29:01
# @Last Modified by:   JUN
# @Last Modified time: 2018-11-13 11:41:09

# 本函数用于检测gff文件中没有键值对的值存在

import sys
import re

sys.argv = ['', 't-raw.gff3.clean']
fi_name = sys.argv[1]
fi = open(fi_name)
Nrow = 0
for line in fi:
    Nrow += 1
    if line.startswith('#'):
        continue
    # print(line)
    line8 = line.split('\t')[8]
    Lline8 = line8.split(';')
    perr = 0
    for x in Lline8:
        if '=' not in x:
            perr = 1
    if perr == 1:
        print('%d\t%s'%(Nrow,line))
    perr = 0
