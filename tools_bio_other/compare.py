#!/usr/bin/env python3


"""
Install bash:

# focks by: https://github.com/LankyCyril/pyvenn.git
git clone https://github.com/wan230114/pyvenn.git
cd pyvenn
python setup.py install

pip install matplotlib
# pip install matplotlib_venn
"""

# %%
import sys
import os
from matplotlib import pyplot as plt
from venn import venn
# from matplotlib_venn import venn2
import argparse


def fargv():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='venn图工具，输入2-3个文件对比')
    parser.add_argument('fipath', type=str, default=[], nargs="+",
                        help='输入对比的文件路径')
    parser.add_argument('-o', '--outdir', type=str, default=None,
                        help='输入对比的文件路径')
    args = parser.parse_args()
    return args


def comp(*args, outdir=None):
    datas = {}
    for fi_name in args:
        print(f"reading: {fi_name}")
        out = os.path.splitext(os.path.basename(fi_name))[0]
        with open(fi_name) as fi:
            s = {x.strip().strip('"') for x in fi.readlines()}
            datas[out] = s

    Outname = outdir if outdir else '--VS--'.join(datas)
    print(f"result to: {Outname}")
    venn(datas,
         fmt="{percentage:.1f}%\n({size})",
         figsize=(9, 9),
         outdir=Outname,
         #   alpha=.5,
         #  cmap=["r", "g", "b"]
         #  cmap="Accent"
         #  cmap="Set2"  # 蓝 绿 紫
         #  cmap="Set3"  # 蓝 绿 黄
         #  cmap=list("rgy")  # 红 绿 黄
         #  cmap=list("rgb")  # 红 绿 黄
         )


def main():
    args = fargv()
    if len(args.fipath) > 6:
        sys.argv = ["", "-h"]
        fargv()
    print("args:", args)
    comp(*args.fipath, outdir=args.outdir)


if __name__ == "__main__":
    main()
