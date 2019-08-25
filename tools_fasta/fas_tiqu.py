# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-07 12:45:36
# @Last Modified by:   JUN
# @Last Modified time: 2019-05-31 13:33:01

# 平均每G需要10秒钟

import sys
from collections import OrderedDict


def fmain(S, finame_fa):
    '''
    输入：
        S = {genename1, genename2, ...}
        finame_fa = 待提取的fa文件的name
    返回:
        提取后的字典{genename1:ATGGGCCC, genename2:ATGGGCCC, ...}
    '''
    with open(finame_fa) as fi_fa:
        print('> 开始筛选')
        S_filter = set()
        p = 0  # p==1时开始写入Ltmp
        D = OrderedDict()
        Ltmp = []
        line = fi_fa.readline()
        genename = line.strip()[1:].split()[0]
        if genename in S:
            p = 1
        for line in fi_fa:
            if line.startswith('>'):
                if Ltmp:
                    D[genename] = ''.join(Ltmp).strip()
                p, Ltmp = (0, [])
                genename = line.strip()[1:].split()[0]
                if genename in S:
                    p = 1
                    if genename in D:
                        print("Warning, 发现重复基因: %s" % genename)
            elif p:
                Ltmp.append(line.strip().upper())
        if p:
            D[genename] = ''.join(Ltmp).strip()
        print('筛选结束, 筛选了%s个基因' % len(D))
        if S - set(D):
            print('总待筛选的基因有：')
            print(S)
            print('筛选的基因有：')
            print(S_filter)
            print('Warning: 存在未筛选的基因：')
            print(S - S_filter)
        else:
            print('[ok.] 已检测全部筛选完毕')
        return D


def writefile(D, finame_list, foname_fa=None):
    if not foname_fa:
        if len(finame_list.split('.')) > 1:
            foname_fa = '.'.join(finame_list.split('.')[:-1]) + '.fa'
        else:
            foname_fa = finame_list + '.fa'
    fo_fa = open(foname_fa, 'w')
    for genename in D:
        fo_fa.write('>%s\n%s\n' % (genename, D[genename]))


def get_S_fromlist(finame_list):
    fi_list = open(finame_list)
    # print('\n> 输入: %s, %s' % (finame_list))
    S = set()
    for line in fi_list:
        if line.strip():
            data = line.strip()
            S.add(data)
    return S


def main():
    # sys.argv = ['', 'fas_tiqu.py.list', 'fas_tiqu.py.fa']
    # sys.argv = ['', 'fas_tiqu.py.list', 'fas_tiqu.py.fa']
    finame_list, finame_fa = sys.argv[1:3]
    try:
        foname_fa = sys.argv[3]
    except Exception:
        foname_fa = None
    D = fmain(get_S_fromlist(finame_list), finame_fa)
    writefile(D, finame_list, foname_fa)


if __name__ == '__main__':
    main()
