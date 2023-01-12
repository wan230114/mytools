#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# @ Author: Chen Jun
# @ Author Email: 1170101471@qq.com
# @ Created Date: 2022-11-05, 15:51:46
# @ Modified By: Chen Jun
# @ Last Modified: 2023-01-13, 01:31:21
#############################################

# %%
import os
import argparse
import glob

# %%


def get_directory_size(directory):
    """Returns the `directory` size in bytes."""
    total = 0
    try:
        # print("[+] Getting the size of", directory)
        for entry in os.scandir(directory):
            if "./pipeline-framework-learning/nextflow/demo1/work/6b/5e053f613a047bb06dd279bc38e3f2/1week-input-2_1.fq.gz" == entry.path:
                print(entry.path)
            if entry.is_symlink():
                pass
            elif entry.is_file():
                # if it's a file, use stat() function
                # total += entry.stat().st_size
                total += os.lstat(entry.path).st_size
            elif entry.is_dir():
                # if it's a directory, recursively call this function
                try:
                    total += get_directory_size(entry.path)
                except FileNotFoundError:
                    pass
    except FileNotFoundError:
        # if `directory` isn't find, return 0
        return 0
    except NotADirectoryError:
        # if `directory` isn't a directory, get the file size then
        return os.path.getsize(directory)
    except PermissionError:
        # if for whatever reason we can't open the folder, return 0
        return 0
    return total


def getSize(inputPaths, m1=False, m2=False, sortNames=False):
    # %%
    path_all = []
    if inputPaths:
        path_all = [path for paths in inputPaths for path in glob.glob(paths)]
    else:
        path_all = glob.glob('./*')
    path_all
    # %%
    if m1:
        paths_str = ' '.join(map(lambda x: '"'+x+'"', path_all))
        if sortNames:
            os.system(
                """du -bs %s|sort -k1 |awk 'BEGIN{sum=0}{sum+=$1;print $0}END{print "-----------";print sum}'""" % paths_str)
        else:
            os.system(
                """du -bs %s|sort -k1n|awk 'BEGIN{sum=0}{sum+=$1;print $0}END{print "-----------";print sum}'""" % paths_str)
    else:
        L = []
        for path in path_all:
            L.append([get_directory_size(path), path])

        for x in sorted(L, key=lambda x: x[0]):
            print(*x, sep="\t")
        print("-----------")
        print(sum([x[0] for x in L]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        # formatter_class=argparse.RawDescriptionHelpFormatter,
        formatter_class=argparse.RawTextHelpFormatter,
        description=('路径大小获取'),)
    parser.add_argument('inputPaths', type=str, nargs="*", default=None,
                        help=('输入路径'))
    parser.add_argument('-n', "--sortNames", action='store_true',
                        help='按文件名排序，否则按大小排序')
    # 参数组，只能选择其中一个
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-m1', action='store_true',
                       help=('模式1，默认 du -bs 方式获得文件大小'))
    group.add_argument('-m2', action='store_true',
                       help=('模式2，使用Python内计算获得大小'))
    args = parser.parse_args()
    # print(args)
    inputPaths = args.inputPaths
    getSize(inputPaths, m1=args.m1, m2=args.m2, sortNames=args.sortNames)

# %%
