# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-07 12:45:36
# @Last Modified by:   JUN
# @Last Modified time: 2019-01-07 13:53:37

import sys


def fmain(finame_list, finame_fa):
    fi_list = open(finame_list)
    fi_fa = open(finame_fa)
    fo_fa = open(finame_fa + '.new', 'w')
    print('>开始建立索引')
    S = set()
    for line in fi_list:
        data = line.strip()
        S.add(data)
    print(S)
    print('>开始筛选')
    p = 0
    Ltmp = []
    line = fi_fa.readline()
    if line.rstrip()[1:] in S:
        Ltmp.append(line)
        p = 1
    else:
        print('过滤掉: ' + line.rstrip())
    while True:
        line = fi_fa.readline()
        # print(line)
        if line.startswith('>'):
            if Ltmp:
                fo_fa.write(''.join(Ltmp))
            p = 0
            Ltmp = []
            if line.rstrip()[1:] in S:
                Ltmp.append(line)
                p = 1
            else:
                print('过滤掉: ' + line.rstrip())
        elif not line:
            if Ltmp:
                fo_fa.write(''.join(Ltmp))
            break
        elif p:
            Ltmp.append(line)


def main():
    #sys.argv = ['', 'fas_tiqu.py.list', 'fas_tiqu.py.fa']
    #sys.argv = ['', 'fas_tiqu.py.list', 'fas_tiqu.py.fa']
    finame_list, finame_fa = sys.argv[1:3]
    fmain(finame_list, finame_fa)

if __name__ == '__main__':
    main()
