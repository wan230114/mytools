# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-15 16:45:12
# @Last Modified by:   JUN
# @Last Modified time: 2019-01-16 22:03:14


# 目前卡点，核心代码未完成，需要读取下一个数刚好小于平均值得数

"""
最大同时投递100个job
使用work
target
blast_split_dir
blast_out_dir

步骤0：切分fasta，设置可选参数：需要的每个文件的序列数，默认为1
    实现1：
        200个文件为一个文件夹
    实现2：
        如果各条序列之间长度差异巨大，长短不一，则按照序列长度先排序，从首末尾分别开始取值，加到满序列数
        该方法有缺陷，不适用差异较小的情况。
方案2：
步骤0：不切分fasta，读取100个序列号，写入临时文件，投递运行，

步骤1：建立target的famot
步骤2：运行qsub_sge（自己写，可以避免ps进程列表中出现很多子程序，不便管理）
"""

import os
import sys
import re
import argparse

# 导入自定义模块
sys.path.append('/ifs/TJPROJ3/Plant/chenjun/mytools')
sys.path.append('/NJPROJ2/Plant/chenjun/mytools')
sys.path.append('E:\\我的云同步\\ALLdata\\mytools')
import tools
import fas

sys.argv = ['', 'fas.test.fa', '--num', '200']


class Split:

    def __init__(self):
        self.fargv()

    def fargv(self):
        parser = argparse.ArgumentParser(description='本程序用于均分切割fasta文件，使切割后的每个文件之间的碱基总数差异尽量小.')
        parser.add_argument('finame_fa', type=str,
                            help='输入需要切割的fasta文件')
        parser.add_argument('-o', '--outdir', type=str, default="./split_dir",
                            help='outdir 输出文件夹，默认')
        parser.add_argument('-n', '--num', type=int, default=100,
                            help='num 切割多少份跑')
        # if len(sys.argv) < 5:
        #     parser.parse_args(['', '--help'])
        #     sys.exit()
        args = parser.parse_args()
        self.Largs = [args.finame_fa, args.outdir, args.num]
        print("输入参数是:\n  文件: %s\n  切割输出的文件夹是: %s\n  切割的文件数是: %s\n\n" % tuple(self.Largs))

    def fmain(self):
        finame_fa, outdir, num = self.Largs
        self.func(finame_fa, outdir, num)

    def func(self, finame_fa, outdir, num):
        # 1) 获取长度列表
        OBJfas = fas.fas(['', finame_fa, '-lr'])
        L = OBJfas.fmain()
        print('\n\n')
        print(L)

        # 需要处理基因组重名问题

        # 2) 计算总数和平均数
        L_tmp = [x[1] for x in L]
        sum_L = sum(L_tmp)
        num_L = sum_L / num

        print('总值', sum_L)
        print('均值', num_L)

        Dall = {x: [] for x in range(1, num + 1)}
        Lnew = L.copy()
        i = 0
        while True:
            i += 1
            if i > len(Dall):
                break
            try:
                Dall[i].append(Lnew[0][0])
                oldLlen = Lnew[0]
            except IndexError:
                break
            if oldLlen[1] < num_L:
                Lsum = []
                print(Lnew)
                for idx, Ldata in enumerate(Lnew):
                    sumLtmp = oldLlen[1] + Ldata[1]
                    Lsum.append(sumLtmp)
                    if sumLtmp < num_L:
                        oldLlen = Ldata
                    if sumLtmp > num_L:
                        Dall[i].append(Lnew[0][0])
                        Lnew.pop(0)
                        print(Lnew)
                print(Lsum)
            Lnew.pop(0)

        print(Dall)


def main():
    obj = Split()
    obj.fmain()

if __name__ == '__main__':
    main()
