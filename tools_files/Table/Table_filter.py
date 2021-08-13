#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# @ Author: Chen Jun
# @ Author Email: 1170101471@qq.com
# @ Created Date: 2021-06-17, 00:00:15
# @ Modified By: Chen Jun
# @ Last Modified: 2021-08-13, 16:01:01
#############################################

import pandas as pd
import sys
import argparse


def fargv():
    parser = argparse.ArgumentParser(description='Process introduction.')
    parser.add_argument('inputfile', type=str, nargs="?",
                        help='输入需要运行的inputfile')
    parser.add_argument('-c', '--Cols', type=str, nargs="+", default=[],
                        help='需要挑选的列, 如"colname1 colname2 colname3')
    parser.add_argument('-cn', '--ColsNums', type=str, default="",
                        help='需要挑选的列, 如"1,3,4-6,8')
    parser.add_argument('-si', '--sepInfile', type=str, default="\t",
                        help='输入的文件的分隔符, default: “\\t”')
    parser.add_argument('-o', '--outfile', type=str, default=None,
                        help='outfile, 输出文件路径。 默认输出到标准输出')
    parser.add_argument('-so', '--sepOutfile', type=str, default="\t",
                        help='输出的文件的分隔符, 默认 “\\t”')
    parser.add_argument('-f', '--filter', type=str, nargs="+", default=[],
                        help='挑选某一列，格式为 col,file，如"colname1,file1 colname2,file2 colname3,file3')
    parser.add_argument('-sf', '--sepfilter', type=str, default=",",
                        help='filter参数的每个值中间的分隔符, 默认 “,”')
    parser.add_argument('-H', '--Header', action="store_true",
                        help='Header, 输出的文件是否打印Header。 默认 False')
    args = parser.parse_args()
    return args.__dict__


# %%


def pd_read_table_str(infile, dtype={}, **kwargs):
    # ! 二次读取的解决方案：先读第一行，将所有列指定为str，根据需求手动改类型，二次读取。
    colnames = pd.read_table(
        infile, nrows=1, keep_default_na=False, **kwargs).columns
    dtypes = {x: "str" for x in colnames}
    dtypes.update(dtype)
    # dtype.update({"c1": "int"})  # 根据需要更改
    df = pd.read_table(infile, dtype=dtypes, keep_default_na=False, **kwargs)
    # 如需将NA也识别为字符串，需指定参数，keep_default_na=False
    return df
# %%


def fmain(inputfile, Cols=[], ColsNums="", sepInfile="\t", sepOutfile="\t",
          filter=None, sepfilter=",",
          outfile=None, Header=False):
    # %%
    r"""
    inputfile = "./a.txt"
    Cols = ["A", "B"]
    ColsNums = "1,2-3"
    sepInfile = "\t"
    sepOutfile = "\t"
    # filter = None
    filter = ["A,./filter.A"]
    sepfilter = ","
    outfile = None
    Header = False
    """
    L_ColsNums = []
    if ColsNums:
        for x in ColsNums.split(","):
            if "-" in x:
                a, b = x.split("-")
                L_ColsNums.extend(range(int(a), int(b)+1))
            else:
                L_ColsNums.append(int(x))
        L_ColsNums = [x-1 for x in L_ColsNums if x-1 > 0]
    df = pd_read_table_str(inputfile, sep=sepInfile)
    filters = [x.split(sepfilter) for x in filter]
    # 筛选列数据
    for Col, File in filters:
        df = df[df[Col].isin([line.strip("\r\n")
                              for line in open(File) if line.strip()])]
    # 筛选需要选择的列
    if L_ColsNums:
        Cols2 = list(df.columns[L_ColsNums])
        Cols2.extend(list(df.columns[df.columns.isin(Cols)]))
        Cols = list(df.columns[df.columns.isin(Cols2)])
    df = df[Cols] if Cols else df
    outfile = outfile if outfile else sys.stdout
    # print(outfile, bool(outfile))
    df.to_csv(outfile, index=False, sep=sepOutfile, header=Header)
# %%


def main():
    # sys.argv = ['', 'file', 'file2']
    kwargs = fargv()
    # print(kwargs)
    # print(*list(kwargs.keys()),sep=", ")
    fmain(**kwargs)


if __name__ == '__main__':
    main()
