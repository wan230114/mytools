#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# @ Author: Chen Jun
# @ Author Email: 1170101471@qq.com
# @ Created Date: 2021-08-27, 23:25:12
# @ Modified By: Chen Jun
# @ Last Modified: 2022-09-16, 02:06:58
#############################################

# 待修改

"""
psutil.disk_io_counters(perdisk=False, nowrap=True)
返回全系统磁盘 I/O 统计作为命名的 Tuple，包括以下字段：
bytes_sent: 发送的字节数
bytes_recv: 接收的字节数
packet_sent: 发送的数据包数
packet_recv: 接收到的数据包数
errin: 接收时的错误总数
errout: 发送时的错误总数
dropin: 丢弃的传入数据包总数
dropout: 丢弃的传出数据包总数（在 macOS 和 BSD 上始终为 0）
"""

# %%
from ctypes import c_char_p
from multiprocessing import Process, Manager
import os
import time
import curses
import psutil

# %%
global QUIT
QUIT  = 0
speed = 1


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
    d = psutil.net_io_counters(pernic=True)
    newr, neww = [], []
    for disk in d:
        newr.append(d[disk].bytes_recv)
        neww.append(d[disk].bytes_sent)
    # print(d.keys(), oldr, newr, oldw, neww, sep="\n")
    time1 = time.time()
    T = time1 - time0
    s = ["统计间隔时间：%.3fs\n" % T]
    L_res = []
    for name, o, n, o2, n2 in zip(d.keys(), oldr, newr, oldw, neww):
        sp1 = (n-o)/T
        sp2 = (n2-o2)/T
        s_new = ["%s" % name,
                 "  r: %-10s" % (getsize(sp1)+"/s"),
                 "  s: %-10s" % (getsize(sp2)+"/s"),
                 "\n"]
        L_res.append(s_new)
        # s += s_new
    max_len = max([len(x[0]) for x in L_res])
    for x in L_res:
        x[0] = ("%%%ds" % max_len) % x[0]
    s += [xx for x in L_res for xx in x]
    oldr, oldw = newr, neww
    return ''.join([str(x) for x in s]), oldr, oldw


def get_speed_main(s_Value):
    try:
        d = psutil.net_io_counters(pernic=True)
        oldr, oldw = [], []
        for disk in d:
            oldr.append(d[disk].bytes_sent)
            oldw.append(d[disk].bytes_sent)
        while True:
            time0 = time.time()
            time.sleep(speed)
            s, oldr, oldw = get_speed(oldr, oldw, time0)
            s_Value.value = s
            # print(s_Value)
    except KeyboardInterrupt:
        pass
    except Exception:
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
            QUIT = 1
            break
        time.sleep(0.07)
    p.kill()
    p.join()
    QUIT = 1



if __name__ == '__main__':
    # while not QUIT:
    os.system("clear")
    try:
        curses.wrapper(main)
        # input(QUIT)
    except KeyboardInterrupt:
        pass
    except Exception:
        pass


# [multiprocessing - How to share a string amongst multiple processes using Managers() in Python? - Stack Overflow](https://stackoverflow.com/questions/21290960/how-to-share-a-string-amongst-multiple-processes-using-managers-in-python)
# [教你在windows上用Python获得控制台大小(宽高)-百度经验](https://jingyan.baidu.com/article/c1a3101e659268de656deb1d.html)
