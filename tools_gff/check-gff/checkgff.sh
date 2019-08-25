#2）gff3修改
#表头、第三列、第八列、第九列存在的格式问题较多，以下为对几列内容进行更改的参考脚本：
#a.	若CDS区第八列没有phase信息，可用下述脚本进行修改填充：
#Perl /PUBLIC/software/RESEQ/Pipeline/current/BSA/QTLseq_TopV1Test/00.bin/GFF/check/buqi.gff.cds.pl -in gff3file -out newfile
#b.	检测注释文件（gff3）中的基本错误
perl /PUBLIC/software/RESEQ/Pipeline/current/BSA/QTLseq_TopV1Test/00.bin /GFF/check/gff_filter-v0.pl  \
-in input.gff3 \
-out cherked.gff3 \
-err err.gff3
#c.	利用gtf、pep、fa文件生成gff3文件（适用于ensemble网站下载文件格式）
/PUBLIC/software/RESEQ/Pipeline/current/BSA/QTLseq_TopV1Test/00.bin/GFF/gtf2gff.sh
sh  ensembl-pipeline.sh  gtf/gtf.gz  genome.fa.gz  pep.gz
#在生成注释库的时候，可能会因为gff3中某一行的大写或小写报错，则需要根据报错信息针对性修改。
