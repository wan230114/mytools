#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# @ Author: Chen Jun
# @ Author Email: 1170101471@qq.com
# @ Created Date: 2021-06-17, 00:00:15
# @ Modified By: Chen Jun
# @ Last Modified: 2021-08-11, 12:53:35
#############################################

import pandas as pd
import sys
import argparse


def fargv():
    parser = argparse.ArgumentParser(description='Process introduction.')
    parser.add_argument('inputfile', type=str, nargs="?",
                        help='输入需要运行的inputfile')
    parser.add_argument('-c', '--Cols', type=str, nargs="+", required=True,
                        help='需要挑选的行, 如"colname1 colname2 colname3')
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


def fmain(inputfile, Cols, sepInfile="\t", sepOutfile="\t",
          filter=None, sepfilter=",",
          outfile=None, Header=False):
    r"""
    inputfile = "./a.txt"
    Cols = ["A", "B"]
    sepInfile = "\t"
    sepOutfile = "\t"
    # filter = None
    filter = ["A,./filter.A"]
    sepfilter = ","
    outfile = None
    Header = False
    """
    df = pd_read_table_str(inputfile)
    filters = [x.split(sepfilter) for x in filter]
    # 筛选需要选择的列
    for Col, File in filters:
        df = df[df[Col].isin([line.strip("\r\n") for line in open(File) if line.strip()])]
    df = df[Cols]
    outfile = outfile if outfile else sys.stdout
    # print(outfile, bool(outfile))
    df.to_csv(outfile, index=False, sep=sepOutfile, header=Header)


def main():
    # sys.argv = ['', 'file', 'file2']
    kwargs = fargv()
    # print(kwargs)
    # print(*list(kwargs.keys()),sep=", ")
    fmain(**kwargs)


if __name__ == '__main__':
    main()
