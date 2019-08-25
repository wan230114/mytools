# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-06-09 14:56:42
# @Last Modified by:   JUN
# @Last Modified time: 2019-08-12 11:28:23

import sys


def updata(s1, s2):
    '''输入：a|b|c   b|d
    返回：a|b|c|d'''
    L1 = s1.split('|')
    L2 = s2.split('|')
    newL = []
    for x in L1:
        if x not in newL:
            newL.append(x)
    for x2 in L2:
        if x2 not in newL:
            newL.append(x2)
    if '' in newL:
        newL.remove('')
    return '|'.join(newL)


def dealfile(finame):
    '''输入下机的map文件，lst.merge.final'''
    D = {}  # {xiangmu:[num, name, yunnyin, xiangmu, xiangmuname],...}
    with open(finame, 'rb') as fi:
        for line in fi:
            line = line.decode('utf8')
            Lline = line.strip().split('\t')
            if len(Lline) > 2:
                if len(Lline) > 23:
                    name, yunnyin = Lline[24], Lline[23]
                else:
                    name, yunnyin = 'None', 'None'
                for i in (4, 5):
                    if not Lline[i]:
                        Lline[i] = 'None'
                xiangmu, xiangmuname = Lline[4], Lline[5]
                if Lline[4] not in D:
                    # print(len(Lline))
                    # [print(x) for x in enumerate(Lline)]
                    D[Lline[4]] = [1, name, yunnyin,
                                   xiangmu, xiangmuname]
                else:
                    L = []
                    for x1, x2 in zip(D[Lline[4]][1:],
                                      [name, yunnyin,
                                       xiangmu, xiangmuname]):
                        # print(x1, x2)
                        L.append(updata(x1, x2))
                    D[Lline[4]] = [D[Lline[4]][0] + 1] + L
            else:
                if '-' not in D:
                    D['-'] = [1, '-', '-', '-', '-']
                else:
                    D['-'][0] += 1
    L = sorted(D.values(), key=lambda x: (-x[0], x[3]))
    [print(*x, sep='\t') for x in L]


def main():
    finame = sys.argv[1]
    # finame = 'lst.merge.final'
    # finame = 'lst.merge.tiqu'
    # fmain(finame)
    dealfile(finame)


if __name__ == '__main__':
    main()
