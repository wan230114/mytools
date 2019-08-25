#! /ifs/TJPROJ3/Plant/chenjun/software/Miniconda3/miniconda3/bin/python3
# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-05-10 14:10:49
# @Last Modified by:   JUN
# @Last Modified time: 2019-07-09 09:54:29


import os
import sys
import re
import pandas as pd
import numpy as np
from collections import OrderedDict


def getsize(size):
    D = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    for x in D:
        if size < 1024**(x + 1):
            hsize = str('%.3f' % (int(size) / 1024**x)) + D[x]
            return hsize


def getsizeL(args):
    size = sum(args)
    D = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    for x in D:
        if size < 1024**(x + 1):
            hsize = str('%.3f' % (int(size) / 1024**x)) + D[x]
            return hsize


def fgetsort(D):
    '''传入字典，返回字典生成的序号的函数'''
    def func(x):
        return D[x.values[0]]
    return func


def print_file(*args, sep=' ', end='\n', file=[]):
    for fo in file:
        args = [str(x) for x in args]
        fo.write(sep.join(args) + end)


def getmenu(finame, Lall):
    '''用于获取目录，过滤出项目信息'''
    if os.path.exists('/NJPROJ2/Plant/chenjun/Admin/'):
        path = {"NJPROJ1_10M": b"/NJPROJ1/PAG/Plant/",
                "NJPROJ2_10M": b"/NJPROJ2/Plant/",
                "NJPROJ3_10M": b"/NJPROJ3/Plant/"}[finame]
    else:
        path = {"TJNAS_Plant_10M": b"/TJNAS01/PAG/Plant/",
                "TJPROJ1_DENOVO_10M": b"/TJPROJ1/DENOVO/",
                "TJPROJ3_Plant_10M": b"/ifs/TJPROJ3/Plant/"}[finame]
    num_munu = 5  # 设置最多遍历几级目录
    # 设计数据结构 {dir*:{x:path,x:path,...},...}
    D_xiangmu = {'dir%s' % x: {} for x in range(1, num_munu + 1)}
    # D_path = {'dir%s' % x: {} for x in range(1, num_munu + 1)}
    for i, Lline in enumerate(Lall):
        Lline[0] = Lline[0].decode()  # 原文件有部分特殊字符，必须如此
        Lline[1] = int(Lline[1])  # int一下
        Lline_new = [None] * num_munu
        if path in Lline[2]:
            Lpath = Lline[2].replace(path, b'').split(b'/')
            p = 0
            for j, x in enumerate([path] + Lpath):
                pathdir = (path + b'/'.join(Lpath[:j])).decode()
                # if x not in D_xiangmu['dir%s' % (j + 1)]:
                # D_xiangmu['dir%s' % (j + 1)][x] = D_xiangmu['dir%s' % (j + 1)]
                if j < num_munu:
                    x = x.decode()
                    if re.findall('[PNRX].*?[12]\d{5}', x):
                        if not x.endswith('-V'):
                            if p == 1:
                                break
                                # print('项目名检测到子项目包含:',file=fo,
                                #       x, Lline[2])
                            D_xiangmu['dir%s' % (j + 1)][x] = pathdir
                            p = 1
                    Lline_new[j] = x
                else:
                    break
            Lall[i].extend(Lline_new)
    return D_xiangmu


def fmain_00():
    pd.set_option('display.max_colwidth', 200)  # 解决行显示不完全
    # pd.set_option('display.colheader_justify', 'left')
    L_df = []
    for finame in sorted(os.listdir('result')):
        # print('\n\n### deal:', finame, file=fo1)
        # print(open(os.path.join('result', finame), 'rb').readline(),file=fo)
        Lall = sorted([x.strip().split(b'\t')
                       for x in open(os.path.join('result', finame), 'rb')
                       if x.strip().split(b'\t')[1].isdigit()])
        D_xiangmu = getmenu(finame, Lall)
        # [print(x, '-->', D_xiangmu[x]) for x in D_xiangmu,file=fo]
        # sys.exit()
        df = pd.DataFrame(Lall)
        df.rename(columns=dict(
            zip([0, 1, 2, 3],
                ['name', 'size', 'file', 'date'])), inplace=True)
        df.rename(columns=dict(
            zip([4, 5, 6, 7, 8],
                ['dir%s' % x for x in range(1, 6)])), inplace=True)
        L_df.append([finame, df, D_xiangmu])
        # break
    return L_df


def fmain_01allsum(L_df):
    fo = open('result-tongji.txt', 'w')
    fo2_sortsize_path = open('result-tongji.txt2-sortsize-path', 'w')
    fo2_sortsize_dir = open('result-tongji.txt2-sortsize-dir', 'w')
    fo3_sortname = open('result-tongji.txt3-sortname', 'w')
    fo4_split_Big = open('result-tongji.txt4-split-Big', 'w')
    print_file('#欢迎使用集群磁盘统计工具。 本次结果中每个标题开头都为“###”, 可以直接搜索快速跳转查看\n',
               file=[fo, fo2_sortsize_path, fo2_sortsize_dir, fo3_sortname, fo4_split_Big])
    for finame, df, D_xiangmu in L_df:
        print_file('### deal:', finame,
                   file=[fo, fo2_sortsize_path, fo3_sortname, fo4_split_Big])
        print_file('## 总大小: %s' % getsize(df.iloc[:, 1].sum()),
                   file=[fo, fo2_sortsize_path, fo3_sortname, fo4_split_Big])
        # for fo in [fo1, fo2_sortsize_path]:
        # gp = df.groupby([0, 4, 5, 6, 7], sort=True)
    for finame, df, D_xiangmu in L_df:
        gp = df.groupby(['name', 'dir1'], sort=False)['size'].agg(
            [len, np.sum, getsizeL])
        print('\n### deal:', finame, file=fo)
        # print('\n\n### deal:', finame, file=fo4_split_Big)
        print('##统计文件所属人总大小：', file=fo)
        # print('\n##统计文件所属人总大小：', file=fo4_split_Big)
        print(gp.sort_values(['sum'], ascending=False).to_string(), file=fo)  # 排序打印
        # print(gp.sort_values(['sum'], ascending=False).to_string(), file=fo4_split_Big)  # 排序打印


def fmain_02allfenji(L_df):
    fo = open('result-tongji.txt', 'a')
    fo2_sortsize_path = open('result-tongji.txt2-sortsize-path', 'a')
    fo2_sortsize_dir = open('result-tongji.txt2-sortsize-dir', 'a')
    fo3_sortname = open('result-tongji.txt3-sortname', 'a')
    fo4_split_Big = open('result-tongji.txt4-split-Big', 'a')
    for finame, df, D_xiangmu in L_df:
        print('\n\n### deal:', finame, file=fo)
        D_sort = {}
        D_sort2 = {}
        D_dirsize = OrderedDict()
        for col in ['dir%s' % x for x in range(1, 6)]:
            L = ['dir%s' % x for x in range(1, int(col[-1]) + 1)]
            # path版
            gp = df.groupby(['name'] + L, sort=True)['size'].agg([len, np.sum, getsizeL])
            print('\n###统计文件所属人各个分级文件大小：\n%s\n%s\n%s\n' %
                  ('-' * 50, col, '-' * 50), gp.to_string(), file=fo3_sortname)
            d_gp = gp.to_dict()
            L_tmp = []
            # L_tmp2 = []
            if col == 'dir1':
                for T in d_gp['sum']:
                    D_sort[T[0]] = d_gp['sum'][T]  # 把第一个名字复制排序
                    D_sort2[T[0]] = getsize(d_gp['sum'][T])
                getsort = fgetsort(D_sort)
                getsort.__name__ = 'sum_all'
                getsort2 = fgetsort(D_sort2)
                getsort2.__name__ = 'sum_all2'
            D_dirsize[col] = {}  # {dir1:{():sum,():sum}, dir2:...}
            for T in d_gp['sum']:
                # print(T, d_gp['sum'][T])
                D_dirsize[col][T] = d_gp['sum'][T]
                # for i_T in range(len(T)):
                #     if T[:i_T] in D_dirsize:
                #         D_dirsize[T] =
                #     else:
                #         D_dirsize[T] = d_gp['sum'][T]
                x_path = list(T)[1] + '/'.join(list(T)[2:])
                L_tmp.append([T[0], x_path, d_gp['len'][T],
                              d_gp['sum'][T], getsize(d_gp['sum'][T]),
                              D_sort[T[0]], getsize(D_sort[T[0]])])
                # L_tmp2.append([T[0]] + list(list(T)[1:]) +
                #               [d_gp['len'][T],
                #                d_gp['sum'][T], getsize(d_gp['sum'][T]),
                #                D_sort[T[0]], getsize(D_sort[T[0]])])
            # print(D_dirsize)
            # sys.exit()
            newnameL = ['#name', 'path', 'num', 'sum', 'sum2', 'sum_all', 'sum_all2']
            df_tmp = pd.DataFrame(L_tmp)
            df_tmp.rename(columns=dict(enumerate(newnameL)), inplace=True)
            df_tmp = df_tmp.sort_values(by=['sum_all', 'sum', 'path'],
                                        ascending=False).reset_index(drop=True)
            gp_tmp = df_tmp.groupby(['#name', 'path', 'num'], sort=False,
                                    observed=True).agg({'sum': getsizeL, 'sum_all': getsizeL})
            print('\n###统计文件所属人各个分级文件大小：\n%s\n%s\n%s\n' %
                  ('-' * 50, col, '-' * 50), gp_tmp.to_string(), file=fo2_sortsize_path)
            # print(gp_tmp.to_string())
            # sys.exit()
            if col == 'dir2':
                print(df_tmp.to_string(), file=fo4_split_Big)

            # dir版
            # gp = df.groupby(['name'] + L, sort=True).agg(
            #     {'size': [len, np.sum, getsizeL],
            #      'name': [getsort, getsort2]})
            # print(gp.sort_values([('name', 'sum_all')] + L[:-1] + [('size', 'sum')],
            #                      ascending=False).to_string(), file=fo2_sortsize_path)

            # d_gp = gp.to_dict()
            # for T in d_gp:
            #     print(T,d_gp[T])
            # print(D_dirsize)
            # print(pd.DataFrame(gp).to_string())
            # print(gp.to_string(), file=fo2_sortsize_path)
            # [print(x) for x in gp.to_dict()]  # 啃爹的设计，竟然用函数名作为标题

            # 输出总目录
            # df_tmp = pd.DataFrame(L_tmp2)
            # newdirL = ['dir%s' % x for x in range(1, len(list(T)[1:]) + 1)]
            # newnameL = (['#name'] + newdirL +
            #             ['num', 'sum', 'sum2', 'sum_all', 'sum_all2'])
            # df_tmp.rename(columns=dict(enumerate(newnameL)), inplace=True)
            # # df_tmp = df_tmp.sort_values(
            # #     by=['sum_all'] + newdirL + ['sum'],
            # #     # by=['sum_all', 'sum'] + newdirL,
            # #     ascending=False).reset_index(drop=True)
            # gp_tmp = df_tmp.groupby(['#name'] + newdirL +
            #                         ['num', 'sum', 'sum2',
            #                          'sum_all', 'sum_all2'], sort=False
            #                         )['sum_all'].agg([getsizeL])
            # print(gp_tmp.to_dict())
            # print(gp_tmp.sort_value('sum_all').to_string())
            # sys.exit()
        # print()

        # 用于按大小排序的算法设计
        def sortL(La, Lb):
            L = []
            # print(La)
            # print(Lb)
            for size, T in La:
                Ltmp = []
                for size2, T2 in Lb:
                    # print('is? ', T2, T)
                    if T2[:-1] == T:
                        Ltmp.append([size2, T2])
                Ltmp = sorted(Ltmp, key=lambda x: -x[0])
                L.extend(Ltmp)
            return L

        def print_dir(Llines):
            df_tmp = pd.DataFrame(Llines)
            newnameL = ['name'] +\
                ['dir%s' % x for x in range(1, len(Llines[0]) - 2)] +\
                ['sum_last', 'sum']
            df_tmp.rename(columns=dict(enumerate(newnameL)), inplace=True)
            gp_tmp = df_tmp.groupby(newnameL[:-2], sort=False).agg(
                {'sum': getsizeL, 'sum_last': getsizeL, 'name': [getsort2]})
            print('\n###统计文件所属人各个分级文件大小：\n%s\n%s\n%s\n' %
                  ('-' * 50, col, '-' * 50), gp_tmp.to_string(), file=fo2_sortsize_dir)

        def print_path(Llines):
            Lp = [[Lline[0], Lline[1] + '/'.join(Lline[2:-2]),
                   Lline[-2], Lline[-1]] for Lline in Llines]
            # print(Lp)
            df_tmp = pd.DataFrame(Lp)
            newnameL = ['name', 'path', 'sum_last', 'sum']
            df_tmp.rename(columns=dict(enumerate(newnameL)), inplace=True)
            gp_tmp = df_tmp.groupby(newnameL[:-2], sort=False).agg(
                {'sum': getsizeL, 'sum_last': getsizeL, 'name': [getsort2]})
            print('\n###统计文件所属人各个分级文件大小：\n%s\n%s\n%s\n' %
                  ('-' * 50, col, '-' * 50), gp_tmp.to_string(), file=fo)

        Llines = []
        col = 'dir1'
        L1 = [[D_dirsize[col][T], T] for T in D_dirsize[col]]
        L1 = sorted(L1, key=lambda x: -x[0])
        # D['dir1'] = L1
        # print(L1)
        # print()
        # [print(T, size, getsize(size),  sep='\t') for size, T in L1]
        [Llines.append(list(T) + [D_dirsize['dir1'][T], size]) for size, T in L1]
        print_dir(Llines)
        print_path(Llines)
        Lold = L1
        for col in list(D_dirsize)[1:]:
            Llines = []
            L = [[D_dirsize[col][T], T] for T in D_dirsize[col]]
            L = sortL(Lold, L)
            # D['dir2'] = L
            # print()
            # [print(T, size, getsize(size),  sep='\t') for size, T in L]
            for size, T in L:
                Llines.append(list(T) + [D_dirsize['dir%s' % (int(col[-1]) - 1)][T[:-1]], size])
            print_dir(Llines)
            print_path(Llines)
            Lold = L
        # for col in D_dirsize:
        #     L = [[D_dirsize['dir1'][T], T] for T in D_dirsize['dir1']]
        #     D[col] = L


def fmain_03xiangmu(L_df):
    fo = open('result-tongji.txt5--xiangmu', 'w')
    print('#欢迎使用集群磁盘统计工具。 本次结果中每个标题开头都为“###”, 可以直接搜索快速跳转查看', file=fo)
    for finame, df, D_xiangmu in L_df:
        print('\n\n\n### deal:', finame, file=fo)
        print('##总大小: ', getsize(df.iloc[:, 1].sum()), file=fo)
        L_df = []
        L_xiangmu = []
        for col in range(1, 6):
            col_dir = 'dir%s' % col
            L = ['dir%s' % x for x in range(1, col + 1)]
            # 不排序加速计算
            gp = df.groupby(['name'] + L, sort=False).agg(
                {'size': [len, np.sum, getsizeL]})
            # print(col_dir, D_xiangmu[col_dir], file=fo)
            if D_xiangmu[col_dir]:
                for x_dir in D_xiangmu[col_dir]:
                    x_path = D_xiangmu[col_dir][x_dir]
                    df_tiqu = df[df[col_dir] == x_dir]
                    L_df.append(df_tiqu)
                    # print(df.to_string(),file=fo)
                    # print(df[col_dir],file=fo)
                    # print(col_dir, x_dir,file=fo)
                    # print(col_dir, df_tiqu.to_string(),file=fo)
                    x_size = df_tiqu['size'].sum()
                    x_count = df_tiqu['size'].count()
                    df_tongji = df_tiqu.groupby(['name'])['size'].agg([np.sum])
                    x_info = df_tongji.to_dict()['sum']
                    x_info_sorted = sorted(x_info.items(), key=lambda x: x[1], reverse=True)
                    x_info = ','.join(['%s:%s' % (name, getsize(x)) for name, x in x_info_sorted])
                    # x_info = re.sub('[\'{} ]', '', x_info)
                    # x_xinxi = ','.join(sorted(set(df_tiqu.to_dict()['name'].values())))
                    L_xiangmu.append([x_dir, x_count, x_size, getsize(x_size),
                                      '%s' % (x_info),
                                      x_path])
        newnameL = ['##prjname', 'count', 'size', 'size(k/m/g/t)', 'INFO', 'PATH']
        df_xiangmu = pd.DataFrame(
            L_xiangmu,
            columns=newnameL
        )

        # #.drop_duplicates(['path'], keep='first', inplace=False)
        # print('###统计到的项目总大小', getsize(pd.concat(L_df, ignore_index=True)['size'].sum()),file=fo)
        print('##统计到的项目总大小:', getsize(df_xiangmu['size'].sum()), file=fo)
        print('##统计到的项目个数:', df_xiangmu['size'].count(), file=fo)
        df_xiangmu = df_xiangmu.sort_values(['size'], ascending=False)
        gp_xiangmu = df_xiangmu.groupby(newnameL, sort=False).agg({"size": getsizeL})
        print(gp_xiangmu.to_string(), file=fo)
        # 遍历
        # for row in df.iteritems():
        #     print(row,file=fo)

        # print('3. 写入文件...',file=fo)
        # print(gp.to_string(),file=fo)
        # with open('info.txt', 'w') as fo:
        #     print(gp.to_string(),file=fo)

        # gp2 = gp[1].sum()
        # gp2 = gp.describe(include=[np.number])
        # gp2 = gp.describe().reset_index()
        # gp2.to_excel('out.xlsx', sheet_name='Sheet1')


def fmain():

    print('fmain_00start...')
    L_df = fmain_00()

    print('fmain_01allsum...')
    fmain_01allsum(L_df)
    print('fmain_02allfenji...')
    fmain_02allfenji(L_df)
    print('fmain_03xiangmu...')
    fmain_03xiangmu(L_df)


def main():
    fmain()


if __name__ == '__main__':
    main()
