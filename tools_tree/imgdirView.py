#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#############################################
# @ Author: Chen Jun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-22 16:32:01
# @Last Modified time: 2019-05-16 01:13:17
# @ Created Date: 2021-06-22, 17:53:19
# @ Modified By: Chen Jun
# @ Last Modified: 2021-06-29, 10:05:19
#############################################

#############################################
# TODO: [ ] 修复多级目录下输出文件路径定义问题
#############################################

import os
import sys
import argparse


def fargv():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='本程序用于生成html可视化文件夹中的png、pdf、svg文件')
    parser.add_argument('fidirs', type=str, default=[], nargs="+",
                        help='输入需要可视化的文件夹名，当前文件夹')
    parser.add_argument('houzui', type=str,
                        help='输入后缀名，末尾只能以png,pdf,svg结束，可以包含多个字符如 tre.png , option.tre.pdf , ')
    parser.add_argument('-n', '--name_out', type=str, default=None,
                        help='输出想要的html前缀名字')
    parser.add_argument('-f', '--filter', type=str, default=[], nargs='*',
                        help='增加想要的文件名，可依次增加多个条件，类似于grep -v用法')
    parser.add_argument('-v', '--remove', type=str, default=[], nargs='*',
                        help='排除不想要的文件名，可依次增加多个条件，类似于grep -v用法（此方法生效于-f之后）')
    parser.add_argument('-c', '--clean', action='store_true', default=False,
                        help='是否只生成html而不压缩')
    args = parser.parse_args()
    if args.houzui[-3:] not in ["png", "pdf", "svg"]:
        print('请检查输入文件后缀名')
        parser.parse_args(['', '--help'])
        sys.exit()
    print("--------------------------")
    print(f"输入参数是:\n1、输入文件夹: {args.fidirs}\n"
          f"2、过滤文件后缀名: {args.houzui}\n"
          f"3、筛选的文件名：{args.filter}\n"
          f"4、排除的文件名：{args.remove}")
    print("--------------------------\n")
    return args.__dict__


def fmain(fidirs, houzui, filter=[], remove=[], clean=False, name_out=None):
    softpath = os.path.split(os.path.realpath(__file__))[0]
    L = []
    for fidir in fidirs:
        if not os.path.isdir(fidir):
            print('%s 文件夹不存在' % fidir)
            sys.exit()
        dirname = fidir.rstrip(os.sep).split(os.sep)[-1]
        for p, d, f in os.walk(fidir):
            for ff in f:
                # L.append(os.path.join(p, ff))
                L.append(os.path.join(p, ff))
    L = sorted([x for x in L if x.endswith(houzui)])
    if filter:
        S = set()
        for x in L:
            for f in filter:
                if f in x:
                    S.add(x)
        L = sorted(S)
    if remove:
        S = set()
        for x in L:
            p = 0
            print(remove)
            for r in remove:
                # print(r not in x, r, x)
                if r in x:
                    p = 1
                    break
            if p == 0:
                S.add(x)
        L = sorted(S)
    print(*L, sep='\n')
    print('过滤到%s个文件' % len(L))
    Dfile = {'pdf': 'mod-pdf.html',
             'png': 'mod-png.html',
             'svg': 'mod-svg.html',
             }
    ourdir = os.path.dirname(fidir.rstrip(os.sep))
    outdir = ourdir if ourdir else "."
    dirname_out = "view" if dirname == "." else dirname
    foname = outdir + os.sep + (
        name_out if name_out else '%s-%s' % (dirname_out, houzui)) + ".html"
    with open(foname, 'w') as fo:
        with open(os.path.join(softpath, 'mod', Dfile[houzui.split('.')[-1]])) as fi:
            s=fi.read()
        fo.write(s % (str(L).strip('[]')))
    print('\nSuccess. write to: ' + foname)
    print('\nThank you for using imgdirView.py.')


def main():
    # sys.argv = ['', '1', 'pdf']
    # fidir, houzui = sys.argv[1:3]
    fmain(**fargv())


if __name__ == '__main__':
    main()
