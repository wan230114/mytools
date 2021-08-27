#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# @ Author: Chen Jun
# @ Author Email: 1170101471@qq.com
# @ Created Date: 2021-08-27, 23:25:12
# @ Modified By: Chen Jun
# @ Last Modified: 2021-08-27, 23:57:43
#############################################

"""
psutil.disk_io_counters(perdisk=False, nowrap=True)
返回全系统磁盘 I/O 统计作为命名的 Tuple，包括以下字段：
read_count： 阅读次数
write_count： 写作次数
read_bytes： 字节读数
write_bytes： 字节数
平台特定字段：
read_time： （除NetBSD和OpenBSD外 ） 从磁盘（以毫秒为单位）阅读的时间
write_time： （除Netbsd和Openbsd外 ） 写到磁盘的时间 （以毫秒为单位）
busy_time：（Linux， FreeBSD） 花在做实际 I/Os 上的时间 （以毫秒为数）
read_merged_count （Linux）： 合并读取次数 （见iostats 文书）)
write_merged_count （Linux）： 合并的写作数量 （见iostats 文书）)
"""

# %%
from ctypes import c_char_p
from multiprocessing import Process, Manager
import os
import time
import curses
import psutil

# %%


def getsize(size):
    D = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T', 5: "P"}
    try:
        for x in D:
            if int(size) < 1024**(x + 1):
                hsize = str('%.3f' % (int(size) / 1024**x)) + D[x]
                return hsize
    except ValueError:
        return size


def get_speed(oldr, oldw, time0):
    d = psutil.disk_io_counters(perdisk=True)
    newr, neww = [], []
    for disk in d:
        newr.append(d[disk].read_bytes)
        neww.append(d[disk].write_bytes)
    # print(d.keys(), oldr, newr, oldw, neww, sep="\n")
    time1 = time.time()
    T = time1 - time0
    s = ["统计间隔时间：%.3fs\n" % T]
    for name, o, n, o2, n2 in zip(d.keys(), oldr, newr, oldw, neww):
        sp1 = (n-o)/T
        sp2 = (n2-o2)/T
        s_new = ["%5s  " % name,
                 "  r: %-10s" % (getsize(sp1)+"/s"),
                 "  w: %-10s" % (getsize(sp2)+"/s"),
                 "\n"]
        s += s_new
    oldr, oldw = newr, neww
    return ''.join([str(x) for x in s]), oldr, oldw


def get_speed_main(s_Value):
    try:
        d = psutil.disk_io_counters(perdisk=True)
        oldr, oldw = [], []
        for disk in d:
            oldr.append(d[disk].read_bytes)
            oldw.append(d[disk].write_bytes)
        while True:
            time0 = time.time()
            time.sleep(1)
            s, oldr, oldw = get_speed(oldr, oldw, time0)
            # print(s)
            s_Value.value = s
            # print(s_Value)
    except KeyboardInterrupt:
        pass


def main(sc):
    sc.nodelay(1)
    s_Value = Manager().Value(c_char_p, "compt...")
    p = Process(target=get_speed_main, args=(s_Value,))
    p.start()
    while True:
        s = str(s_Value.value)
        sc.addstr(0, 0, time.strftime(r"%Y-%m-%d %H:%M:%S")+"\n"+s)
        sc.addstr(os.get_terminal_size().lines-1, 0, "[按 `q` 退出程序]")
        sc.refresh()
        if sc.getch() == ord('q'):
            break
        time.sleep(0.07)
    p.kill()
    p.join()


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass


# [multiprocessing - How to share a string amongst multiple processes using Managers() in Python? - Stack Overflow](https://stackoverflow.com/questions/21290960/how-to-share-a-string-amongst-multiple-processes-using-managers-in-python)
# [教你在windows上用Python获得控制台大小(宽高)-百度经验](https://jingyan.baidu.com/article/c1a3101e659268de656deb1d.html)
