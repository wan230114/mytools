# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2018-11-22 13:00:50
# @Last Modified by:   JUN
# @Top Modified time: 2019-01-11 13:20:29
# @Last Modified time: 2019-04-11 17:03:45

# 改进计划，将ID，Parent的对应严格加入
# 2019-04-11 mRNA修正错误
# 改进计划：改进输出第九列冗余输出; mRNA、CDS行严格对应


shelp = """--help
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Date:   2018-11-22 13:00:50
功能：
    1 筛选gene、mRNA、CDS的行
    2 按gene > mRNA > CDS排序
    3 CDS编号 (将CDS行中"CDS:"或":cds"去除，并在末尾加上":cds编号")
    4 去除重复行
    5 去除冗余的行
        (1) 只有gene，无mRNA的基因相关行
        (2) 信息缺失的mRNA及其CDS行：
            信息不全的mRNA行(只有mRNA行无CDS行)
            信息不全的CDS行(只有CDS行无对应的mRNA行)
        (3) 判定结束，必须至少有一个mRNA及对应CDS，否则整个基因相关行会被去除
用法：
    python sort_clean.py file
注意：
    输入文件的ID，Parent须对应
"""

import sys
import re
import time


def clean(Largv):
    finame = Largv[1]
    foname = finame + '.clean'
    fi = open(finame, 'r', encoding='UTF-8')
    fo = open(foname, 'w')
    fo.write('##gff-version 3\n')

    t0 = time.time()
    print('处理中...')
    L = []  # 存储总的Lline
    D = {}  # 存储mRNA对应的gene是什么，为了让CDS_ID获取到geneID，从而方便排序
    Dtype = {'gene': 1, 'mRNA': 2, 'CDS': 3}

    # 1) 必须先提前建立D，因为CDS可能出现极个别错误在mRNA的前面
    while True:
        line = fi.readline()
        if not line:
            break
        if line.startswith('#') or (not line.strip()):
            continue
        Lline = line.strip().split('\t',9)[:9]   # 纠正流程错误
        Lline[8] = Lline[8].split()[0]   # 纠正流程错误
        if Lline[2] == 'mRNA':
            ID_name = re.findall('ID=(.*?)[;,]', Lline[8] + ';')[0]
            # print(ID_name)
            # print(Lline[8]+';')
            Parent_name = re.findall('Parent=(.*?)[;,]', Lline[8] + ';')[0]
            D[ID_name] = Parent_name
        # 过滤出gene、mRNA、CDS的行
        elif Lline[2] not in Dtype:
            Lline = []
        if Lline:
            L.append(Lline)
    # print(D)

    # 2) 给每一行增加基因标识
    for Lline in L:
        if Lline[2] == 'gene':
            ID_name = re.findall('ID=(.*?)[;]', Lline[8] + ';')[0]
            Lline.extend([ID_name, ID_name, Dtype[Lline[2]]])
        elif Lline[2] == 'mRNA':
            ID_name = re.findall('ID=(.*?)[;]', Lline[8] + ';')[0]
            Parent_name = re.findall('Parent=(.*?)[;,]', Lline[8] + ';')[0]
            Lline.extend([Parent_name, ID_name,  Dtype[Lline[2]]])
            D[ID_name] = Parent_name
        elif Lline[2] == 'CDS':
            # ID_name = re.findall('ID=(.*?)[;]', Lline[8]+';')[0]
            # print(Lline[8]+';')
            Parent_name = re.findall('Parent=(.*?)[;,]', Lline[8] + ';')[0]
            Lline.extend([D[Parent_name], Parent_name, Dtype[Lline[2]]])

    # 3) 去重并排序
    L = [tuple(x) for x in L]
    L = sorted(list(set(L)), key=lambda x: (x[-3], x[-2], x[-1]))
    with open(finame + '.sort', 'w') as fosort:
        for Lline in L:
            # print(Lline)
            fosort.write('\t'.join(Lline[:-3]) + '\n')

    # 4) 去除没有mRNA的gene及其信息
    Ltmp = []  # 暂存每一个基因符合要求的信息
    i = -1
    while True:
        i += 1
        try:
            Lline = L[i]
        except:
            break
        Ltmp = []
        pGENE = 0  # 用于判断是否有mRNA和CDS同时存在的行
        # 排除只有基因的行
        try:
            if L[i + 1][2] == 'gene':
                # print(Lline)
                print('冗余gene行被去除', L[i])
                continue
        except:
            break
        if Lline[2] == 'gene':
            PLline_gene = Lline[:-3]
            while True:
                i += 1
                try:
                    Lline = L[i]
                except:
                    break
                # if L[i] == L[i-1]
                # 排除CDS进入mRNA的行
                try:
                    if L[i + 1] == 'mRNA':
                        print('冗余mRNA行被去除', L[i])
                except:
                    pass
                if Lline[2] == 'mRNA':
                    n_CDS = 0
                    Ltmp.append(L[i - 1][:9])  # 记录有mRNA的基因
                    while True:  # 读取mRNA
                        i += 1
                        try:
                            Lline = L[i]
                        except:
                            break
                        # 排除多余的mRNA行
                        if Lline[2] == 'CDS':
                            pGENE = 1
                            Ltmp.append(L[i - 1][:9])  # 加入mRNA行
                            ID_mRNA = re.findall('ID=(.*?)[;]', L[i-1][8] + ';')[0]
                            while True:
                                if Lline[2] == 'CDS':
                                    n_CDS += 1
                                    Lline = list(Lline)
                                    # print(Lline[8]+';')
                                    oldID = re.findall('ID=(.*?)[;]', Lline[8] + ';')[0]
                                    #tmpCDS = re.findall('CDS:|cds.|:cds', oldID)[0]
                                    #newID = oldID.replace(tmpCDS, ID_mRNA)
                                    newID = 'ID=' + ID_mRNA + '.cds' + str(n_CDS)
                                    Lline[8] = Lline[8].replace('ID=%s' % oldID, newID)
                                    Ltmp.append(Lline[:9])
                                else:
                                    n_CDS = 0
                                    i -= 1
                                    break
                                i += 1
                                try:
                                    Lline = L[i]
                                except:
                                    break
                        elif Lline[2] == 'gene':
                            i -= 1
                            break
                elif Lline[2] == 'gene':
                    i -= 1
                    break
        if pGENE:
            pGENE = 0
            for Lline in Ltmp:
                fo.write('\t'.join(Lline[:9]) + '\n')
        else:
            print('该基因及相关行缺少CDS被去除:', PLline_gene)
    fi.close()
    fo.close()
    print('输出的新文件是: %s' % foname)
    print('处理完毕，耗时%f秒' % (time.time() - t0))
if __name__ == "__main__":
    Largv = sys.argv
    # Largv = ['', 't.gff3']
    if len(Largv) == 1:
        print(shelp)
        sys.exit()
    elif Largv[1] == '-h':
        print(shelp)
        sys.exit()
    elif len(Largv) == 2:
        print('您输入的文件是: %s' % Largv[1])
        try:
            with open(Largv[1]) as f:
                pass
        except:
            print('文件读取错误，文件或不存在')
            print(shelp)
            sys.exit()
    elif len(Largv) > 2:
        print('您输入的参数是: %s请检查输入参数是否正确' % (' '.join(Largv[1:])))
        print(shelp)
    clean(Largv)
