# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-06-09 14:56:42
# @Last Modified by:   JUN
# @Last Modified time: 2019-07-26 12:31:23

import sys


def updata(s1, s2):
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


def fmain(finame):
    D = {}
    with open(finame) as fi:
        for line in fi:
            Lline = line.strip().split('\t')
            if len(Lline) > 2:
                # (num  name)   yunnyin   xiangmu  xiangmuname
                # print(Lline)
                Ltmp = Lline[0].split()
                if len(Ltmp) == 1:
                    Ltmp.append('-')
                num, name = Ltmp
                xiangmu = Lline[2].strip('|')
                if len(xiangmu.split('|')) > 1:
                    print('Erro: 项目名有问题:')
                    print(Lline)
                    sys.exit(1)
                if xiangmu not in D:
                    #             num  name   yunnyin   xiangmu  xiangmuname
                    D[xiangmu] = [num, name, Lline[1], Lline[2], Lline[3]]
                else:
                    num = str(int(num) + int(D[xiangmu][0]))
                    name = updata(D[xiangmu][1], name)
                    xiangmuname = updata(D[xiangmu][4], Lline[3])
                    D[xiangmu] = [num, name, Lline[1], Lline[2], xiangmuname]
            else:
                D['-'] = [line.split()[0], '-', '-', '-', '-']
        #print(D.values())
        maxnum = max([len(x[0]) for x in D.values()])
        L = sorted(D.values(), key=lambda x: -int(x[0]))
        # s = '%' + str(maxnum) + 's'  # 用法：s % Lline[0]
        for Lline in L:
            print(Lline[0], Lline[1].strip('|'), Lline[2], Lline[3], Lline[4], sep='\t')


def main():
    finame = sys.argv[1]
    #finame = 'lst.merge.tiqu'
    fmain(finame)


if __name__ == '__main__':
    main()
