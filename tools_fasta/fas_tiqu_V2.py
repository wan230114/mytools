# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-07 12:45:36
# @Last Modified by:   JUN
# @Last Modified time: 2019-06-25 18:08:19

# 平均每G需要10秒钟

import sys


def fmain(finame_list, finame_fa, foname_fa=None, Doption={}):
    fi_list = open(finame_list)
    if not foname_fa:
        if len(finame_list.split('.')) > 1:
            foname_fa = '.'.join(finame_list.split('.')[:-1]) + '.fa'
        else:
            foname_fa = finame_list + '.fa'
    fi_fa = open(finame_fa)
    fo_fa = open(foname_fa, 'w')
    print('\n> 输入: %s, %s' % (finame_list, finame_fa),  file=sys.stderr)
    S = set()
    for line in fi_list:
        if line.strip():
            data = line.strip()
            S.add(data)
    print('> 开始筛选',  file=sys.stderr)
    S_filter = set()
    p = 0
    Ltmp = []
    line = fi_fa.readline()
    genename = line.strip()[1:].split()[0]
    if line.rstrip()[1:] in S:
        Ltmp.append(line)
        S_filter.add(genename)
        p = 1
    # else:
    #     print('过滤掉: ' + line.rstrip(),  file=sys.stderr)
    while True:
        line = fi_fa.readline()
        # print(line,  file=sys.stderr)
        if line.startswith('>'):
            if Ltmp:
                fo_fa.write(''.join(Ltmp))  # .rstrip()+'\n'
            p = 0
            Ltmp = []
            genename = line.strip()[1:].split()[0]
            if genename in S:
                S_filter.add(genename)
                Ltmp.append('>%s\n' % genename)
                p = 1
            # else:
            #     print('过滤掉: ' + line.rstrip(),  file=sys.stderr)
        elif not line:
            if Ltmp:
                fo_fa.write(''.join(Ltmp))  # .rstrip()+'\n'
            break
        elif p:
            # if Doption.get('--notline',1):
            #     Ltmp.append(line.strip())
            # else:
            Ltmp.append(line)

    print('筛选结束, 筛选了%s个(总共:%s), --> %s' %
          (len(S_filter), len(S), foname_fa), file=sys.stderr)
    if S - S_filter:
        print('\n总待筛选的基因有：',  file=sys.stderr)
        print(S,  file=sys.stderr)
        print('\n筛选的基因有：',  file=sys.stderr)
        print(S_filter,  file=sys.stderr)
        print('Warning: 存在未筛选的基因：',  file=sys.stderr)
        print(S - S_filter,  file=sys.stderr)
    else:
        print('[ok.] 已检测全部筛选完毕',  file=sys.stderr)


def main():
    # sys.argv = ['', 'fas_tiqu.py.list', 'fas_tiqu.py.fa']
    # sys.argv = ['', 'fas_tiqu.py.list', 'fas_tiqu.py.fa']
    finame_list, finame_fa = sys.argv[1:3]
    try:
        foname_fa = sys.argv[3]
    except Exception:
        foname_fa = None
    fmain(finame_list, finame_fa, foname_fa)


if __name__ == '__main__':
    main()
