#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# @ Author: Chen Jun
# @ Author Email: 1170101471@qq.com
# @ Created Date: 2021-02-04, 09:17:54
# @ Modified By: Chen Jun
# @ Last Modified: 2021-02-05, 14:39:17
#############################################

"""
该程序用于看各个文件的行内容在各个文件中的存在情况
example: 
    ./compares.py res/*
    ./compares.py -i table
"""

# %%
import numpy as np
import pandas as pd
from os.path import splitext, basename
import sys
import argparse
from collections import OrderedDict


def fargv():
    parser = argparse.ArgumentParser(description='Process introduction.')
    if len(sys.argv) == 1:
        sys.argv.append("-h")
    parser.add_argument('infiles', type=str, nargs="*",
                        help='输入文件')
    parser.add_argument('-i', '--intable', type=str,
                        help='')
    parser.add_argument('-o', '--outname', type=str,
                        help='')
    args = parser.parse_args()
    return args.__dict__


def fmain(infiles, intable, outname):
    outname = outname if outname else "des.xls"
    L = sorted(np.unique(open(intable).read().split())) if intable else infiles

    res = {}
    for file in L:
        print(file)
        df = pd.read_table(
            file,
            names=[splitext(basename(file))[0]])
        d = df.to_dict()
        d_res = {x: d[x].values() for x in d}
        res.update(d_res)
    rows = set()
    for k in res:
        rows.update(res[k])

    L_rows = []
    L_res = []
    for row in rows:
        L_rows.append(row)
        d = {}
        for k in res:
            d[k] = 1 if row in res[k] else 0
        L_res.append(d)

    df = pd.DataFrame(L_res)
    df = pd.concat([pd.DataFrame(L_rows, columns=["ID"]),
                    df[sorted(df.columns)]], axis=1)
    df["Sum"] = df.iloc[:, 1:].sum(axis=1)
    df.sort_values(
        list(df.columns[-1:0:-1]),
        ascending=False, inplace=True)
    df.to_csv(outname, index=False, sep="\t")
    return df


if __name__ == '__main__':
    kwargs = fargv()
    fmain(**kwargs)
