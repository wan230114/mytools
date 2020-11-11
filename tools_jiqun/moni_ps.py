#!/usr/bin/env python3

'''
 # @ Author: Jun
 # @ Create Time: 2020-09-01 14:42:53
 # @ Modified by: Jun
 # @ Description: 监控 ps xjf 运行，找出流程内部运行脚本
'''

import os
import sys
import re
import datetime
import time
import ks
import argparse


def fargv():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=('“moni_ps” ———— 进程树监控器 \n  使用keyword找寻关键字的SGID所包含的父子进程'
                     ),
        epilog=('说明：\n'
                '  谨慎使用'
                ))
    parser.add_argument('keyword', type=str,
                        help=('输入需要操作的sjm语法文件'))
    parser.add_argument('-s', '--speed', type=float, default=2,
                        help='监控的时间间隔，秒为单位，默认为2')
    parser.add_argument('-u', '--user', type=str, default="x",
                        help='查看谁的进程，默认为当前用户')
    args = parser.parse_args()
    # print(args)
    return args.__dict__


def fmain(keyword, speed=1, user="x"):
    time_start = datetime.datetime.now()
    ps_info_old = "STAT: moni start\n"
    L_ps_info = []
    CMD = 'ps %s jf|grep -v moni_ps' % user
    while True:
        # 判断结束
        if not ps_info_old:
            print("\nEND: moni ok.")
            time_spend = datetime.datetime.now() - time_start
            print('耗时:', time_spend)  # 耗时: 0:00:01.003083
            break
        # 截取字符串进行判断
        ps_info = ks.fmain(keyword, return_mode=True,
                           user=user, CMD=CMD).strip()
        if not ps_info:
            print("ps_info is None.")
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
                "\n[Now_time] : %Y-%m-%d %H:%M:%S", time.localtime()))
            print(ps_info)
        ps_info_old = ps_info
        time.sleep(speed)


def main():
    # print(fargv())
    fmain(**fargv())


if __name__ == '__main__':
    main()
