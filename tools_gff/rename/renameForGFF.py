# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com 
# @Qmail:  1170101471@qq.com
# @Date:   2018-10-26 15:33:21
# @Last Modified by:   JUN
# @Last Modified time: 2019-03-05 16:45:29

'''
python prj2-all.py prj2_congfig.txt
'''
# 1 先全部按照基因排序
# 2 构建数据结构
# 需要重构数据结构

from multiprocessing import Pool
import os
import sys
import re
import traceback
sys.path.append('/ifs/TJPROJ3/Plant/chenjun/mytools/tools_fasta')
import fas


class renameforgff:
    """docstring for renameforgff"""

    def __init__(self, Largv):
        self.filename, self.Rename, self.path_cds, \
            self.path_fa, self.path_gff, self.path_pep = Largv   # 文件
        # PRJNAME = self.filename
        L = re.findall('0+', self.Rename)
        for num in L:
            self.Rename = self.Rename.replace(num, '{:0>%s}' % len(num), 1)

        print('输入的文件是: ')
        for i in Largv[2:]:
            print(i)
        # 提前输出结果的目录准备
        self.mkpath = 'results'
        try:
            os.makedirs(self.mkpath)
        except Exception:
            pass
        self.main()

    def main(self):
        os.chdir(self.mkpath)  # 进入输出目录
        Dgenetype, Dgenelist = self.step1_fa()
        self.step2_gff(Dgenetype, Dgenelist)
        print('正在写入pep&cds文件...')
        self.step3_write_pep_cds('pep', self.path_pep)
        self.step3_write_pep_cds('cds', self.path_cds)
        os.chdir('..')  # 一次循环结束，返回主目录

    def step1_fa(self):
        # 第一步，获取按大到小的统计基因列表，设置排序字典，以及指定另一个排序字典
        Dgenetype = {'gene': 1, 'mRNA': 2, 'CDS': 3, 'exon': 4,
                     'three_prime_UTR': 5, 'five_prime_UTR': 6}
        # Dgenetype = {'gene': 1, 'mRNA': 2, 'five_prime_UTR': 3, 'exon': 4, 'CDS': 5, 'three_prime_UTR': 6}
        # 获取基因从大到小排序的列表
        getlist = fas.fas(['', self.path_fa, '-o', self.filename + '.fa.length']).fmain()
        # os.rename(self.path_fa + '.length', self.filename + '.length')
        Dgenelist = {}
        self.Dgenelist2 = {}
        for i, gene in enumerate(getlist):
            Dgenelist[gene[0]] = i + 1
            if 'chr' in gene[0]:
                self.Dgenelist2[gene[0]] = i + 1
            else:
                self.Dgenelist2[gene[0]] = 'ct'
        return Dgenetype, Dgenelist

    def step2_gff(self, Dgenetype, Dgenelist):
        '''处理gff'''
        # 第二步，读取gff文件原始数据，存入L中，进行排序
        # 1) 初次按照所属的基因排序
        # 将所有的基因打包起来放在一起
        # 将gff读进内存，先提前建立D={ID:Parents}，用于将所有数据排序
        D_parent = {}  # 存储mRNA对应的gene是什么，为了让CDS/exon等ID获取到geneID，从而方便排序
        Llines_allraw = []  # 用于存储所有的行，末尾标注出其Parents，作为键
        print('正在读取gff文件...')
        with open(self.path_gff) as fi:
            for line in fi:
                if line.startswith('#'):
                    continue
                Lline = line.strip().split('\t')
                s_key = ''
                Lline[8] += '\n'
                if Lline[2] == 'gene':
                    # ID_name = re.findall('ID=(.*?)[;\n]', Lline[8])[0]
                    ID_name = re.findall('ID=(.*?)[;\n]', Lline[8])[0].rstrip('.p')
                    D_parent[ID_name] = ID_name
                    s_key = ID_name
                elif Lline[2] == 'mRNA':
                    # print(Lline)
                    ID_name = re.findall('ID=(.*?)[;\n]', Lline[8])[0]
                    try:
                        Parent_name = re.findall('Parent=(.*?)[;,\n]', Lline[8])[0]
                    except Exception:
                        Parent_name = ID_name
                    D_parent[ID_name] = Parent_name
                    s_key = Parent_name
                else:
                    # print(Lline[8])
                    Parent_name = re.findall('Parent=(.*?)[;,\n]', Lline[8])[0]
                    s_key = Parent_name
                Lline.append(Dgenelist[Lline[0]])
                Lline.append(Dgenetype[Lline[2]])
                Lline.append(ID_name)
                Lline.append(s_key)
                Llines_allraw.append(Lline)
        # [print(x) for x in Llines_allraw]

        # 将所有的Parent在末尾加上新的内容，转换为其对应的基因，并按照末尾的基因ID排序
        Llines = []  # [[...line数据,chrmo,type,ID,s_key,GeneID],[],[],...]
        for Lline in Llines_allraw:
            Lline.append(D_parent[Lline[-1]])
            Llines.append(Lline)
        print('文件读取完毕，排序中...')
        Llines = sorted(Llines, key=lambda x: (x[-1]))
        # 如果出错，请考虑相同geneID是否存在不同chr

        # 2) 排序准备：进行按基因分割打包，并进行包内排序，并将整个基因的排序信息标注于外，准备最外层排序
        # 设计数据结构
        # L = [
        #       [[该基因的所有行的数据],排序1,排序2,排序3],
        #       [[该基因的所有行的数据],排序1,排序2,排序3],
        #       [...],
        #       ...
        #     ]
        L = []
        P_gene_old = Llines[0][-1]  # 存储所属基因
        Lwhole = []  # 存储[Ltmps,排序信息]
        Ltmps = [Llines[0]]  # 存储第一行基因及之后的行[[],[]]
        for Lline in Llines[1:]:
            if P_gene_old != Lline[-1]:
                P_gene_old = Lline[-1]
                # Ltmps.insert(0, Ltmp_1)
                # Ltmp_1 = Lline
                if Ltmps[0][6] == '-':
                    Ltmps = sorted(Ltmps, key=lambda x: (-int(x[4]), int(x[3]), x[-3]))
                else:
                    Ltmps = sorted(Ltmps, key=lambda x: (int(x[3]), -int(x[4]), x[-3]))
                SChrom = set()
                for Llinetmp in Ltmps:
                    SChrom.add(Llinetmp[0])
                if len(SChrom) > 1:
                    print("WARNING :发现错误，有相同基因ID的染色体不同，该基因ID为: %s" % Ltmps[0][-1])
                    raise
                Lwhole = [Ltmps, Dgenelist[Ltmps[0][0]], int(
                    Ltmps[0][3]), int(Ltmps[0][4])]  # 放置排序指标,chrom,start,end
                L.append(Lwhole)
                Lwhole, Ltmps = [], [Lline]  # 归位，准备下个读取
            else:
                Ltmps.append(Lline)
        Lwhole = [Ltmps, Dgenelist[Ltmps[0][0]], int(Ltmps[0][3]), int(Ltmps[0][4])]
        L.append(Lwhole)
        print("总共基因数: %s" % len(L))
        # [[print(xx) for xx in x] for x in L]
        # [print(x) for x in L]

        # 3) 将基因及其所属行整体排序
        L = sorted(L, key=lambda x: (x[1], x[2], -x[3]))
        Lsort = []  # 重新归零，将排序后的数据导入
        for Lwhole in L:
            for Lline in Lwhole[0]:
                Lsort.append(Lline)
        print("总共的行数: %s" % len(Lsort))

        # 输出gff排序文件
        with open('%s.gff.sort' % self.filename, "w") as file_sort:
            for Lline in Lsort:
                file_sort.write('\t'.join(Lline[:9]))
        print('已保存好排序文件，路径为: %s' % ('%s.gff.sort' % self.filename))

        # [print(x) for x in Lsort]

        # 第四步，写入列表文件,并建立字典，重写注释gff文件
        print('排序完毕！正在写入列表list文件，重新注释gff文件...')
        self.__Dgff_mRNA__ = {}  # 建立字典，用于后面替换cds和pep文件，格式为scafoldxxx:name_NEW_gene
        fo_list_name = "%s.list" % self.filename
        foname_gff_new = '%s.gff' % self.filename
        with open(foname_gff_new, 'w') as fo_gff_new, \
                open(fo_list_name, "w") as fo_list:
            name_Chr = ''  # 记录第一列初始值
            BEGIN, END = 0, 0  # 统计基因起止
            pCOUNT = 0  # 用于记录统计的第几个基因
            name_NEW_gene = ''  # 用于合成新的基因注释名字 name_NEW_gene = 'Pxx0000001'
            cn_exon = 0  # 用于记录这个基因中第几个exon
            cn_5p = 0
            cn_3p = 0
            for i in range(len(Lsort)):
                Ldata = Lsort[i]
                ID = 'ID=%s' % name_NEW_gene
                Parent = ';Parent=%s' % name_NEW_gene
                Name = ''
                if name_Chr != Ldata[0]:  # 判断此条染色体
                    name_Chr = Ldata[0]
                    BEGIN, END = 0, 0
                BEGIN, END = int(Ldata[3]), int(Ldata[3])
                if BEGIN > END:
                    if Ldata[2] != 'gene':
                        print("\n----------\nWARNING :有基因注释缺失，此行内容为：\n" +
                              ('\t'.join(Ldata)))
                        raise
                if Ldata[2] == 'gene':
                    pCOUNT += 1
                    name_NEW_gene = self.Rename.format(self.Dgenelist2[Ldata[0]], pCOUNT)
                    Parent = ''
                    ID = 'ID=%s' % name_NEW_gene
                    Name = ';Name=EVM%%20prediction%%20%s' % name_NEW_gene
                    cn_exon = 0
                    cn_5p = 0
                    cn_3p = 0
                elif Ldata[2] == 'mRNA':
                    ID += '.mRNA'
                    Scf_name = Ldata[-3]
                    Parent_ID = Ldata[-1]
                    Name = ';Name=EVM%%20prediction%%20%s' % name_NEW_gene
                    name_NEW_gene = self.Rename.format(self.Dgenelist2[Ldata[0]], pCOUNT)
                    fo_list.write('\t'.join([Parent_ID, name_NEW_gene, name_Chr,
                                             str(Ldata[3]), str(Ldata[4]),
                                             Ldata[6]]) + '\n')
                    if Scf_name not in self.__Dgff_mRNA__:
                        self.__Dgff_mRNA__[Scf_name] = name_NEW_gene
                    else:
                        print("WARNING :注意！！发现标注的基因重复，文件可能有误，内容为：" + Scf_name)
                        raise
                elif Ldata[2] == 'exon':
                    cn_exon += 1
                    ID += '.exon%d' % cn_exon
                elif (Ldata[2] == 'CDS') or (Ldata[2] == 'cds'):
                    ID += '.cds'
                elif Ldata[2] == 'five_prime_UTR':
                    cn_5p += 1
                    ID += '.utr5p%d' % cn_5p
                elif Ldata[2] == 'three_prime_UTR':
                    cn_3p += 1
                    ID += '.utr3p%d' % cn_3p

                zhushi = ID + Parent + Name
                fo_gff_new.write('\t'.join(Ldata[:8]) + '\t' + zhushi + '\n')
        print('写入完毕，请于当前文件夹查看list文件：%s' % fo_list_name)
        print('写入完毕，请于当前文件夹查看gff文件：%s' % foname_gff_new)
        # [print(x, self.__Dgff_mRNA__[x]) for x in self.__Dgff_mRNA__]

    def step3_write_pep_cds(self, mod, path):
        print('%s写入开始...' % mod)
        foname = "%s.%s" % (self.filename, mod)
        nRow = 0
        with open(path) as fi,\
                open(foname, "w") as fo:
            for line in fi:
                nRow += 1
                if line.startswith('>'):
                    re_data = re.findall('>(.*)', line.rstrip())[0]
                    try:
                        line = '>%s\n' % self.__Dgff_mRNA__[re_data]
                    except Exception:
                        print("WARNING :第 %s 行基因: %s 未替换成功，列表对应关系不存在" % (nRow, re_data))
                fo.write(line)
        print('写入完毕，请于当前文件夹查看文件：%s' % foname)


def fmain(Largv):
    try:
        renameforgff(Largv)
    except Exception as ee:
        print('Error:', ee)
        traceback.print_exc()


def main():
    Largv = sys.argv
    # Largv = ['', 'list.txt']
    with open(Largv[1]) as file_congfig:
        L, Ld = [], []
        for data in file_congfig:
            if data.startswith("#"):
                continue
            if data.startswith(">"):
                L.append(Ld)
                Ld = []
                continue
            Ldata = data.split()
            Ldata = [x.strip() for x in Ldata]
            Ld.append(Ldata[2])
        else:
            L.append(Ld)
        p = Pool(10)
        for Largv in L[1:]:
            print(Largv)
            fmain(Largv)
            # p.apply_async(fmain, args=(Largv,))
        p.close()
        p.join()


if __name__ == '__main__':
    main()
