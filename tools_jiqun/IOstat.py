#!/usr/bin/env python3
# -*- coding:utf-8 -*-

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
import psutil
import time
# print('Disk: ', psutil.disk_io_counters())
# print('Network: ', psutil.net_io_counters())
# psutil.disk_io_counters()
# psutil.disk_io_counters(perdisk=True)
# d = psutil.disk_io_counters(perdisk=True)
# for disk in d:
#     print(d[disk].write_bytes)


# %%
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


def disk_stat():
    d = psutil.disk_io_counters()
    # print("read_count:",
    #       "write_count:",
    #       "read_bytes:",
    #       "write_bytes:",
    #       "read_time:",
    #       "write_time:",
    #       "read_merged_count:",
    #       "write_merged_count:",
    #       "busy_time:",
    #       sep="\t")
    # print('Disk: ',
    #     d.read_count, getsize(d.read_count),
    #     d.write_count, getsize(d.write_count),
    #     d.read_bytes, getsize(d.read_bytes),
    #     d.write_bytes, getsize(d.write_bytes),
    #     d.read_time, getsize(d.read_time),
    #     d.write_time, getsize(d.write_time),
    #     d.read_merged_count, getsize(d.read_merged_count),
    #     d.write_merged_count, getsize(d.write_merged_count),
    #     d.busy_time, getsize(d.busy_time),
    # )
    return d



d = psutil.disk_io_counters(perdisk=True)

oldr, oldw = [], []
for disk in d:
    oldr.append(d[disk].read_bytes)
    oldw.append(d[disk].write_bytes)

while True:
    d = psutil.disk_io_counters(perdisk=True)
    newr, neww = [], []
    for disk in d:
        newr.append(d[disk].read_bytes)
        neww.append(d[disk].write_bytes)
    # print(d.keys(), oldr, newr, oldw, neww, sep="\n")
    for name, o, n, o2, n2 in zip(d.keys(), oldr, newr, oldw, neww):
        print(name, " r:", n-o, getsize(n-o), "/ s",
              " w:",  n2-o2, getsize(n2-o2), "/ s")
    print("\n")
    oldr, oldw = newr, neww
    time.sleep(1)
