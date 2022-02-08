#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun2049@foxmail.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-09-10 10:42:35
# @Last Modified by:   JUN
# @Last Modified time: 2019-09-10 12:08:50

import sys
import argparse
import time


def fargv():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=('用自定义的替换列表, 替换原文件中某一列的旧名字为新名字（并输出未替换成功的行信息）'),
        epilog=('注意事项: \n    None'
                ))
    parser.add_argument('-l', '--listfile', type=str, required=True,
                        help=('对应替换列表文件, 按第一个分隔符分割为键值两部分，用于后续替换'))
    parser.add_argument('-i', '--oldfile', type=str, required=True,
                        help=('需要替换的文件'))
    parser.add_argument('-n', '--num', type=str, required=True,
                        help=('需要替换的文件的列, 每一行每一列都替换输入为: “all”, 如“all”。'
                              '某些列替换则输入: “n个数字之间使用英文逗号分隔”, 如“1,2,3”。'))
    parser.add_argument('-o', '--outfile', type=str, default=None,
                        help=('需要替换的文件, 默认为输入文件末尾加.new'))
    parser.add_argument('-s1', '--sep1', type=str, default="\t",
                        help=('指定输入的list文件的分隔符, 默认为\\t'))
    parser.add_argument('-s2', '--sep2', type=str, default="\t",
                        help=('指定输入的待替换文件的分隔符, 默认为\\t'))
    args = parser.parse_args()
    try:
        if args.num != 'all':
            [int(x) for x in args.num.split(',')]
    except ValueError:
        print('请检查输入的num是否正确,格式为: 数字1,数字2,数字3,...')
        sys.exit(1)
    return args.__dict__


def fmain(listfile, oldfile, num, outfile, sep1, sep2):
    list_name, old_name, new_name = listfile, oldfile, outfile
    if not outfile:
        new_name = oldfile + '.new'

    t0 = time.time()
    print("( start at time %s )" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    print("列表文件: %s" % list_name)
    print("输入文件: %s" % old_name)
    print("输出文件: %s" % new_name)

    if num == 'all':
        Lnum = []
    else:
        Lnum = [int(x) - 1 for x in num.split(',')]

    # 1）处理list, 生成字典
    print('>>> 建立索引中...')
    Dlist = {}
    with open(list_name, 'r') as fi_list:
        for line in fi_list:
            Lline = line.strip().split(sep1, 1)
            try:
                Dlist[Lline[0]] = Lline[1]
            except IndexError:
                s = '输入的list在一行中无法分割, 请检查list文件\n'
                s += '该行是:\n' + line
                raise IndexError(s)
        print('>>> 已建立索引, 即将开始替换...')

    # 2）替换文件
    key = ''
    n_line = 0
    n_all = 0
    n_ok = 0
    s_WARNING = ''
    n_eer = 0
    fi = open(old_name, 'r')
    if new_name != old_name:
        fo = open(new_name, 'w')
    else:
        L_res = []
    for line in fi:
        n_line += 1
        Lline = line.rstrip().split(sep2)
        if not Lnum:
            Lnum = list(range(len(Lline)))
        for Num in Lnum:
            try:
                n_all += 1
                key = Lline[Num]
                keyValue = Dlist[key]
                Lline[Num] = key.replace(key, keyValue)
                n_ok += 1
                oldkey = key
            except KeyError:
                n_eer += 1
                s_WARNING += 'WARNING %s: 跳过第 %s 行替换, 列表文件中键对应值 %s 不存在\n' % (n_eer, n_line, key)
        tmp = sep2.join(Lline) + '\n'
        if new_name != old_name:
            fo.write(tmp)
        else:
            L_res.append(tmp)
    if new_name != old_name:
        fi.close()
        fo.close()
    else:
        with open(new_name, 'w') as fo:
            for line in L_res:
                fo.write(line)
    if s_WARNING:
        print('----------------------\n%s----------------------' % s_WARNING)
    try:
        print('>>> 替换完毕! 最后一次替换是将"%s"替换为"%s"\n进行了%d次替换(%s/%s[%.2f%%]), 请查看新文件: %s' %
              (oldkey, Dlist[oldkey], n_ok, n_ok, n_all, (n_ok / n_all * 100), new_name))
    except KeyError:
        print('Error :替换失败！请检查list列表文件与待替换列是否有对应关系')
        sys.exit()
    print("运行结束, 耗时%s秒" % (time.time() - t0))
    print("( Finish at time %s )\n" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))


def main():
    # sys.argv = '1 -l listfile -i file -n 1,2'.split()
    args = fargv()
    # print(*list(args.keys()), sep=", ")
    fmain(**args)


if __name__ == '__main__':
    main()
