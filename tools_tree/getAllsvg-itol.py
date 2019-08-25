# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-22 16:32:01
# @Last Modified by:   JUN
# @Last Modified time: 2019-05-07 03:15:08

import os
import sys
import re
import traceback
from multiprocessing import Pool
sys.path.append('/ifs/TJPROJ3/Plant/chenjun/mytools/tools_tree')
from itol import itol
import getTree_fromFile


def getinfo_list(Lpath, L_all, L_cankao, Lfilter,  name_tonglu, name_sample, name_Gene):
    # 给挑选的基因填充信息
    try:
        D_xls = {}
        fi_list = open('/'.join(Lpath[:4]) + '/result.xls.xls', 'r')
    except Exception:  # 因为只有两种，懒得用模式匹配了
        fi_list = open('/'.join(Lpath[:4]) + '/result.xls_lk.xls', 'r')
    fi_list.readline()
    for line in fi_list:
        Lline = line.split()
        Lline = [x.strip() for x in Lline]
        D_xls[Lline[2]] = Lline[8]
    try:
        Dlist = {}
        with open('list/%s_list.txt' % name_sample, 'r') as fi:
            for line in fi:
                Lline = line.strip().split('\t')
                Dlist[Lline[1]] = Lline[2:]
        for gene_ID in Lfilter:
            Dlist_L = Dlist.get(gene_ID, ['.'] * 4)
            with open('result.txt', 'a') as fo:
                fo.write('\t'.join([name_tonglu, name_sample, name_Gene,
                                    gene_ID, D_xls[gene_ID],
                                    Dlist_L[0], Dlist_L[1],
                                    Dlist_L[2], Dlist_L[3]]) + '\n')

        for gene_ID in (set(L_all) - set(L_cankao)):
            Dlist_L = Dlist.get(gene_ID, ['.'] * 4)
            with open('result_all.txt', 'a') as fo:
                fo.write('\t'.join([name_tonglu, name_sample, name_Gene,
                                    gene_ID, D_xls[gene_ID],
                                    Dlist_L[0], Dlist_L[1],
                                    Dlist_L[2], Dlist_L[3]]) + '\n')
    except Exception:
        print('list文件不存在')


def fmain(filepath2, mod, Lgene, filepath, name_tonglu, name_sample, name_Gene):
    """
    输入：./3.shanlichun/Pzao/gene.result.xls/tree/pep/
    标准输出：找到的参考的gene
    """
    try:
        L_all, L_cankao, Lfilter = getTree_fromFile.fmain(filepath2, mod, Lgene)
        Lpath = filepath.split('/')
        getinfo_list(Lpath, L_all, L_cankao, Lfilter,  name_tonglu, name_sample, name_Gene)
    except KeyboardInterrupt:
        print('运行终止！')
        sys.exit(1)
    except Exception:
        traceback.print_exc()
        sys.exit(1)


def main():
    prjname, genelist = sys.argv[1:]
    try:
        os.mkdir('out_svg')
    except Exception:
        print('文件夹已存在')
    open('result.txt', 'w').close()
    open('result_all.txt', 'w').close()
    with open(genelist) as fi:
        Lgene = [line.strip() for line in fi if line.strip()]
    p = Pool(10)
    for path, Ldic, Lfile in os.walk('./' + prjname, followlinks=True):
        if '/tree/pep' in path:
            Lfile = [x for x in Lfile if 'bestTree' in x]
            for file in Lfile:
                # RAxML_bestTree.refPzao.tre.pep.tre
                filepath = path + '/' + file
                name_tonglu, name_sample, name_Gene = filepath.split('/')[1:3] + [
                    file.replace('RAxML_bestTree.', '').replace('.tre.pep.tre', '')]
                filepath2 = 'out_svg/%s_%s_%s' % (name_tonglu, name_sample, file)

                os.system('cp %s %s' % (filepath, filepath2))
                os.system('cp %s %s' % (filepath.replace('_bestTree.', '_bipartitionsBranchLabels.'),
                                        filepath2.replace('_bestTree.', '_bipartitionsBranchLabels.')))

                p.apply_async(fmain, args=(filepath2, 'f', Lgene, filepath,
                                           name_tonglu, name_sample, name_Gene))
                # fmain(filepath2, 'f', Lgene)
    p.close()
    p.join()


if __name__ == '__main__':
    main()
    # fmain('./3.shanlichun/Pzao/gene.result.xls/tree/pep/RAxML_bestTree.A6PR.tre.pep.tre')
    # fmain('./3.shanlichun/Pnan/gene.result.xls/tree/pep/RAxML_bestTree.SUCSUT.tre.pep.tre')
    # 运行太久了，可以探索一下why
    # fmain('./1.muzhisu/Mdom/gene.result.xls_lk/tree/pep/RAxML_bipartitions.4CL.tre.pep.tre')
    # fmain('./3.shanlichun/Ptia/gene.result.xls/tree/pep/RAxML_bestTree.SDH.tre.pep.tre')
