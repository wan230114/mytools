#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# @ Author: Chen Jun
# @ Author Email: 1170101471@qq.com
# @ Created Date: 2023-03-06, 11:42:47
# @ Modified By: Chen Jun
# @ Last Modified: 2023-12-01, 11:41:17
#############################################

# %%

from Bio import SeqIO
import re
import sys

# from Bio.Seq import Seq
# my_dna = Seq("AGTANNNCACTGGTN")
# my_dna.find("N")
# for x in re.compile("N+").finditer(str(my_dna)):
#     a, b = x.span()

# fasta = "/home/chenjun/gitlab/bam_to_freebayes/ref/high-homologous-genes.fa"
fasta = sys.argv[1]

for record in SeqIO.parse(fasta, "fasta"):
    # print(record.id, len(record.seq))
    for x in re.compile("N+").finditer(str(record.seq)):
        a, b = x.span()
        print(record.id, a, b, sep="\t")
