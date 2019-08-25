# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-04-11 16:32:03
# @Last Modified by:   JUN
# @Last Modified time: 2019-04-11 16:46:37

# clean第9列

import sys

Sfilter = {'ID', 'Parent', 'Name'}
with open(sys.argv[1]) as fi, open(sys.argv[1] + '.col9clean', 'w') as fo:
    for line in fi:
        if line.startswith('#'):
            fo.write(line)
        else:
            Lline = line.strip().split('\t')
            Ldict = []
            for x in Lline[8].split(';'):
                Ltmp = x.split('=')
                Ldict.append(Ltmp)
            Lfilter = ['='.join(x) for x in Ldict if x[0] in Sfilter]
            Lline[8] = ';'.join(Lfilter)
            fo.write('\t'.join(Lline[:9]) + '\n')
