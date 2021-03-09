#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# @ Author: Chen Jun
# @ Author Email: 1170101471@qq.com
# @ Created Date: 2021-03-02, 20:33:40
# @ Modified By: Chen Jun
# @ Last Modified: 2021-03-09, 09:05:55
#############################################

import os
import sys
import re
import datetime
import time
import ks
from multiprocessing import Process, Array
import argparse
import getpass


def fargv():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=('“moni_ps” ———— 进程树监控器 \n'
                     '  使用keyword找寻关键字的SGID所包含的父子进程\n'
                     '  （监控 ps xjf 运行，找出流程内部运行脚本）'
                     ),
        epilog=('说明：\n'
                '  None'
                ))
    parser.add_argument('keyword', type=str,
                        help=('输入需要操作的sjm语法文件'))
    parser.add_argument('-s', '--speed', type=float, default=2,
                        help='监控的时间间隔，秒为单位，默认为2')
    parser.add_argument('-u', '--user', type=str, default=getpass.getuser(),
                        help='查看谁的进程，默认为当前用户')
    parser.add_argument('-S', '--Stat', action='store_true',
                        help='是否查看运行状态，默认为False')
    parser.add_argument('--noFlush', action='store_true',
                        help='是否使用缓存机制输出日志？适用于高速监控间隔对于IO资源的缓和利用。默认不使用，直接输出日志')
    args = parser.parse_args()
    # print(args)
    return args.__dict__


def fmain(keyword, speed=1, user=getpass.getuser(), Stat=False, noFlush=False):
    FLUSH_STAT = False if noFlush else True
    time_start = datetime.datetime.now()
    ps_info_old = "STAT: moni start\n"
    shm = Array('i', [0])
    if Stat:
        import moni_free
        p = Process(target=moni_free.moni_free,
                    args=(shm, 10, "moni_free_" + keyword + ".log"))
        p.start()
    L_ps_info = []
    CMD = 'ps -u %s jf|grep -v moni_ps' % user
    while True:
        # 判断结束
        if not ps_info_old:
            print("\nEND: moni ok.", flush=FLUSH_STAT)
            time_spend = datetime.datetime.now() - time_start
            print('耗时:', time_spend, flush=FLUSH_STAT)  # 耗时: 0:00:01.003083
            break
        # 截取字符串进行判断
        ps_info = ks.fmain(keyword, return_mode=True,
                           user=user, CMD=CMD).strip()
        if not ps_info:
            print("ps_info is None.", flush=FLUSH_STAT)
            ps_info_old = ps_info
            continue
        L_ps_info.clear()
        for line in ps_info.split('\n'):
            result = line.split(maxsplit=8)[-1]
            result = re.findall(" .*", result)[0]
            L_ps_info.append(result)
        ps_info = '\n'.join(L_ps_info)
        # print(ps_info)
        # os.popen("ks -v %s|cat" % keyword).read()
        if ps_info != ps_info_old:
            print(time.strftime(
                "\n[Now_time] : %Y-%m-%d %H:%M:%S", time.localtime()),
                ps_info, sep="\n", flush=FLUSH_STAT)
        ps_info_old = ps_info
        time.sleep(speed)
    shm[0] = 1
    if Stat:
        p.join()


def main():
    # print(fargv())
    try:
        fmain(**fargv())
    except KeyboardInterrupt:
        print("Terminated: KeyboardInterrupt.", flush=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
