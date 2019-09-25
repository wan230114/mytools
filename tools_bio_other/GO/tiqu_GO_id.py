# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun2049@foxmail.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-09-25 10:37:31
# @Last Modified by:   JUN
# @Last Modified time: 2019-09-25 10:52:33


# 提取GO_id

import sys
import re


def fmain(finame, foname):
    with open(finame) as fi, open(foname, 'w') as fo:
        fi.readline()  # 丢弃表头
        for line in fi:
            geneID = line.split('\t', 1)[0]
            L_GO = re.findall('\((GO:.*?)\)', line)
            fo.write('\t'.join([geneID] + L_GO) + '\n')


def main():
    # sys.argv = ['', 'GO_anno.txt', 'GO_anno.txt2']
    finame, foname = sys.argv[1:3]  # 输入，输出
    fmain(finame, foname)


if __name__ == '__main__':
    main()
