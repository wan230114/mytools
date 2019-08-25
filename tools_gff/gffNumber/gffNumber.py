# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  wan230114@qq.com
# @Date:   2018-11-20 15:49:39
# @Last Modified by:   JUN
# @Last Modified time: 2019-05-03 22:53:27

# 此函数用于更改gff文件里CDS的相同序号，输出文件为后缀加.Number

import sys
import re

# if sys.version_info[0] < 3:
#     print("Erro: can not run in python2")
#     sys.exit(0)  # exit programe

finame = sys.argv[1]
# finame = "Arabidopsis_thaliana.TAIR10.37.gff3"
foname = finame +'.Number'

fi = open(finame, 'rb')
fo = open(foname, 'wb')

Nrow = 0
nCDS = 0

while True:
    line = fi.readline()
    Nrow += 1
    if not line:
        break
    elif line.startswith(b'#'):
        continue
    Lline = line.split(b'\t')
    if Lline[2] == b'gene':
        fo.write(line)
        while True:
            line = fi.readline()
            Lline = line.split(b'\t')
            Nrow += 1
            if not line:
                break
            elif Lline[2] == b'gene':
                fi.seek(-len(line), 1)
                Nrow -= 1
                break
            elif Lline[2] == b'mRNA':
                nCDS = 0
            elif Lline[2] == b'CDS':
                nCDS += 1
                oldID = re.findall(b'ID=(CDS:.*?);', Lline[8])[0]
                newIDtmp = oldID.replace(b'CDS:', b'')
                newID = newIDtmp + b'.CDS' + str(nCDS).encode()
                line = line.replace(oldID, newID)
            else:
                print('文件中含有非gene、mRNA、CDS的行，行数是: %d' % Nrow)
                sys.exit()
            fo.write(line)
