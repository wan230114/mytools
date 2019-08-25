# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-05-07 00:35:53
# @Last Modified by:   JUN
# @Last Modified time: 2019-05-07 11:25:39


import sys
import re


def fmain(fipath, fopath, prjname='.'):
    print(fipath, '-->', fopath)
    Llines = []
    D_Parent = {}
    D_type = {'gene': 1, 'mRNA': 2, 'CDS': 3}
    with open(fipath) as fi:
        for line in fi:
            if not line.startswith('#'):
                Lline = line.strip().split('\t')
                if Lline[2] in D_type:
                    # 1get ID
                    try:
                        c9_ID = re.findall('ID=(.*?);', Lline[8] + ';')[0]
                    except IndexError:
                        c9_ID = 'gene-' + re.findall('locus_tag=(.*?);', Lline[8] + ';')[0]

                    # 2get Parent
                    if Lline[2] == 'gene':
                        c9_Parent = c9_ID
                        D_Parent[c9_Parent] = c9_ID
                    else:
                        c9_Parent = re.findall('Parent=(.*?);', Lline[8] + ';')[0]
                    if Lline[2] == 'mRNA':
                        D_Parent[c9_ID] = c9_Parent

                    # 3get key
                    c9_geneID = None

                    # 4Name
                    Lre_Name = re.findall('Name=(.*?);', Lline[8] + ';')
                    if Lre_Name:
                        c9_Name = Lre_Name[0]
                    else:
                        c9_Name = c9_ID

                    Lline.append([c9_ID, c9_Parent, c9_geneID, c9_Name])
                    Llines.append(Lline)

    for Lline in Llines:
        Lline[-1][2] = D_Parent[Lline[-1][1]]
    Llines = sorted(Llines, key=lambda x: (x[-1][2], D_type[x[2]]))
    Lgenelines = []
    Lline = Llines[0]
    Ltemp = [Lline]
    old_geneID = Lline[-1][2]
    for Lline in Llines[1:]:
        new_geneID = Lline[-1][2]
        if old_geneID == new_geneID:
            Ltemp.append(Lline)
        else:
            Lgenelines.append(Ltemp)
            Ltemp = [Lline]
            old_geneID = new_geneID
    else:
        Lgenelines.append(Ltemp)
    # [print('sorted:', x) for x in Lgenelines[0]]
    fo = open(fopath, 'w')
    for Ltem in Lgenelines:
        Lwrite = []
        # [print('Ltem:', x) for x in Ltem]
        for Lline in Ltem:
            geneID = Lline[-1][3]
            # print(Lline)
            # print(Lwrite)
            if Lline[2] == 'gene':
                Lwrite += [prjname, geneID, Lline[0], Lline[3], Lline[4], Lline[6]]
                # print(Lwrite)
            if Lline[2] == 'CDS':
                Lwrite[1] = geneID.replace('cds', '').replace('CDS', '').strip('-_:')
                # print(Lwrite)
                fo.write('\t'.join(Lwrite) + '\n')
                break


def main():
    if len(sys.argv) == 4:
        fmain(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        fmain(sys.argv[1])


if __name__ == '__main__':
    main()
