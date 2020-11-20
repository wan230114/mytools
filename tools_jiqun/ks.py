#!/usr/bin/env python3

# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-09 00:59:57
# @Last Modified by:   JUN
# @Last Modified time: 2019-06-11 15:51:56

""""""

import os
import argparse


def fargv():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=('“ks” ———— 进程树管理器 \n  使用keyword找寻关键字的SGID所包含的父子进程'
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
                        help='是否使用全遍历模式遍历所有父子进程')
    parser.add_argument('-c', '--children', action='store_true',
                        default=False,
                        help='是否使用去除该进程的父进程，只遍历其下子进程')
    parser.add_argument('-s', '--sigle', type=int, default=-1,
                        help='kill发送的信号值，默认不指定(系统默认为15)')
    parser.add_argument('-u', '--user', type=str, default="x",
                        help='查看谁的进程，默认为当前用户')
    args = parser.parse_args()
    # print(args)
    return args.__dict__


def fmain(keyword, view=False, all=False, children=False,
          sigle=-1, return_mode=False, user="x",
          CMD=None):
    user = "-u " + user if user != "x" else user
    CMD = 'ps %s jf' % user if not CMD else CMD
    CMD_res = os.popen(CMD).read()
    Llines = []
    S_PGID = set()
    S_PID = set()
    for NUM, line in enumerate(CMD_res.strip().split('\n'), start=1):
        Lline = line.strip().split()
        # print(Lline)
        Llines.append([Lline[2], Lline[1], line, NUM])
        if all:
            if Lline[0] in S_PID:
                S_PGID.add(Lline[2])
        if keyword in line and int(Lline[1]) != os.getpid():
            S_PGID.add(Lline[2])
            S_PID.add(Lline[1])
    Lresult = []
    Lpid = []
    for PGID in S_PGID:
        for PGID2, pid, line, NUM in Llines:
            if PGID2 == PGID:
                Lresult.append((line, NUM))
                Lpid.append(pid)
    # xjf = os.popen('''tmp="`ps xjf`"; echo -e "$tmp"|grep -v "\\-bash"|grep -v mytools/ks.py|grep %s|awk '{print $3}'|sort|uniq'''%s).read()
    # 'ps xjf|grep -v bash|grep -v mytools/ks.py|grep -v "grep %s"|grep %s' % (keyword, keyword)).read()
    if not Lresult:
        print('WARNING: 未搜索到相关进程.')
        return ""
    Lresult = sorted(Lresult, key=lambda x: x[-1])
    CMD_res = '\n'.join([x[0] for x in Lresult])
    if return_mode:
        return CMD_res
    os.system('echo -e "%s"|less -S' % CMD_res)
    if view:
        return
    os.system('echo -e "%s"' % CMD_res)
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
    # print(fargv())
    fmain(**fargv())


if __name__ == '__main__':
    main()
