#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# @ Author: Chen Jun
# @ Author Email: 1170101471@qq.com
# @ Created Date: 2021-01-03, 03:36:10
# @ Modified By: Chen Jun
# @ Last Modified: 2021-02-13, 00:32:01
#############################################
# %%
import psutil
import argparse
import time
import sys
import os


def fargv():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=('“moni_free” ———— 资源监控器'),
        epilog=('说明：\n'
                '  谨慎使用'
                ))
    # parser.add_argument('keyword', type=str,
    #                     help=('输入需要操作的sjm语法文件'))
    parser.add_argument('-s', '--speed', type=float, default=2,
                        help='监控的时间间隔，秒为单位，默认为2')
    parser.add_argument('-o', '--out', type=str, default=None,
                        help='输出文件，默认为stdout')
    args = parser.parse_args()
    # print(args)
    return args


def getsize(size):
    D = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    try:
        for x in D:
            if int(size) < 1024**(x + 1):
                hsize = str('%.3f' % (int(size) / 1024**x)) + D[x]
                return hsize
    except ValueError:
        # print(size, 'have eero')
        return size


def get_used_stat():
    c_counts = psutil.cpu_count()
    c_per = psutil.cpu_percent(percpu=False)
    c_counts_used = c_counts * c_per / 100
    m = psutil.virtual_memory()
    stat_c = f'{c_per:.2f}%\t{c_counts_used:.2f}\t{c_counts}'
    stat_m = f'{m.percent:.2f}%\t{getsize(m.used)}\t{getsize(m.total)}\t{m.used}\t{m.total}'
    return stat_c + "\t" + stat_m


def moni_free(shm=[0], speed=2, out=sys.stdout):
    out = open(out.replace(os.sep, "."), "a") if out else sys.stdout        
    while True:
        print(time.strftime("%Y-%m-%d %H:%M:%S",
                            time.localtime()),
              get_used_stat(), file=out, sep="\t")
        if shm[0] == 1:
            break
        time.sleep(speed)


if __name__ == "__main__":
    # import sys
    # sys.argv = [""]
    args = fargv()
    moni_free([0], args.speed, args.out)
