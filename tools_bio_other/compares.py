#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# @ Author: Chen Jun
# @ Author Email: 1170101471@qq.com
# @ Created Date: 2021-02-04, 09:17:54
# @ Modified By: Chen Jun
# @ Last Modified: 2021-03-08, 22:54:39
#############################################

"""
该程序用于看各个文件的行内容在各个文件中的存在情况
example: 
    ./compares.py res/*
    ./compares.py -i table
"""

# %%
import sys
import argparse


def fargv():
    parser = argparse.ArgumentParser(description='Process introduction.')
    if len(sys.argv) == 1:
        sys.argv.append("-h")
    parser.add_argument('infiles', type=str, nargs="*", default=None,
                        help='输入文件')
    parser.add_argument('-i', '--intable', type=str, default=None,
                        help='输入文件的文件列表')
    parser.add_argument('-o', '--outname', type=str,
                        help='输出文件')
    parser.add_argument('-s', '--sort_cols', action='store_true',
                        help='按结果列进行三角sort')
    args = parser.parse_args()
    return args.__dict__


def fmain(infiles, intable, outname, sort_cols=False):
    # import numpy as np
    import pandas as pd
    from os.path import splitext, basename
    from collections import OrderedDict
    assert infiles or intable, "未输入对比文件"
    outname = outname if outname else "des.xls"
    L = open(intable).read().split() if intable else infiles
    print(*L)

    res = OrderedDict()
    for file in L:
        df = pd.read_table(
            file,
            names=[splitext(basename(file))[0]])
        d = df.to_dict()
        d_res = {x: d[x].values() for x in d}
        res.update(d_res)
    rows = OrderedDict()
    for k in res:
        rows.update(OrderedDict(zip(res[k], [0]*len(res[k]))))

    L_rows = []
    L_res = []
    for row in rows:
        L_rows.append(row)
        d = OrderedDict()
        for k in res:
            d[k] = 1 if row in res[k] else 0
        L_res.append(d)

    df = pd.DataFrame(L_res, index=L_rows)
    # print(df)
    # df = pd.concat([pd.DataFrame(L_rows, columns=["ID"]),
    #                 df], axis=1)
    df["Sum"] = df.sum(axis=1)
    cols = list([df.columns[-1]])+list(df.columns[0:-1]) if sort_cols else list([df.columns[-1]])
    df.sort_values(
        cols,
        ascending=False, inplace=True)
    df.to_csv(outname, index_label="ID", sep="\t")
    return df


if __name__ == '__main__':
    kwargs = fargv()
    fmain(**kwargs)
