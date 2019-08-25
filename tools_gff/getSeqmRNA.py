# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-03-25 14:47:55
# @Last Modified by:   JUN
# @Last Modified time: 2019-03-25 15:17:26


# 从gff文件提取mRNA行对应序列

import sys
import re


def fmain(finame_gff, finame_seq, foname):
    with open(finame_seq) as fi:
        D = {}
        line = fi.readline()
        oldname = line.split()[0][1:]
        D[oldname] = []
        while True:
            line = fi.readline()
            if not line:
                D[oldname] = ''.join(D[oldname])
                break
            if line.startswith('>'):
                D[oldname] = ''.join(D[oldname])
                oldname = line.split()[0][1:]
                D[oldname] = []
            else:
                D[oldname].append(line.strip())
    print('fa读取完毕')
    with open(finame_gff) as fi:
        D2 = {x: [] for x in D}  # {chr1:[[rna1,s,e],[rna2,s,e],...], chr2:...}
        for line in fi:
            if line.startswith('#'):
                continue
            Lline = line.split('\t')
            if Lline[2] == 'mRNA':
                D2[Lline[0]].append([re.findall('^ID=(.*?);', Lline[8])[0],
                                     int(Lline[3]), int(Lline[4])])
        D2 = {x: D2[x] for x in D2 if D2[x]}
    print('gff读取完毕')
    with open(foname, 'w') as fo:
        for key in D2:
            for Ltmp in D2[key]:
                fo.write('>%s\n' % Ltmp[0])
                fo.write(D[key][Ltmp[1] - 1:Ltmp[2]] + '\n')
    print('newfa写入完毕')

def main():
    finame_gff, finame_seq, foname = sys.argv[1:]
    fmain(finame_gff, finame_seq, foname)


if __name__ == '__main__':
    main()
