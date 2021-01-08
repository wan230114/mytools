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
        description=('“moni_cmd” ———— 命令标准输出监控器 \n  '
                     ),
        epilog=('说明：\n'
                '  谨慎使用'
                ))
    parser.add_argument('CMD', type=str,
                        help=('输入需要操作的sjm语法文件'))
    parser.add_argument('-s', '--speed', type=float, default=2,
                        help='监控的时间间隔，秒为单位，默认为5')
    parser.add_argument('--endtime', type=float, default=1,
                        help='指定结束时间，单位h，默认1h')
    args = parser.parse_args()
    # print(args)
    return args.__dict__


def fmain(CMD, speed=5, endtime=1):
    time_start = datetime.datetime.now()
    ps_info_old = "STAT: moni start\n"
    while True:
        # 判断结束
        if not ps_info_old:
            print("\nEND: moni ok.")
            time_spend = datetime.datetime.now() - time_start
            print('耗时:', time_spend)  # 耗时: 0:00:01.003083
            break
        # 截取字符串进行判断
        ps_info = os.popen(CMD).read()
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
