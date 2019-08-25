# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-06-09 14:56:42
# @Last Modified by:   JUN
# @Last Modified time: 2019-07-03 15:39:27


import sys


def getsize(size):
    D = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    for x in D:
        if size < 1024**(x + 1):
            hsize = str('%.3f' % (int(size) / 1024**x)) + D[x]
            return hsize


def fmain(fixiangmu, num, fimerge, fisize):
    # 包含项目的文件，包含项目的文件第几列，merge文件，扫盘文件(大小\t文件路径)
    Lxiangmu = [x.strip().split('\t')[int(num) - 1] for x in open(fixiangmu)]
    L = []
    with open(fimerge) as fi:
        for line in fi:
            Lline = line.strip().split('\t')
            # print(Lline)
            if len(Lline) > 2:
                L.append(Lline)
    Lsize = []
    with open(fisize) as fi:
        for line in fi:
            Lline = line.strip().split('\t')
            Lline[0] = int(Lline[0])
            if Lline[0] == 0:
                continue
            else:
                Lsize.append(Lline)
    # Ltongji = []  # [[xiangmu,size],[...],...]
    allsize = 0
    # print(Lsize)
    for xiangmu in Lxiangmu:
        if (xiangmu == '-') or not xiangmu:
            print('-', '-', '-',sep='\t')
            continue
        Ltmp = []
        for Lline in L:
            # print(Lline)
            # sys.exit()
            if Lline[4] == xiangmu:
                Ltmp.append(Lline[1])
        size = 0
        # print(Ltmp)
        for path in Ltmp:
            for Lline in Lsize:
                # print(path, Lline[1])
                if path in Lline[1]:
                    size += Lline[0]
        allsize += size
        # print(size)
        print(xiangmu, getsize(size),size, sep='\t')
    print('\n所有项目大小:', getsize(allsize))
    print('扫盘总大小：', getsize(sum([x[0] for x in Lsize])))


def main():
    fixiangmu, num, fimerge, fisize = sys.argv[1:5]
    fmain(fixiangmu, num, fimerge, fisize)
    # fmain('lst.merge.tiqu', '4', 'lst.merge.final', 'result.path.size')


if __name__ == '__main__':
    main()
