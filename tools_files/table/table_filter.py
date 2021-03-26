#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# @ Author: Chen Jun
# @ Author Email: 1170101471@qq.com
# @ Created Date: 2021-01-20, 10:17:44
# @ Modified By: Chen Jun
# @ Last Modified: 2021-03-25, 10:10:18
#############################################

# %%
import pandas as pd
import sys
import argparse
import os
# %%


def fargv():
    parser = argparse.ArgumentParser(description='Process introduction.')
    parser.add_argument('infile', type=str,
                        help='输入需要运行的infile')
    parser.add_argument('Cols', type=str,
                        help='cols，如"colname1,colname3,colname2')
    parser.add_argument('-sc', '--sepCols', type=str, default=",",
                        help='sepCols, Cols\'s sep, default: “,”')
    # parser.add_argument('-si', '--sepInfile', type=str, default="\t",
    #                     help='sepInfile, Infile\'s sep, default: “\\t”')
    parser.add_argument('-o', '--outfile', type=str,
                        help='outfile')
    parser.add_argument('-so', '--sepOutfile', type=str, default="\t",
                        help='sepOutfile, Outfile\'s sep, default: “\\t”')
    parser.add_argument('-H', '--Header', action="store_true",
                        help='Header, default: False')
    args = parser.parse_args()
    return args.__dict__


def do(infile, Cols, sepCols=",", outfile=None, Header=False, sepInfile=None, sepOutfile=None):
    # %%
    # infile = "./table_filter.py--test/a.txt"
    # Cols = "C,B,D"
    # sepCols = ","
    # # outfile = "./table_filter.py--test/a_filter.txt"
    # outfile = None
    # Header = False
    # sepInfile = "\t"
    # sepOutfile = "\t"

    # sepInfile = sepInfile if sepInfile else "\t"
    sepOutfile = sepOutfile if sepOutfile else "\t"
    if not outfile:
        from io import StringIO
        output = StringIO()
    # os.path.splitext(infile)[0] + "_filter" + os.path.splitext(infile)[1]
    read_mt = pd.read_table
    if os.path.splitext(infile)[-1] == ".csv":
        read_mt = pd.read_csv
    colnames = read_mt(infile, nrows=1).columns
    dtype = {x: "str" for x in colnames}
    df = read_mt(infile, dtype=dtype, keep_default_na=False)
    df[Cols.split(sepCols)].to_csv(
        output, sep=sepOutfile, index=False, header=Header
    )
    if not outfile:
        output.seek(0)
        sys.stdout.write(output.read())


# %%


def main():
    kwargs = fargv()
    # print(kwargs)
    # print(*list(kwargs.keys()),sep=", ")
    do(**kwargs)


if __name__ == '__main__':
    main()
