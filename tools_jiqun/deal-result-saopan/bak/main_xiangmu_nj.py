#! /NJPROJ2/Plant/chenjun/software/python3.5/python3.5/bin/python3
# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-05-10 14:10:49
# @Last Modified by:   JUN
# @Last Modified time: 2019-05-13 15:13:52


import os
import sys
import re
import pandas as pd
import numpy as np
# from collections import OrderedDict


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


def getmenu(finame, Lall):
    '''用于获取目录'''
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


def fmain_00(fo1=None, fo2=None):
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


def fmain_01allsum(L_df, fo):
    fo2 = open('result-tongji.txt2', 'w')
    print('#欢迎使用集群磁盘统计工具。 本次结果中每个标题开头都为“###”, 可以直接搜索快速跳转查看', file=fo2)
    fo3 = open('result-tongji.txt3-split-all', 'w')
    print('#欢迎使用集群磁盘统计工具。 本次结果中每个标题开头都为“###”, 可以直接搜索快速跳转查看', file=fo3)
    for finame, df, D_xiangmu in L_df:
        print('\n### deal:', finame, file=fo)
        print('\n### deal:', finame, file=fo2)
        print('\n### deal:', finame, file=fo3)
        print('## 总大小: %s' % getsize(df.iloc[:, 1].sum()), file=fo)
        print('## 总大小: %s' % getsize(df.iloc[:, 1].sum()), file=fo2)
        print('## 总大小: %s' % getsize(df.iloc[:, 1].sum()), file=fo3)
        # for fo in [fo1, fo2]:
        # gp = df.groupby([0, 4, 5, 6, 7], sort=True)
    for finame, df, D_xiangmu in L_df:
        gp = df.groupby(['name', 'dir1'], sort=False)['size'].agg(
            [len, np.sum, getsizeL])
        print('\n\n### deal:', finame, file=fo)
        # print('\n\n### deal:', finame, file=fo3)
        print('\n##统计文件所属人总大小：', file=fo)
        # print('\n##统计文件所属人总大小：', file=fo3)
        print(gp.sort_values(['sum'], ascending=False).to_string(), file=fo)  # 排序打印
        # print(gp.sort_values(['sum'], ascending=False).to_string(), file=fo3)  # 排序打印


def fmain_02allfenji(L_df, fo):
    fo3 = open('result-tongji.txt3-split-all', 'a')
    fo2 = open('result-tongji.txt2', 'a')
    for finame, df, D_xiangmu in L_df:
        print('\n### deal:', finame, file=fo)
        D_sort = {}
        for col in ['dir%s' % x for x in range(1, 6)]:
            L = ['dir%s' % x for x in range(1, int(col[-1]) + 1)]
            print('\n###统计文件所属人各个分级文件大小：', file=fo)
            print('\n###统计文件所属人各个分级文件大小：', file=fo2)
            print('%s\n%s\n%s' % ('-' * 50, col, '-' * 50), file=fo)
            print('%s\n%s\n%s' % ('-' * 50, col, '-' * 50), file=fo2)
            gp = df.groupby(['name'] + L, sort=False)['size'].agg([len, np.sum, getsizeL])
            gp = gp.sort_values(['name'] + L[:-1] + ['sum'], ascending=True)
            # print(gp.to_string(), file=fo2)
            d_gp = gp.to_dict()
            L_tmp = []
            L_tmp2 = []
            if col == 'dir1':
                for T in d_gp['sum']:
                    D_sort[T[0]] = d_gp['sum'][T]  # 把第一个名字复制排序
            for T in d_gp['sum']:
                x_path = list(T)[1] + '/'.join(list(T)[2:])
                L_tmp.append([T[0], x_path, d_gp['len'][T],
                              d_gp['sum'][T], getsize(d_gp['sum'][T]),
                              D_sort[T[0]], getsize(D_sort[T[0]])])
                L_tmp2.append([T[0]] + list(list(T)[1:]) +
                              [d_gp['len'][T],
                               d_gp['sum'][T], getsize(d_gp['sum'][T]),
                               D_sort[T[0]], getsize(D_sort[T[0]])])
            df_tmp = pd.DataFrame(L_tmp)
            newnameL = ['#name', 'path', 'num', 'sum', 'sum2', 'sum_all', 'sum_all2']
            df_tmp.rename(columns=dict(enumerate(newnameL)), inplace=True)
            df_tmp = df_tmp.sort_values(by=['sum_all', 'sum', 'path'], ascending=False).reset_index(
                drop=True)
            print(df_tmp.to_string(), file=fo2)
            if col == 'dir2':
                print(df_tmp.to_string(), file=fo3)

            df_tmp = pd.DataFrame(L_tmp2)
            newdirL = ['dir%s' % x for x in range(1, len(list(T)[1:]) + 1)]
            newnameL = (['#name'] + newdirL +
                        ['num', 'sum', 'sum2', 'sum_all', 'sum_all2'])
            df_tmp.rename(columns=dict(enumerate(newnameL)), inplace=True)
            df_tmp = df_tmp.sort_values(
                by=['sum_all', 'sum'] + newdirL,
                ascending=False).reset_index(drop=True)
            print(df_tmp.groupby(['#name'] + newdirL +
                                 ['num', 'sum', 'sum2',
                                  'sum_all', 'sum_all2'], sort=False
                                 )['sum_all'].agg([np.sum]).to_string(), file=fo)
            # sys.exit()


def fmain_03xiangmu(L_df, fo):
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
        df_xiangmu = pd.DataFrame(
            L_xiangmu,
            columns=['##prjname', 'count', 'size(kb)', 'size(k/m/g/t)', 'INFO', 'PATH']
        )

        # #.drop_duplicates(['path'], keep='first', inplace=False)
        # print('###统计到的项目总大小', getsize(pd.concat(L_df, ignore_index=True)['size'].sum()),file=fo)
        print('##统计到的项目总大小:', getsize(df_xiangmu['size(kb)'].sum()), file=fo)
        print('##统计到的项目个数:', df_xiangmu['size(kb)'].count(), file=fo)
        print(df_xiangmu.sort_values(
            ['size(kb)'], ascending=False, ).reset_index(drop=True).to_string(), file=fo)

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
    with open('result-tongji.txt', 'w') as fo1, open('result-tongji.txt--xiangmu', 'w') as fo_xm:
        print('#欢迎使用集群磁盘统计工具。 本次结果中每个标题开头都为“###”, 可以直接搜索快速跳转查看', file=fo1)
        print('#欢迎使用集群磁盘统计工具。 本次结果中每个标题开头都为“###”, 可以直接搜索快速跳转查看', file=fo_xm)
        # fo1, fo2 = None, None

        print('fmain_00start...')
        L_df = fmain_00(fo1, fo_xm)

        print('fmain_01allsum...')
        fmain_01allsum(L_df, fo1)
        print('fmain_02allfenji...')
        fmain_02allfenji(L_df, fo1)
        print('fmain_03xiangmu...')
        fmain_03xiangmu(L_df, fo_xm)


def main():
    fmain()


if __name__ == '__main__':
    main()
