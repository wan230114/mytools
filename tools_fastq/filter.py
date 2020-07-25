'''
 # @ Author: ChenJun
 # @ Create Time: 2020-07-22 10:18:35
 # @ Modified time: 2020-07-22 10:32:05
 # @ Description:
 '''

import sys
import gzip

finame, foname = sys.argv[1:3]
left = int(sys.argv[3])
right = int(sys.argv[4])

with (gzip.open(finame) if finame.endswith('.gz') else open(finame)) as fi, \
     (gzip.open(foname, 'w') if foname.endswith('.gz')
      else open(foname, 'w')) as fo:
    i = 0
    L_tmp = []
    for line in fi:
        i += 1
        L_tmp.append(line)
        if i % 4 == 0:
            if left <= len(L_tmp[1].strip()) <= right:
                fo.write(''.join(L_tmp))
            i = 0
            L_tmp.clear()
