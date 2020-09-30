#!/usr/bin/env python3

# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-03-01 14:30:22
# @Last Modified by:   JUN
# @Last Modified time: 2019-07-20 02:32:00


# 处理意外：当匹配的列有空值时如何处理


import sys
import collections
import argparse
import time


def fargv():
    '''输入文件注意事项：不能有表头'''
    parser = argparse.ArgumentParser(description='用于合并两个文件。')
    parser.add_argument('-f1', type=str, nargs=2,
                        help='参数1：file1；参数2：对应列数')
    parser.add_argument('-f2', type=str, nargs=2,
                        help='参数1：file2；参数2：对应列数')
    parser.add_argument('-fo', type=str,
                        help='输出文件的名字')
    parser.add_argument('--keep', action='store_true',
                        help='默认False，是否按照第一个文件的相应列顺序输出，'
                             '此模式下不合并相同行。与alone、showlost参数不能并存')
    parser.add_argument('--alone', action='store_true',
                        help='默认False，是否跳过相同键值，若是则只保留第一个出现的键值')
    parser.add_argument('--showlost', action='store_true',
                        help='默认False，是否输出第二个文件中未匹配到的键值')
    parser.add_argument('--include', action='store_true',
                        help='默认False，是否使用包含匹配模式，\
                        既当无法全等匹配时，采用包含模式去匹配（一个部分包含于另一个）')
    parser.add_argument('--sep', type=str, default=';',
                        help='定义相同键合并时使用的符号，默认为;')
    args = parser.parse_args()
    Largs = [args.f1, args.f2, args.fo, args.keep,
             args.alone, args.showlost, args.sep]
    if (None in Largs[1:3]) or (args.keep & args.alone) or (args.keep & args.showlost):
        parser.parse_args(['', '--help'])
        sys.exit()
    print('Welcome:\n您输入的参数为：', args)
    finame1, num1 = Largs[0]
    finame2, num2 = Largs[1]
    foname = Largs[2]
    return finame1, num1, \
        finame2, num2, \
        foname, \
        args.keep, \
        args.alone, \
        args.showlost, \
        args.sep, \
        args.include


def cleanL(L):
    if (len(L) == 2) and ('' in L):
        L.remove('')
    return L


def mergevalue(Lline1, Lline2):
    '''
    输入：Lline1=[[x1],[x2,x3]], Lline2
    输出：L'''
    L = []
    if len(Lline1) > len(Lline2):
        Lline2.extend([['']] * (len(Lline1) - len(Lline2)))
    elif len(Lline1) < len(Lline2):
        Lline1.extend([['']] * (len(Lline2) - len(Lline1)))
    for i, Lx in enumerate(Lline1):
        if Lline2[i][0] not in Lx:
            Lx.extend(Lline2[i])
        Lx = [x for x in Lx if x]
        L.append(Lx)
    return L


def dealfile(finame, nums, alone):
    D = collections.OrderedDict()
    Lnum = [(int(num) - 1) for num in nums.split(',')]
    Lp = []
    # 获取首行的列数
    # with open(finame) as fi:
    #     Lline = fi.readline().strip().split('\t')
    #     Ncol = len(Lline)
    t0 = time.time()
    print('[开始处理 %s]...' % finame)
    with open(finame) as fi:
        for Nrow, line in enumerate(fi):
            if '\t' in line:
                Lline = line.strip().split('\t')
            else:
                print(Nrow, "行无·")

                # Lline = [[x] for x in line.strip().split(' ')]
                # print('注意，该行无\\t，已用空格特殊处理')
                # print('-' * 30, line, Lline,
                #       tuple(Lline[num][0] for num in Lnum),
                #       len(Lline), '-' * 30, sep='\n')
            Lline = [[x] for x in Lline]
            # if len(Lline) != Ncol:
            #     print('WARNING: 第%s行：列数不一致，为%s' % (Nrow + 1, Ncol))
            #     Lp.append(len(Lline))
            try:
                key = tuple(Lline[num][0] for num in Lnum)
            except IndexError:
                print('WARNING,该行分割有问题')
                print('-' * 30, line, Lline,
                      # tuple(Lline[num][0] for num in Lnum),
                      len(Lline), '-' * 30, sep='\n')
                continue
            # for num in Lnum:
            # key = Lline[num][0]
            # Lline.remove(Lline[num])
            if key not in D:
                D[key] = Lline
            elif not alone:
                D[key] = mergevalue(D[key], Lline)
            else:
                print('WARNING: 发现key有重复，key: %s, 只保留第一个值' % key)
    print('[处理完毕 %s]...' % finame, '耗时%.3f秒' % (time.time() - t0))
    return D, Lp


def fmain(finame1, num1, finame2, num2, foname, keep, alone, showlost, sep, include):
    Llines = [[[x] for x in line.strip().split('\t')]
              for line in open(finame1)]
    # L1 = [[L[num1 - 1][0], L[0:num1 - 1] + L[num1:]] for L in Llines]
    L1 = [[L[int(num1) - 1][0], L] for L in Llines]
    Lp1 = []
    # if not keep:
    #     D1, Lp1 = dealfile(finame1, num1, alone)
    #     L1 = [[key, D1[key]] for key in D1]
    D2, Lp2 = dealfile(finame2, num2, alone)
    if Lp1:
        print('WARNIING: file1中有列数不正常，以下行:', Lp1)
    if Lp2:
        print('WARNIING: file2中有列数不正常，以下行:', Lp2)
    D_D2 = {}
    for x in D2:   # x == (xx1,xx2,xx3)
        for xx in x:  # xx
            if xx not in D_D2:
                D_D2[xx] = [x]
            elif x in D_D2[xx]:
                continue
            else:
                # print('----------------')
                # print(xx, x, D_D2[xx], x in D_D2[xx])
                D_D2[xx].append(x)
    # sys.exit()
    L_nomerge = []
    L_nomerge_list = []
    print('正在写入文件 -->')
    with open(foname, 'w') as fo:
        for key, Lline1 in L1:
            Lline1 = [sep.join(x) for x in Lline1]
            if key in D_D2:
                # print(Lline1)
                if len(D_D2[key]) > 1:
                    print('----------------------------------------------------')
                    print('WARNING, 键值有重复, 只取第一个值，键值:', key)
                    for tmp_key in D_D2[key]:
                        print(tmp_key, D2[tmp_key])
                    print('----------------------------------------------------')
                Lline2 = cleanL([sep.join(x) for x in D2[D_D2[key][0]]])
                fo.write('\t'.join([key] + Lline1 + Lline2) + '\n')
            else:
                p = 0  # 用于是否匹配到的指标
                if include:
                    for key_DD2 in D_D2:
                        if key_DD2 and key:
                            if key in key_DD2:
                                Lline2 = cleanL([sep.join(x)
                                                 for x in D2[D_D2[key_DD2][0]]])
                                fo.write(
                                    '\t'.join([key] + Lline1 + Lline2) + '\n')
                                print('WARNING: 键 %s 使用包含模式匹配, %s --> %s' %
                                      (key, key, key_DD2), )
                                p = 1
                                break
                            elif key_DD2 in key:
                                Lline2 = cleanL([sep.join(x)
                                                 for x in D2[D_D2[key_DD2][0]]])
                                fo.write(
                                    '\t'.join([key] + Lline1 + Lline2) + '\n')
                                print('WARNING: 键 %s 使用包含模式匹配, %s --> %s' %
                                      (key, key, key_DD2), )
                                p = 1
                                break
                if p == 0:
                    if keep or showlost:
                        fo.write('\t'.join([key] + Lline1) + '\n')
                    L_nomerge.append('\t'.join([key] + Lline1))
                    L_nomerge_list.append(key)
    print('替换完成 --> %s' % foname)
    if L_nomerge:
        print('匹配情况：%.4f%%(%s), 写入了 %s 个key, 剩余 %s 个未匹配到' % (
            (len(L1) - len(L_nomerge_list)) / len(L1) * 100,
            (len(L1) - len(L_nomerge_list)),
            '%s/%s' % ((len(L1) - len(L_nomerge_list)), len(L1)),
            len(L_nomerge_list)))
        # print('未写入文件 %s 的keys有: ' % foname, L_nomerge_list)
        with open(foname + '-nomerge', 'w') as fo:
            fo.write('\n'.join(L_nomerge))
        with open(foname + '-nomerge.keys', 'w') as fo:
            fo.write('\n'.join(L_nomerge_list))
        print('未写入的keys已输出到文件:  %s-nomerge  %s-nomerge.keys' % (foname, foname))


def main():
    # fmain(fargv())
    # sys.argv = ['', '-f1', 'file1', '1', '-f2', 'file2', '1', '-fo', 'file-merge.txt']
    finame1, num1, finame2, num2, foname, keep, alone, showlost, sep, include = fargv()
    fmain(finame1, num1, finame2, num2, foname,
          keep, alone, showlost, sep, include)


if __name__ == '__main__':
    main()
