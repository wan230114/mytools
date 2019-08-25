# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-04-11 14:52:49
# @Last Modified by:   JUN
# @Last Modified time: 2019-04-11 14:54:26

import sys
with open(sys.argv[1]) as fi, open(sys.argv[1] + '.new', 'w') as fo:
    for line in fi:
        if not line.strip():
            continue
        fo.write(line)