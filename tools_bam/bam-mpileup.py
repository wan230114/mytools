#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# @ Author: Chen Jun
# @ Author Email: 1170101471@qq.com
# @ Created Date: 2023-12-11, 18:04:44
# @ Modified By: Chen Jun
# @ Last Modified: 2023-12-12, 11:34:03
#############################################


import os,sys
# import argparse
import logging
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s %(levelname)s] - %(message)s'
                    )

if len(sys.argv)>1:
    bam,ref,regin=sys.argv[1],sys.argv[2],sys.argv[3]
else:
    bam="630621-1005-PCRNGS-sorted.bam"
    ref="/mfs1/gene/nuclear/GRCh37.fasta"
    regin="chr20:57484420-57484420"

pileupout = f"{bam}.{regin.replace(':', '-')}.pileup"
if not os.path.exists(bam+".bai"):
    os.system(f"samtools index {bam}")
os.system(f"""echo "samtools mpileup -aa -A --max-depth 0 -q 0 --ff 0 -Q 0 -r {regin}  -f {ref} {bam} -o {pileupout}" | bash -x""")

sample = os.path.basename(bam)

def count_bases(pileup_file):
    if os.path.exists(pileup_file):
        with open(pileup_file) as f:
            for line in f:
                fields = line.strip().split()
                pos = int(fields[1])
                ref_base = fields[2].upper()
                total = int(fields[3])
                bases = fields[4].upper()
                counts = {'A': bases.count('A'), 'C': bases.count('C'),
                        'G': bases.count('G'), 'T': bases.count('T')}
                counts.update({ref_base: bases.count(".") + bases.count(",")})
                # total = sum(counts.values())
                if total > 0:
                    proportions = {base: "%.4f (%s)"%(count / total * 100, count)
                                for base, count in counts.items()}
                else:
                    proportions = {base: 0 for base in counts.keys()}
                print(f'Sample: {sample}, Position: {fields[0]}:{pos}, Ref: {ref_base}, Total: {total}, Proportions: {proportions}')
                print(f'{sample}\t{fields[0]}:{pos}\t{ref_base}\t{total}\t{proportions}', file=open(pileup_file+".tsv", "w"))
    else:
        Chr=regin.split(":")[0]
        pos_a, pos_b = regin.split(":")[1].split("-")
        for pos in range(int(pos_a),int(pos_b)+1):
            print(f'Sample: {sample}, Position: {Chr}:{pos}, Ref: NA, Total: NA, Proportions: NA')
            print(f'{sample}\t{Chr}:{pos}\tNA\tNA\tNA', file=open(pileup_file+".tsv", "w"))

count_bases(f'{pileupout}')
