# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-03-25 14:47:55
# @Last Modified by:   JUN
# @Last Modified time: 2019-03-27 17:21:16


# 从gff文件提取CDS行对应序列
# 同一个CDS名字合并，最后负链反转

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
    with open(finame_gff) as fi, open(foname, 'w') as fo:
        oldID = ''
        oldP = ''
        Ltmp = []
        for line in fi:
            if line.startswith('#'):
                continue
            Lline = [x.strip() for x in line.split('\t')]
            if Lline[2] == 'CDS':
                newID = re.findall('Parent=(.*?);', Lline[8])[0]
                # print(newID)
                if oldID == newID:
                    if Lline[6] == '-':
                        Ltmp.insert(0, D[Lline[0]][int(Lline[3]) - 1:int(Lline[4])])
                    else:
                        Ltmp.append(D[Lline[0]][int(Lline[3]) - 1:int(Lline[4])])
                elif oldID:
                    if oldP == '-':
                        s = ''.join(Ltmp)[::-1]
                    else:
                        s = ''.join(Ltmp)
                    fo.write('>%s\n' % oldID)
                    fo.write(s + '\n')
                    oldP = Lline[6]
                    oldID = newID
                    Ltmp = [D[Lline[0]][int(Lline[3]) - 1:int(Lline[4])]]
                else:
                    oldID = newID
                    oldP = Lline[6]
                    Ltmp = [D[Lline[0]][int(Lline[3]) - 1:int(Lline[4])]]
        if oldP == '-':
            s = ''.join(Ltmp)[::-1]
        else:
            s = ''.join(Ltmp)
        fo.write('>%s\n' % oldID)
        fo.write(s + '\n')
    print('写入完毕 -->', foname)


def main():
    finame_gff, finame_seq, foname = sys.argv[1:]
    fmain(finame_gff, finame_seq, foname)


if __name__ == '__main__':
    main()
