#################################################
#  File Name:merge.py
#  Author: xingpengwei
#  Mail: xingpengwei@novogene.com
#  Created Time: Sun 24 Mar 2019 09:00:38 PM CST
#################################################

import sys
import numpy as np
f1 = open('all.txt','r')
f2 = open('merge.txt','w')
name = []
size = []
for line in f1:
    line = line.strip()
    line1 = line.split()
    name.append(line1[0])
    size.append(line1[1])
uniq_name =list(set(name))
allsize2 = sum([int(aa) for aa in size])
name_array=np.array(name)
size_array=np.array(size)
mydict2 = {}
for each in uniq_name:
    myindex=np.where(name_array==each)[0]
    mysize = size_array[myindex]
    allsize=sum([int(temp) for temp in mysize])
    mydict2[each]=allsize
mydict2_sorted = sorted(mydict2.items(),key=lambda x:x[1],reverse=True)
mydict2_sorted.append(('SUM',allsize2))
for key,value in mydict2_sorted:
    allsize = value
    if int(allsize) <=1024:
        hsize=str('%.3f' % (int(allsize)))+'KB'
    elif 1024 < int(allsize) <=1024**2:
        hsize=str('%.3f' % (int(allsize)/1024))+'M'
    elif 1024**2 < int(allsize) <=1024**3:
        hsize=str('%.3f' % (int(allsize)/(1024**2)))+'G'
    else:
        hsize=str('%.3f' % (int(allsize)/1024**3))+'T'
    f2.write('%s,%s\n' % (key,hsize))
f1.close()
f2.close()
