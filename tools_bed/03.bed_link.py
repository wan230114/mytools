# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-17 11:16:22
# @Last Modified by:   JUN
# @Last Modified time: 2019-01-17 19:28:15
"""
连接区间

输入：blast文件
输出：bed文件，blast第一列中比对上的区间汇总

例如：
    输入：
        第1行:chr01 ... 10  30  ...
        第2行:chr01 ... 26  55  ...
    输出
        chr01 10  55

步骤：
    01) 合并重叠区间
    02) 还原比对后的真实区间
    03) 将该基因写入文件
"""
import sys
import time


def merge(intervals):
    """
    :type intervals: List[Interval]
    :rtype: List[Interval]
    """
    if len(intervals) <= 1:
        return intervals
    res = []
    intervals = sorted(intervals, key=lambda start: start[0])
    l = intervals[0][0]
    h = intervals[0][1]
    for i in range(1, len(intervals)):
        if intervals[i][0] <= h:
            h = max(h, intervals[i][1])
        else:
            res.append([l, h])
            l = intervals[i][0]
            h = intervals[i][1]
    res.append([l, h])
    return res


def func(finame, foname):
    t00 = time.time()
    fi = open(finame, 'rb')
    fo = open(foname, 'w')

    print('running...')
    t0 = time.time()
    line = fi.readline()
    Lline = line.strip().split(b'\t')
    name = Lline[0].decode()
    Ltmp = [[int(Lline[6]), int(Lline[7])]]

    def do():
        # 进行区间合并
        print('start merge at:', name)
        # print(Ltmp)
        Ltmpmerge = merge(Ltmp)
        print(Ltmpmerge)
        Lx = name.split('_')
        # print(Lx)
        genename = '_'.join(Lx[:-2])
        for Ldata in Ltmpmerge:
            BEGIN = Ldata[0] + int(Lx[-2]) - 1
            END = Ldata[1] + int(Lx[-2]) - 1
            Lline = [genename, BEGIN, END]
            if END < Ldata[1]:
                print('发现错误', Ldata, Lline)
            fo.write('%s\t%s\t%s\n' % (Lline[0], Lline[1], Lline[2]))
        return [], new_name

    while True:
        line = fi.readline()
        if not line:
            break
        Lline = line.strip().split(b'\t')
        new_name = Lline[0].decode()
        if new_name == name:
            Ltmp.append([int(Lline[6]), int(Lline[7])])
        else:
            Ltmp, name = do()
            Ltmp.append([int(Lline[6]), int(Lline[7])])
    Ltmp, name = do()
    print('run-over. used time %s s' % (time.time() - t00))


def main():
    if len(sys.argv) == 1:
        sys.argv = ['', 'test.bed', 'test.new.bed']
    finame, foname = sys.argv[1:3]
    func(finame, foname)


if __name__ == '__main__':
    main()
