#!/usr/bin/env python3


"""
Install:

git clone https://github.com/LankyCyril/pyvenn.git
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
    args = parser.parse_args()
    return args


def main():
    args = fargv()
    if len(args.fipath) == 2:
        from compare2 import compare2 as comp
    elif len(args.fipath) == 3:
        from compare3 import compare3 as comp
    else:
        sys.argv = ["", "-h"]
        fargv()
    comp(*args.fipath)


if __name__ == "__main__":
    main()
