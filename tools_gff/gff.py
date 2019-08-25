#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
python prj2-all.py prj2_congfig.txt
配置文件中，每行只能有一个=号，否则结果会有错
对于fname Pbr%06d-v2
'''

import os
import sys
import re
# sys.path.append('/ifs/TJPROJ3/Plant/chenjun/mytools')
# sys.path.append('/NJPROJ2/Plant/chenjun/mytools')
# import fas


class gff:

    def __init__(self, Largv):
        self.prjname, self.plantname, self.path_falenth, self.path_gff, self.path_cds, self.path_pep = Largv   # 文件
        self.path_gffsort = '%s.gff.sort' % self.prjname
        self.Lgetlist = []  # 用于存放基因序列长度信息，从长到短的排序
        self.L = []  # 用于存放gff每一行数据
        self.Lsort = []  # 用于存放gff排序后每一行数据

    def gffsort(self):

        # 第一步，获取按大到小的统计基因列表，设置排序字典，以及指定另一个排序字典
        Dtype = {'chromosome': 0,
                 'ncRNA_gene': 1,
                 'ncRNA': 2,
                 'lnc_RNA': 3,
                 'tRNA': 4,
                 'rRNA': 5,
                 'miRNA': 6,
                 'snoRNA': 7,
                 'snRNA': 8,
                 'SRP_RNA':9,
                 'RNase_MRP_RNA': 10,
                 'pre_miRNA': 11,
                 'gene': 12,
                 'mRNA': 13,
                 'three_prime_UTR': 14,
                 'exon': 15,
                 'CDS': 16,
                 'five_prime_UTR': 17
                 }

        # 获取基因序列从大到小排序的列表
        with open(self.path_falenth) as file_falenth:
            for data in file_falenth:
                Ldata = data.split('\t')
                Ldata = [x.strip() for x in Ldata]
                self.Lgetlist.append(Ldata)

        Dgetlist = {}  # 用于后面插入Ldata第0位，用于排序，结构为{gene1:1,gene2:2,gene3:3}
        for i in range(len(self.Lgetlist)):
            Dgetlist[self.Lgetlist[i][0]] = i

        # 第二步，读取gff文件原始数据
        print('\n正在读取gff文件...\n路径: %s' % path_gff)
        cn = 0
        with open(self.path_gff) as file_gff:
            for data in file_gff:
                cn += 1
                if data.startswith('#'):
                    continue
                Ldata = data.split('\t')
                if Ldata[0] in Dgetlist:  # 用于检查错误，可能file_gff里面的染色体多于file_falenth
                    Ldata.insert(0, Dgetlist[Ldata[0]])  # 敢这么做是因为gff染色体完全被包含于fa，若不是如此则报错
                    Ldata.append(Dtype[Ldata[3]])
                    self.L.append(Ldata)
                else:
                    print("%s中排序发现错误，第%d行染色体%s不在文件%s中" % (self.path_gff, cn, Ldata[0], self.path_falenth))
                    sys.exit()
        # print(L[0]) #['16',Chr01', 'EVM', 'gene', '16', '1185', '.', '-', '.',
        # 'ID=evm.TU.Scaffold_110_2_fragment_30801_158131.9;Name=EVM%20prediction%20Scaffold_110_2_fragment_30801_158131.9']

        # 第三步，排序
        # 先按第1列正排序，在按第4列先正排序，在按第5列逆排序，最后按第3列排序
        print('\n排序中...')
        self.Lsort = sorted(self.L, key=lambda x: (x[0], int(x[4]), -int(x[5]), x[-1]))
        with open(self.path_gffsort, "w") as file_sort:
            for Ldata_sort in self.Lsort:
                file_sort.write('\t'.join(Ldata_sort[1:-1]))
        print('已保存好排序文件，路径为: \n%s' % self.path_gffsort)

    def fzhushi(self):

        # 提前输出结果的目录准备
        mkpath = 'results'
        isExists = os.path.exists(mkpath)
        if not isExists:
            os.makedirs(mkpath)
        os.chdir(mkpath)  # 进入输出目录

        # 第四步，写入列表文件,并建立字典，重写注释gff文件
        print('排序完毕！正在写入列表list文件，重新注释gff文件...')
        D_gff = {}  # 建立字典，用于后面替换cds和pep文件，格式为scafoldxxx:pgene
        filelist_name = "%s_list.txt" % prjname
        prjname_gff_new = '%s_new.gff' % prjname
        with open(prjname_gff_new, 'w') as filenew:
            with open(filelist_name, "w") as filelist:
                pNAME = ''  # 记录第一列初始值
                BEGIN, END = 0, 0  # 统计基因起止
                pCOUNT = 0  # 用于记录统计的第几个基因
                pgene = ''  # 用于合成新的基因注释名字 pgene = 'Pxx0000001'
                cn_exon = 0  # 用于记录这个基因中第几个exon
                for i in range(len(Lsort)):
                    Ldata = Lsort[i]
                    ID = 'ID=%s' % pgene
                    Parent = ';Parent=%s' % pgene
                    Name = ''
                    if pNAME != Ldata[1]:  # 判断此条染色体
                        pNAME = Ldata[1]
                        BEGIN, END = 0, 0
                    BEGIN, END = int(Ldata[4]), int(Ldata[4])
                    if BEGIN > END:
                        if Ldata[3] != 'gene':
                            print("\n----------\n有基因注释缺失，此行内容为: \n" +
                                  ('\t'.join(Ldata[1:-1])))
                            raise
                    if Ldata[3] == 'gene':
                        pCOUNT += 1
                        pgene = plantname % pCOUNT
                        Parent = ''
                        ID = 'ID=%s' % pgene
                        Name = ';Name=EVM%%20prediction%%20%s' % pgene
                        cn_exon = 0
                    elif Ldata[3] == 'mRNA':
                        Scf_name = re.findall('ID=(.*?);', Ldata[-2])[0]
                        Name = ';Name=EVM%%20prediction%%20%s' % pgene
                        pgene = plantname % pCOUNT
                        filelist.write('\t'.join([pNAME, Scf_name, str(Ldata[4]), str(Ldata[5]), pgene]) + '\n')
                        if Scf_name not in D_gff.keys():
                            # 得到字典如: {Scaffold_110xxx:chro1}
                            D_gff[Scf_name] = pgene
                        else:
                            print("注意！！发现标注的基因重复，文件可能有误，内容为: " + Scf_name)
                            raise
                    elif Ldata[3] == 'exon':
                        cn_exon += 1
                        ID += '.exon%d' % cn_exon
                    zhushi = ID + Parent + Name
                    filenew.write('\t'.join(Ldata[1:-2]) + '\t' + zhushi + '\n')
        print('\n写入完毕，请于当前文件夹查看文件: %s' % filelist_name)
        print('写入完毕，请于当前文件夹查看文件: %s' % prjname_gff_new)

        # 第五步，写入cds_new文件和pep文件
        if path_cds == '':
            print('未写入cds')
        else:
            print('正在写入cds文件...')
            prjname_cds_new = "%s_new.cds" % prjname
            with open(path_cds) as file_cds:
                with open(prjname_cds_new, "w") as file_cds_new:
                    for data in file_cds:
                        if data.startswith('>'):
                            re_data = re.findall('>(.*)', data)[0]
                            data = '>%s\n' % D_gff[re_data]
                        file_cds_new.write(data)
            print('写入完毕，请于当前文件夹查看文件: %s' % prjname_cds_new)

        if path_pep == '':
            print('未写入pep')
        else:
            print('正在写入pep文件...')
            failename_pep_new = "%s_new.pep" % prjname
            with open(path_pep) as file_pep:
                with open(failename_pep_new, "w") as file_pep_new:
                    for data in file_pep:
                        if data.startswith('>'):
                            re_data = re.findall('>(.*)', data)[0]
                            data = '>%s\n' % D_gff[re_data]
                        file_pep_new.write(data)
            print('写入完毕，请于当前文件夹查看文件: %s' % failename_pep_new)
        os.chdir('..')  # 一次循环结束，返回主目录

    def gffclean(self):
        fname, fname_new = self.path_gffsort, '%s.clean' % self.path_gffsort
        fi = open(fname)
        fo = open(fname_new, 'w')
        fo.write("##gff-version 3\n")

        # 计算文件最后一位的位置
        fi.seek(0, 2)
        seek_end = fi.tell()
        fi.seek(0, 0)

        seek_old = 0  # 初始变量
        S_genetype_raw = set(['gene', 'mRNA', 'CDS'])
        S_genetype = set()
        while True:
            line = fi.readline()
            if not line:  # 判断是否到文件末尾
                if fi.tell() == seek_end:
                    break
            S_genetype = set()  # 设置集合，用于判断基因类型，看gene,mRNA,CDS是否都有
            if line.startswith("#"):
                continue
            genetype = line.split('\t')[2]
            if genetype == "gene":
                seek_old = fi.tell()
                line_next = fi.readline()
                genetype_next = line_next.split('\t')[2]
                if genetype_next == "mRNA":
                    fi.seek(seek_old)  # 光标归位到mRNA一行去
                    line = line.replace(":", "_")  # 避免特殊字符:
                    line = line.replace(" ", "_")  # 避免特殊字符空格
                    fo.write(line)
                    S_genetype.add(genetype)
                    while True:
                        line_next = fi.readline()
                        if not line_next:  # 考虑是否读取到最后一行
                            break
                        genetype_next = line_next.split('\t')[2]
                        if genetype_next == "gene":  # 是基因则进入下一次判断及写入
                            fi.seek(-len(line_next), 1)
                            if S_genetype != S_genetype_raw:
                                print(S_genetype)
                                print('文件有误，缺少CDS数据\n此行数据为：\n' + line_next)
                                sys.exit()
                            break
                        if genetype_next in S_genetype_raw:  # 如果是mRNA，CDS则写入
                            line_next = line_next.replace(":", "_")
                            line_next = line_next.replace(" ", "_")
                            fo.write(line_next)
                            S_genetype.add(genetype_next)
        fi.close()
        fo.close()


if __name__ == '__main__':
    # with open('prj2_config.txt') as file_congfig:
    #     L, Ld = [], []  # L用于存储总的配置，Ld用于存储每一项配置
    #     for data in file_congfig:
    #         if data.strip().startswith("#"):  # 配置文件中可以使用注释语句
    #             continue
    #         if data.startswith(">"):  # 每条配置以此开始，读取此后的6行，加入L
    #             Ld = []
    #             for i in range(6):
    #                 data = next(file_congfig)
    #                 Ldata = data.split('=')
    #                 Ldata = [x.strip() for x in Ldata]
    #                 print(Ldata)
    #                 Ld.append(Ldata[1])
    #         L.append(Ld)

    #     for Largv in L[1:]:
    #         # print(Largv)
    #         fzhushi(Largv)

    prjname = r'Ara'
    plantname = r''
    path_falenth = r'Ara.fa.length'
    path_gff = r'Ara.gff'
    path_cds = r''
    path_pep = r''

    Largv = [prjname, plantname, path_falenth, path_gff, path_cds, path_pep]
    s1 = gff(Largv)
    s1.gffsort()
    s1.gffclean()

# 排序算法有问题，日后研究吧，相同的一段序列还存在多种不同翻译情况，这种情况该如何处理。。。
# 1       araport11       gene    6788    9130    .       -       .       ID=gene_AT1G01020;Name=ARV1;biotype=protein_coding;description=ARV1_[Source_UniProtKB/TrEMBL%3BAcc_Q5MK24];gene_id=A
# 1       araport11       mRNA    6788    9130    .       -       .       ID=transcript_AT1G01020.3;Parent=gene_AT1G01020;biotype=protein_coding;transcript_id=AT1G01020.3
# 1       araport11       mRNA    6788    9130    .       -       .       ID=transcript_AT1G01020.5;Parent=gene_AT1G01020;biotype=protein_coding;transcript_id=AT1G01020.5
# 1       araport11       mRNA    6788    9130    .       -       .       ID=transcript_AT1G01020.4;Parent=gene_AT1G01020;biotype=protein_coding;transcript_id=AT1G01020.4
# 1       araport11       mRNA    6788    9130    .       -       .       ID=transcript_AT1G01020.1;Parent=gene_AT1G01020;biotype=protein_coding;transcript_id=AT1G01020.1
# 1       araport11       mRNA    6788    8737    .       -       .       ID=transcript_AT1G01020.6;Parent=gene_AT1G01020;biotype=protein_coding;transcript_id=AT1G01020.6
# 1       araport11       mRNA    6788    8737    .       -       .       ID=transcript_AT1G01020.2;Parent=gene_AT1G01020;biotype=protein_coding;transcript_id=AT1G01020.2
# 1       araport11       CDS     6915    7069    .       -       2       ID=CDS_AT1G01020.3;Parent=transcript_AT1G01020.3;protein_id=AT1G01020.3
# 1       araport11       CDS     6915    7069    .       -       2       ID=CDS_AT1G01020.5;Parent=transcript_AT1G01020.5;protein_id=AT1G01020.5
# 1       araport11       CDS     6915    7069    .       -       2       ID=CDS_AT1G01020.4;Parent=transcript_AT1G01020.4;protein_id=AT1G01020.4
# 1       araport11       CDS     6915    7069    .       -       2       ID=CDS_AT1G01020.1;Parent=transcript_AT1G01020.1;protein_id=AT1G01020.1
# 1       araport11       CDS     7157    7232    .       -       0       ID=CDS_AT1G01020.3;Parent=transcript_AT1G01020.3;protein_id=AT1G01020.3
# 1       araport11       CDS     7157    7232    .       -       0       ID=CDS_AT1G01020.5;Parent=transcript_AT1G01020.5;protein_id=AT1G01020.5
# 1       araport11       CDS     7157    7232    .       -       0       ID=CDS_AT1G01020.4;Parent=transcript_AT1G01020.4;protein_id=AT1G01020.4
# 1       araport11       CDS     7157    7232    .       -       0       ID=CDS_AT1G01020.1;Parent=transcript_AT1G01020.1;protein_id=AT1G01020.1
