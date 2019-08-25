# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-02-18 14:33:19
# @Last Modified by:   JUN
# @Last Modified time: 2019-03-21 20:46:36

import os
import sys


def fmain(path, flist):
    with open(flist) as fi:
        L = [line.strip() for line in fi]
        # ['Mdom', 'Pcui', 'Pdan', 'Pdul', 'Phai', 'Phei', 'Pkue', 'Pnan', 'Ptia', 'Pzao']
    for wuzhong in L:
        print('%s/%s/gene.result.xls/tree/pep' % (path, wuzhong))
        os.system(
            '''cd %s/%s/gene.result.xls/tree/pep;find ./ -type l|xargs rm; rm xiufu -r''' % (path, wuzhong))
        os.system(
            '''cd %s/%s/gene.result.xls/tree/pep;mkdir xiufu;cd xiufu; \
            ls ..|grep -e .tre.pep$|xargs -i ln -s ../{};\
            ls ../RAxML_bestTree.*.tre.pep.tre|\
            sed 's#^../RAxML_bestTree.##'|\
            sed 's#.tre.pep.tre$##'|xargs -i rm {}.tre.pep;\
            sh %s/run.sh''' % (path, wuzhong, sys.path[0]))


def main():
    path, flist = sys.argv[1:3]
    fmain(path, flist)


if __name__ == '__main__':
    main()
