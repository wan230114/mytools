#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# @ Author: Chen Jun
# @ Author Email: 1170101471@qq.com
# @ Created Date: 2021-01-20, 10:17:44
# @ Modified By: Chen Jun
# @ Last Modified: 2021-01-20, 11:12:47
#############################################

# %%
import pandas as pd
import sys
import argparse


def fargv():
    parser = argparse.ArgumentParser(description='Process introduction.')
    parser.add_argument('infile', type=str,
                        help='输入需要运行的infile')
    parser.add_argument('cols', type=str,
                        help='cols，如"colname1,colname3,colname2')
    parser.add_argument('-o', '--outfile', type=str,
                        help='outfile')
    parser.add_argument('-sc', '--sepCols', type=str, default=",",
                        help='sepCols, defaultz: “,”')
    parser.add_argument('-so', '--sepOutfile', type=str, default="\t",
                        help='sepOutfile, defaultz: “\\t”')
    args = parser.parse_args()
    return args.__dict__


def do(infile, cols, outfile=None, sepCols=None, sepOutfile=None):
    # infile = "./table_tiqu.py--test/a.txt"
    # cols = "C,B,D"
    sepCols = sepCols if sepCols else ","
    sepOutfile = sepOutfile if sepOutfile else "\t"

    outfile = outfile if outfile else sys.stdout
    # os.path.splitext(infile)[0] + "_filter" + os.path.splitext(infile)[1]

    pd.read_table(infile)[cols.split(sepCols)].to_csv(
        outfile, sep=sepOutfile, index=False
    )


def main():
    kwargs = fargv()
    # print(kwargs)
    # print(*list(kwargs.keys()),sep=", ")
    do(**kwargs)


if __name__ == '__main__':
    main()
