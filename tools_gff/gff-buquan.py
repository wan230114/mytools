# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-02-15 14:31:12
# @Last Modified by:   JUN
# @Last Modified time: 2019-02-15 16:06:22

# 本程序用于补全gff文件中缺失gene和mRNA的行


import sys
import re


def decgene(Ltmp):
    Sgene = {x[2] for x in Ltmp}
    Spoint = set()
    Spoint.update({x[3] for x in Ltmp})
    Spoint.update({x[4] for x in Ltmp})
    Llinetmp = []
    for Lline in Ltmp:
        if Lline[2] == 'CDS' or Lline[2] == 'exon':
            Llinetmp = Lline
            break
    print(Sgene)
    if 'gene' not in Sgene:
        Lnew = Llinetmp[0:3] +\
            ['gene', min(Spoint), max(Spoint)] +\
            Llinetmp[5:8] +\
            ['ID=%s;Name=EVM%%20prediction%%20%s' %
             (Llinetmp[-1], Llinetmp[-1])] + [Llinetmp[-1]]
        Ltmp.insert(0, Lnew)
        # print('已插入gene行：', Lnew)
    if 'mRNA' not in Sgene:
        Lnew = Llinetmp[0:3] +\
            ['mRNA', min(Spoint), max(Spoint)] +\
            Llinetmp[5:8] +\
            ['ID=%s;Parent=%s;Name=EVM%%20prediction%%20%s' %
             (Llinetmp[-1], Llinetmp[-1], Llinetmp[-1])] + [Llinetmp[-1]]
        Ltmp.insert(1, Lnew)
        # print('已插入mRNA行：', Lnew)
    return Ltmp


def fmain(finame, foname):
    fi, fo = open(finame), open(foname, 'w')
    Dgenetype = {'gene': 1, 'mRNA': 2, 'CDS': 3, 'exon': 4,
                 'three_prime_UTR': 5, 'five_prime_UTR': 6}
    L = []
    for line in fi:
        Lline = line.rstrip().split('\t')
        ID = re.findall('ID=(.*?);', Lline[8])[0]
        if Lline[2] == 'gene':
            Parent = ID
        else:
            Parent = re.findall('ID=(.*?);', Lline[8] + ';')[0]
        Lline.append(Parent)
        L.append(Lline)
    L = sorted(L, key=lambda x: (x[-1], int(x[3]), int(x[4]), Dgenetype[x[2]]))

    i = 0
    maxi = len(L)
    Lline = L[0]
    geneID = Lline[-1]
    Ltmp = [Lline]
    Lall = []
    while True:
        i += 1
        if i == maxi:
            Ltmp = decgene(Ltmp)
            Lall.append(Ltmp)
            break
        Lline = L[i]
        if Lline[-1] == geneID:
            Ltmp.append(Lline)
        else:
            Ltmp = decgene(Ltmp)
            Lall.append(Ltmp)
            Ltmp = [Lline]
            geneID = Lline[-1]

    for Ltmp in Lall:
        for Lline in Ltmp:
            fo.write('\t'.join(Lline[:-1]) + '\n')

    fi.close()
    fo.close()


def main():
    finame, foname = sys.argv[1:3]
    fmain(finame, foname)


if __name__ == '__main__':
    main()
