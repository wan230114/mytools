#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# @ Author: Chen Jun
# @ Author Email: 1170101471@qq.com
# @ Created Date: 2020-11-19, 09:41:10
# @ Modified By: Chen Jun
# @ Last Modified: 2021-11-22, 17:33:05
#############################################

# Version： v1.1
#  v1.0 基本功能完成
#  v1.1 修正正则表达式，使得 MapGeneID Bug 修复

# https://biopython-cn.readthedocs.io/zh_CN/latest/cn/chr09.html

# %%
import sys
import re
import time

from Bio import Entrez
Entrez.email = "1170101471@qq.com"

# %%


def do(NM, fo=sys.stdout):
    # 搜索
    def run(NM):
        handle = Entrez.esearch(db="nuccore", term=NM)
        record = Entrez.read(handle)
        id = record["IdList"]  # 1787392285
        handle = Entrez.esummary(db="nuccore", id=id)
        return Entrez.read(handle)
    while True:
        try:
            res = run(NM)
            res_title = res[0]["Title"]
            break
        except Exception as e:
            print("ERRO:", e)
            time.sleep(1)
    # Homo sapiens fucosyltransferase 1 (H blood group) (FUT1), transcript variant 1, mRNA
    # Homo sapiens killer cell immunoglobulin like receptor, three Ig domains and long cytoplasmic tail 1 (KIR3DL1), transcript variant 1 (reference allele), mRNA
    # NM_001013907    Hsp40) member B12 (Dnajb12      Rattus norvegicus DnaJ heat shock protein family (Hsp40) member B12 (Dnajb12), mRNA
    # res_title_id = re.findall(r"\((.*?)\)", res_title)
    res_title_id = re.findall(
        r".*\((.*?)\)(?:, transcript variant |, .*mRNA)",
        res_title)
    if res_title_id:
        # res_all = NM, res_title_id[-1], res_title
        res_all = NM, res_title_id[0], res_title
    else:
        res_all = NM, ".", res_title
    print(*res_all, sep="\t", file=fo)
    fo.flush()
    return res_all


def main():
    finame = sys.argv[1]
    foname = open(sys.argv[2], "w") if len(sys.argv) == 3 else sys.stdout
    with open(finame) as fi:
        Llines = fi.readlines()
        LEN_Llines = len(Llines)
        for i, line in enumerate(Llines):
            NM = line.strip()
            print(i, "%.3f%%" % (i/LEN_Llines*100), NM, file=sys.stderr)
            do(NM, foname)


if __name__ == "__main__":
    main()
