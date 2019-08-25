#!/bin/bash
#########################################################################
# File Name: run.sh
# Author: wangguifang
# mail: wangguifang@novogene.com
# Created Time: 2018年05月15日 星期二 10时33分26秒
#########################################################################

perl /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tonglu/gene_findv6.2.pl \
-identity 30 \
-overlap 0.2 \
-Soverlap 0.2 \
-objgenedir gene  \
-evalue 1e-3  \
-result result.xls \
-pep %s  \
-cds %s  \
--genewise \
--genome  %s \
--gff %s \
--peptree \
--cdstree
