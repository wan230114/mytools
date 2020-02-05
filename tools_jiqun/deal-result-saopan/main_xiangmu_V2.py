#! /root/miniconda3/bin/python
# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-05-10 14:10:49
# @Last Modified by:   JUN
# @Last Modified time: 2019-07-11 18:00:18


import os
import sys
import re
import pandas as pd
import numpy as np
from collections import OrderedDict
from pprint import pprint
import argparse

pd.set_option('display.max_colwidth', 200)  # 解决行显示不完全


def fargv():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=('统计扫盘结果的文件夹大小'),
        epilog=('注意事项：\n'
                '    None\n'
                ))
    parser.add_argument('-i', '--infile', type=str, required=True,
                        help=('输入文件'))
    parser.add_argument('-s', '--splitdir', type=str, required=True,
                        help=('输入需要统计的目录，默认为根目录"/"开始'))
    parser.add_argument('-n', '--num_menu', type=int, default=5,
                        help=('输入需要统计的目录的层级数，默认为5'))
    parser.add_argument('-o', '--outfile', type=str, default=None,
                        help=('输出文件, 默认为: 原始文件名 + “--tongji.xls”, '
                              '如：“result/TJNAS_Plant_10M” 的统计结果文件， 命名为：'
                              '“TJNAS_Plant_10M--tongji.xls”'
                              ))
    args = parser.parse_args()
    if not args.__dict__['outfile']:
        args.__dict__['outfile'] = (
            args.__dict__['infile'].split(os.sep)[-1] + '--tongji.xls')
    return args.__dict__


class tongji(object):
    def __init__(self, infile, splitdir, outfile, num_menu):
        self.infile = infile
        self.splitdir = splitdir
        self.outfile = outfile
        self.num_menu = num_menu
        # 程序内需要使用的
        self.__Lall__ = []
        self.__Ldf__ = []  # 存储总L

    def get_info_from_file(self):
        """从文件中获取格式化好后的数据df"""
        # zhaojing	2561320906	/TJNAS01/PAG/Plant/zhaojing/400_ra...fastq.gz	2018-09-04
        self.__Lall__ = sorted([x.strip().split(b'\t') for x in open(self.infile, 'rb')
                                if x.strip().split(b'\t')[1].isdigit()])
        df = pd.DataFrame(self.__Lall__)
        df.rename(columns=dict(
            zip([0, 1, 2, 3],
                ['name', 'size', 'file', 'date'])), inplace=True)
        df.rename(columns=dict(
            zip(range(4, 4+self.num_menu),
                ['dir%s' % x for x in range(1, self.num_menu+1)])), inplace=True)
        self.__Ldf__.append([self.infile, df])

    def xiangmu_tongji(self):
        # -----项目统计-----
        # 设计数据结构 {dir*:{x:path,x:path,...},...}
        path = self.splitdir.encode()
        D_xiangmu = {'dir%s' % x: {} for x in range(1, self.num_menu + 1)}
        for i, Lline in enumerate(self.__Lall__):
            Lline[0] = Lline[0].decode('utf8')  # 原文件有部分特殊字符，必须如此
            Lline[1] = int(Lline[1])  # int一下
            Lline_new = [None] * self.num_menu
            if Lline[2].startswith(b'"'):
                Lline[2] = Lline[2].strip(b'"')
            if Lline[2].startswith(path):
                Lpath = Lline[2].replace(path, b'').split(b'/')
                p = 0
                for j, x in enumerate([path] + Lpath):
                    pathdir = (path + b'/'.join(Lpath[:j])).decode()
                    if j < self.num_menu:
                        x = x.decode()
                        if re.findall('[PNRX].*?[12]\d{5}', x):
                            if not x.endswith('-V'):
                                if p == 1:
                                    break
                                D_xiangmu['dir%s' % (j + 1)][x] = pathdir
                                p = 1
                        Lline_new[j] = x
                    else:
                        break
                self.__Lall__[i].extend(Lline_new)
            else:
                print('Warning, path not in. path:', Lline[2])
        return D_xiangmu


if __name__ == "__main__":
    # sys.argv[1:] = ' -h'.split()
    sys.argv[1:] = ' -i result/TJNAS_Plant_10M -s /TJNAS01/PAG/Plant/'.split()
    D = fargv()
    p = tongji(**D)
    p.get_info_from_file()
    # print(p.xiangmu_tongji())
