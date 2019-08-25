# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-06-09 14:56:42
# @Last Modified by:   JUN
# @Last Modified time: 2019-07-26 13:19:36


import os
import sys
import openpyxl
from collections import OrderedDict


def getsize(size):
    D = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    for x in D:
        if size < 1024**(x + 1):
            hsize = str('%.3f' % (int(size) / 1024**x)) + D[x]
            return hsize


def printtmp(L):
    def f(*args):
        L.append(args)
    return f


def printxlsw(L, fows, fo, nrowL):
    def f(*args):
        print(*args, sep="\t", file=fo)
        for i, values in enumerate(args):
            #print(nrowL, i, values)
            fows.cell(row=nrowL[0], column=i + 1, value=values)
        nrowL[0] += 1
    return f


def list2html(L):
    Lstr = []
    Lstr.append(
        '<table border="1" cellspacing="0" cellpadding="6" style="word-break: break-all;"  width="1480px">')
    Lstr.append('<tr>')

    L_width = ['width="80px"', 'width="140px"', 'width="120px"',
               'width="90px"', 'width="90px"', 'width="180px"', '']
    for s_width, x in zip(L_width, L[0]):
        Lstr.append('<th %s>%s</th>' % (s_width, x))
    Lstr.append('</tr>')
    for Lline in L[1:]:
        Lstr.append('<tr>')
        for x in Lline:
            Lstr.append('<td>%s</td>' % x)
        Lstr.append('</tr>')
    Lstr.append('</table>')
    return ''.join(Lstr)


def fmain(fixiangmu, num, fimerge, fisize):
    '''包含项目的文件，包含项目的文件第几列，merge文件，扫盘文件(大小\\t文件路径)'''
    pwd = os.getcwd()
    Lprint = []
    col = int(num) - 1
    Dxiangmu = OrderedDict()
    with open(fixiangmu, encoding='utf8') as fi:
        for line in fi:
            if line.startswith('#'):
                continue
            Lline = line.strip().split('\t')
            Dxiangmu[Lline[col]] = Lline[:col] + Lline[col:]
    L = []
    with open(fimerge, encoding='utf8') as fi:
        for line in fi:
            Lline = line.strip().split('\t')
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
    print_tmp = printtmp(Lprint)
    print_tmp(*['#文库数量', '大小(b/k/m/g/t)', '大小(b)', '信息负责人', '运营', '项目编号', '项目名称'])
    allwenku = 0
    allsize = 0
    for xiangmu in Dxiangmu:
        allwenku += int(Dxiangmu[xiangmu][0])
        if (xiangmu == '-') or not xiangmu:
            print_tmp(*([Dxiangmu[xiangmu][0], '-', '-'] + Dxiangmu[xiangmu][1:]))
            continue
        Ltmp = []
        for Lline in L:
            # sys.exit()
            if Lline[4] == xiangmu:
                Ltmp.append(Lline[1])
        size = 0
        for path in Ltmp:
            for Lline in Lsize:
                if path in Lline[1]:
                    size += Lline[0]
        allsize += size
        print_tmp(*([Dxiangmu[xiangmu][0], getsize(
            size), str(size)] + Dxiangmu[xiangmu][1:]))
    # 写
    wb = openpyxl.Workbook()  # 创建对象
    ws = wb.active  # 创建标签
    nrowL = [1]
    fo_txt = open('%s--tongji.txt' % fimerge, 'w')
    print_xlsw = printxlsw(L, ws, fo_txt, nrowL)
    print('#' * 96, file=fo_txt)
    print_xlsw('##下机信息路径:', fimerge)
    print_xlsw('##项目大小:', getsize(allsize))
    print_xlsw('##扫盘大小：', getsize(sum([x[0] for x in Lsize])))
    print_xlsw('##文库数量:', allwenku)
    print('#' * 96, file=fo_txt)
    print_xlsw('###')
    for args in Lprint:
        print_xlsw(*args)
    wb.save("%s--tongji.xlsx" % fimerge)
    fo_txt.close()
    with open('%s--tongji.html' % fimerge, 'w') as fo:
        fo.write('<font style="font-size:16px">hi, all:<br>&nbsp;&nbsp;&nbsp;&nbsp;以下项目涉及的下机文库即将上云并在本地删除。<br>&nbsp;&nbsp;&nbsp;&nbsp;<font color="#FF0000"><strong>若需要本地保留，请相关项目负责人两日内回复。</strong></font><br>&nbsp;&nbsp;&nbsp;&nbsp;我们将在下周二统一提交删除</font><br>')
        fo.write('<br>下机信息路径:&nbsp;%s/%s' % (pwd, fimerge))
        fo.write('<br>统计到的项目大小:&nbsp;%s' % getsize(allsize))
        fo.write('<br>本次所有扫盘大小:&nbsp;%s' % getsize(sum([x[0] for x in Lsize])))
        fo.write('<br>文库数量:&nbsp;%s<br>' % allwenku)
        fo.write('<br>统计信息路径(文本版):&nbsp;%s/%s--tongji.txt' % (pwd, fimerge))
        fo.write('<br>统计信息路径(表格版):&nbsp;%s/%s--tongji.xlsx' % (pwd, fimerge))
        fo.write('<br>统计信息预览:<br>')
        fo.write(list2html(Lprint))


def main():
    fixiangmu, num, fimerge, fisize = sys.argv[1:5]
    fmain(fixiangmu, num, fimerge, fisize)
    # fmain('lst.merge.tiqu', '4', 'lst.merge.final', 'result.path')


if __name__ == '__main__':
    main()
