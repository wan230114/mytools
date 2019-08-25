# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2018-12-04 11:22:08
# @Last Modified by:   JUN
# @Last Modified time: 2018-12-04 11:47:32

# 将长读数序列按每行80个碱基格式化输出

import sys
import re


def cut_text(text, lenth):
    textArr = re.findall('.{' + str(lenth) + '}', text)
    textArr.append(text[(len(textArr) * lenth):])
    return textArr


def fmain(finame, foname, n_length):
    fi = open(finame)
    fo = open(foname, "w")
    for line in fi:
        line = line.rstrip()
        Lline = [line]
        if not line.startswith('>'):
            Lline = cut_text(line, n_length)
        fo.write('\n'.join(Lline) + '\n')

if __name__ == "__main__":
    Largv = sys.argv
    # finame = Largv[1]
    finame = "fasta_format80.fa"
    foname = finame + '.new'
    n_length = 80
    fmain(finame, foname, n_length)
