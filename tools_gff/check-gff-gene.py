# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2018-12-05 17:15:54
# @Last Modified by:   JUN
# @Last Modified time: 2018-12-05 17:35:32

# 本函数用于检测是否有相邻基因的存在，若有则输出到新文件：原文件+.err


def main(finame):
    foname = finame + '.err'
    fi = open(finame)
    fo = open(foname,'w')
    Nrow = 0  # 行数
    while True:
        line = fi.readline()
        Nrow+=1
        if not line:
            break
        elif line.startswith("#"):
            continue
        Lline = line.strip().split('\t')
        if Lline[2] == 'gene':
            line = fi.readline()
            Nrow+=1
            Lline = line.strip().split('\t')
            if Lline[2] == 'gene':
                fo.write(str(Nrow)+'\n'+line+'\n')

    fi.close()
    fo.close()

if __name__ == "__main__":
    for line in open("check.list"):
        main(line.strip())
