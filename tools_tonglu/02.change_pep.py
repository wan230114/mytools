# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2018-12-25 17:56:50
# @Last Modified by:   JUN
# @Last Modified time: 2019-03-14 11:33:55

# 此版本可以备份.pep为.pep.bak，因加入跳过.bak，可多次重复执行

import os
import sys
import shutil


def fmain(prjname):
    print("已进入" + prjname + '/gene.result.xls/tree/pep')
    os.chdir(prjname + '/gene.result.xls/tree/pep')
    L_files = os.listdir('.')
    L_files_pep = [x for x in L_files if x.endswith('.pep')]
    L_files_pep_bak = [x.rstrip('.bak') for x in L_files if x.endswith('.pep.bak')]
    L = list(set(L_files_pep) - set(L_files_pep_bak))
    for pep0 in L:
        # 构建pep文件列表准备写入pep
        with open('../../%s.fa.result_aa.fasta' % pep0.rstrip('.tre.pep')) as fi2:
            Ldata = fi2.read().split()
            # print(Ldata)
            # print(Ldata)
            Lnewdata = []
            i = 0
            i_max = len(Ldata) - 1
            linetmp = ''
            Lnewdata.append(Ldata[i])
            while True:
                i += 1
                if i > i_max:
                    break
                if Ldata[i].startswith('>'):
                    linetmp = linetmp[:-1]
                    Lnewdata.append(linetmp)
                    Lnewdata.append(Ldata[i])
                    linetmp = ''
                else:
                    linetmp += Ldata[i]
            linetmp = linetmp[:-1]
            Lnewdata.append(linetmp)
        # print(Lnewdata)
        # 读取前两行准备重新写入pep文件
        # with open(pep0) as fi:
        shutil.copy(pep0, pep0 + '.bak')
        with open(pep0 + '.bak') as fi:
            Ldatas = fi.read().split()
            Ldata = []
            i = -2
            # print(Ldatas)
            while True:
                i += 2
                try:
                    if Ldatas[i + 1].startswith('>'):
                        break
                except IndexError:
                    break
                Ldata.append(Ldatas[i])
                Ldata.append(Ldatas[i + 1])
            Ldata = [x.replace(':', '_') for x in Ldata]
            Ldata = [x.replace('|', '_') for x in Ldata]
            Ldata = [x.replace('*', '') for x in Ldata]
            # print(Ldata, Lnewdata)
        with open(pep0, 'w') as fo:
            fo.write('\n'.join(Ldata + Lnewdata))
        print('已成功写入' + pep0)
    os.chdir('../../../../')


def main():
    # sys.argv = ['', 'Pcui']
    prjname = sys.argv[1]
    fmain(prjname)


if __name__ == '__main__':
    main()
