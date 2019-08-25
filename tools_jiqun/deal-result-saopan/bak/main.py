# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-05-10 14:10:49
# @Last Modified by:   JUN
# @Last Modified time: 2019-05-12 21:50:47


import os
import sys
import pandas
import numpy


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
    path = {"TJNAS_Plant_10M": b"/TJNAS01/PAG/Plant/",
            "TJPROJ1_DENOVO_10M": b"/TJPROJ1/DENOVO/",
            "TJPROJ3_Plant_10M": b"/ifs/TJPROJ3/Plant/"}[finame]
    for i, Lline in enumerate(Lall):
        Lline[0] = Lline[0].decode()  # 原文件有部分特殊字符，必须如此
        Lline[1] = int(Lline[1])  # int一下
        num_munu = 5  # 设置最多遍历几级目录
        Lline_new = [None] * num_munu
        for j, x in enumerate([path] + Lline[2].replace(path, b'').split(b'/')):
            if j < num_munu:
                Lline_new[j] = x.decode()
            else:
                break
        Lall[i].extend(Lline_new)


def fmain_00(finame, mod=0):
    # print(open(os.path.join('result', finame), 'rb').readline())
    Lall = sorted([x.strip().split(b'\t')
                   for x in open(os.path.join('result', finame), 'rb')
                   if x.strip().split(b'\t')[1].isdigit()])
    getmenu(finame, Lall)
    df = pandas.DataFrame(Lall)
    df.rename(columns=dict(zip([0, 1, 2, 3], ['name', 'size', 'file', 'date'])), inplace=True)
    df.rename(columns=dict(zip([4, 5, 6, 7, 8], ['dir%s' % x for x in range(1, 6)])), inplace=True)
    # print(df.to_string())
    print('##总大小: ', getsize(df.iloc[:, 1].sum()))

    # gp = df.groupby([0, 4, 5, 6, 7], sort=True)
    for col in ['dir%s' % x for x in range(1, 6)]:
        L = ['dir%s' % x for x in range(1, int(col[-1]) + 1)]
        # print(L)
        gp = df.groupby(['name'] + L, sort=False)  # 加速计算
        mygp = gp['size'].agg([len, numpy.sum, getsizeL])
        if mod == 3:
            print('\n###统计文件所属人各个分级文件大小：')
            print('%s\n%s\n%s' % ('-' * 50, col, '-' * 50))
            print(mygp.sort_values(['name'] + L[:-1] +
                                   ['sum'], ascending=True).to_string())  # 排序打印
        if mod == 0 and col == 'dir1':
            print('##统计文件所属人总大小：')
            print(mygp.sort_values(['sum'], ascending=False).to_string())  # 排序打印
            # np = mygp.to_records()
            # for x in sorted(np, key=lambda x: -x[3]):
            #     for xx in x:
            #         try:
            #             print(xx.decode(), sep='\t', end='\t')
            #         except Exception:
            #             print(xx, sep='\t', end='\t')
            #     print()

    # 遍历
    # for row in df.iteritems():
    #     print(row)

    # print('3. 写入文件...')
    # print(gp.to_string())
    # with open('info.txt', 'w') as fo:
    #     fo.write(gp.to_string())

    # gp2 = gp[1].sum()
    # gp2 = gp.describe(include=[numpy.number])
    # gp2 = gp.describe().reset_index()
    # gp2.to_excel('out.xlsx', sheet_name='Sheet1')


def fmain():
    for file in sorted(os.listdir('result')):
        print('\n\n### deal:', file)
        fmain_00(file)
    for file in sorted(os.listdir('result')):
        print('\n\n### deal:', file)
        fmain_00(file, mod=3)


def main():
    print('欢迎使用集群磁盘统计工具。',
          '本次结果中每个标题开头都为“###”,',
          '可以直接搜索快速跳转查看')
    fmain()


if __name__ == '__main__':
    main()
