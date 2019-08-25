# -*- coding: utf-8 -*-
# @Author: JUN
# @Date:   2018-10-30 11:32:40
# @Last Modified by:   JUN
# @Last Modified time: 2018-10-30 16:14:39

import sys


def fclean(Largv):
    fname, fname_new = Largv[1:]
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
                        

if __name__ == "__main__":
    sys.argv = ['', "gene_models_20170612.gff3", "gene_models_20170612.gff3.clean"]
    fclean(sys.argv)
