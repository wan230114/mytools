# @Author: ChenJun
# @Date:   2019-01-08 16:45:00
# @Last Modified by:   JUN
# @Last Modified time: 2019-01-17 13:04:37

name=%s
datapath=%s
reffa=%s
softBedtools=%s
softBlast=%s

# cp allstep.00.sh.log.bak allstep.00.sh.log.bak2 &>/dev/null
# cp allstep.00.sh.log allstep.00.sh.log.bak &>/dev/null
# >allstep.00.sh.log


# # 01.run_getBedSeq.sh    # v=0.1g,p=0
# # ********************************************************************************
# ln -s $datapath/Novel_sequence/all.chain.filter.tnet.synnet.axt.tp.bed.merge.unmap tar.bed &>/dev/null
# ln -s $datapath/index/tar.fa tar.fa &>/dev/null
# echo `date +%%F'  '%%H:%%M:%%S` '00 all start.' &>>allstep.00.sh.log
# python3 $softBedtools/01.runExtrct_BedSeq.py tar.bed tar.fa tar_BedSeq.fa
# echo `date +%%F'  '%%H:%%M:%%S` '00 getd tar_BedSeq.fa.' >>allstep.00.sh.log


# # run_blast.sh
# # ********************************************************************************
# ln -s $reffa ref.fa &>/dev/null

# target=ref.fa
# query=tar_BedSeq.fa
# echo `date +%%F'  '%%H:%%M:%%S` '01 blast start' >>allstep.00.sh.log
# $softBlast/formatdb -i $target -p F
# $softBlast/blastall -i $query -d $target -p blastn -e 1e-20 -a 20 -F F -m 8 -o $name.blast  &&\
# echo `date +%%F'  '%%H:%%M:%%S` '01 blast success.' >>allstep.00.sh.log
echo `date +%%F'  '%%H:%%M:%%S` '02 get bed start.' >>allstep.00.sh.log
python3 $softBedtools/03.bed_link.py $name.blast $name.blast.bed &&\
echo `date +%%F'  '%%H:%%M:%%S` '02 get bed success.' >>allstep.00.sh.log


# run_bedtools.sh
# ********************************************************************************
ln -s $datapath/Novel_sequence/novel_gene.gff3 ref.bed.gff3 &>/dev/null
awk '{print $1"\t"$4"\t"$5}' ref.bed.gff3 > ref.bed

tarbed=$name.blast.bed
refbed=ref.bed
echo `date +%%F'  '%%H:%%M:%%S` '03 get resultbed start.' >>allstep.00.sh.log
source /home/likui/.bashrc
bedtools subtract -a $tarbed -b $refbed >result_$name.bed  &&\
echo `date +%%F'  '%%H:%%M:%%S` '03 geted resultbed success.' >>allstep.00.sh.log

# echo `date +%%F'  '%%H:%%M:%%S` '03 bed_sort start.' >>allstep.00.sh.log
# python3 $softBedtools/03.bedsort.py result_$name.bed result_$name.bed.sort &&\
# echo `date +%%F'  '%%H:%%M:%%S` '03 bed_sort success.' >>allstep.00.sh.log
