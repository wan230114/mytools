# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2018-11-25 14:06:50
# @Last Modified by:   JUN
# @Last Modified time: 2018-11-25 16:17:26

# 此函数为了实现标准化输出gene,mRNA,CDS的第9列，只留 ID与Parent 或 ID与Name
# 局限性：只能使用这两项为前两项用;隔开
# gene  ID=...;Name=...
# mRNA  ID=...;Parent=...
# CDS  ID=...;Parent=...

import sys
import re
import time

t0 = time.time()
Largv = sys.argv

Largv = ['', 't.gff3.sort']
finame = Largv[1]
foname = finame + '.clean'
fi = open(finame)
fo = open(foname, 'w')
print('输入的文件是: %s' % finame)
print('输出的文件是: %s' % foname)
print('处理中')

for line in fi:
    if line.startswith('#'):
        fo.write(line)
        continue
    Lline = line.rstrip().split('\t')
    LID = Lline[8].split(';')[:2]
    newID = ';'.join(LID)
    newline = '\t'.join(Lline[:8] + [newID]) + '\n'
    fo.write(newline)

print('格式化处理完毕，耗时%f秒' % (time.time() - t0))
