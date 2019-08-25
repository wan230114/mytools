# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-03-15 14:19:03
# @Last Modified by:   JUN
# @Last Modified time: 2019-05-07 00:59:48


import os
import sys


def fmain(prjname, wuzhong):
    D = {}
    with open('list/' + wuzhong + '_list.txt') as fi:
        for line in fi:
            Lline = line.strip().split('\t')
            D[Lline[1].replace('_',' ')] = Lline[2]
    Lfile = os.popen('ls out_svg/%s_%s_RAxML_bestTree.*.tre.pep.tre.svg' %
                     (prjname, wuzhong)).read().split()
    for fname in Lfile:
        with open(fname) as fi:
            s = fi.read()
        with open(fname + '-chr.svg', 'w') as fo:
            p = 0
            for key in D:
                if key in s:
                    s = s.replace(key.replace('_', ' '), '%s（%s）' % (key, D[key]))
                    p = 1
            if p == 0:
                print('list文件中未找到key，D:', D)                
            fo.write(s)


def main():
    prjname = sys.argv[1]
    Lfile = sorted([x.replace("_list.txt","") for x in os.listdir('list')])
    for wuzhong in Lfile:
        print(prjname, wuzhong)
        fmain(prjname, wuzhong)
        print('[ok]', wuzhong)


if __name__ == '__main__':
    main()
