#!/bin/env python3

# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-09 00:59:57
# @Last Modified by:   JUN
# @Last Modified time: 2019-06-11 15:51:56

""""""

import os
import sys
import argparse


def fargv():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=('“ks” ———— 进程树管理器 \n  使用keyword找寻关键字的SGID父子进程'
                     ),
        epilog=('说明：\n'
                '  谨慎使用'
                ))
    parser.add_argument('keyword', type=str,
                        help=('输入需要操作的sjm语法文件'))
    parser.add_argument('-v', '--view', action='store_true',
                        default=False,
                        help='是否只打印进程树')
    parser.add_argument('-a', '--all', action='store_true',
                        default=False,
                        help='是否使用严格模式遍历所有父子进程')
    parser.add_argument('-s', '--sigle', type=int, default=-1,
                        help='kill发送的信号值，默认不指定(系统默认为15)')
    args = parser.parse_args()
    # print(args)
    return args.__dict__


def fmain(keyword, view=False, all=False, sigle=-1):
    xjf = os.popen('''ps xjf|grep -v mytools/tools_jiqun/ks.py|grep -v mytools/bin/ks''').read()
    Llines = []
    S_PGID = set()
    S_PID = set()
    for NUM, line in enumerate(xjf.strip().split('\n'), start=1):
        Lline = line.strip().split()
        # print(Lline)
        Llines.append([Lline[2], Lline[1], line, NUM])
        if all:
            if Lline[0] in S_PID:
                S_PGID.add(Lline[2])
        if keyword in line:
            S_PGID.add(Lline[2])
            S_PID.add(Lline[1])
    Lresult = []
    Lpid = []
    for PGID in S_PGID:
        for PGID2, pid, line, NUM in Llines:
            if PGID2 == PGID:
                Lresult.append(line)
                Lpid.append(pid)
    # xjf = os.popen('''tmp="`ps xjf`"; echo -e "$tmp"|grep -v "\\-bash"|grep -v mytools/ks.py|grep %s|awk '{print $3}'|sort|uniq'''%s).read()
    # 'ps xjf|grep -v bash|grep -v mytools/ks.py|grep -v "grep %s"|grep %s' % (keyword, keyword)).read()
    if not Lresult:
        print('WARNING: 未搜索到相关进程.')
        sys.exit()
    Lresult = sorted(Lresult, key=lambda x: x[-1])
    xjf = '\n'.join(Lresult)
    os.system('echo -e "%s"|less -S' % xjf)
    if view:
        sys.exit()
    os.system('echo -e "%s"' % xjf)
    if sigle == -1:
        print('准备使用`kill PIDs`命令杀死以下PID的进程')
        print(Lpid)
        if input('是否删除以上进程(y/[n])？') == 'y':
            os.system('kill ' + ' '.join(Lpid))
    else:
        print('准备使用`kill -s %s PIDs`命令杀死以下PID的进程' % sigle)
        print(Lpid)
        if input('是否删除以上进程(y/[n])？') == 'y':
            os.system('kill -s %s ' % sigle + ' '.join(Lpid))


def main():
    fmain(**fargv())


if __name__ == '__main__':
    main()
