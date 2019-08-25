# @Author: ChenJun
# @Date:   2019-01-08 16:45:00
# @Last Modified by:   JUN
# @Last Modified time: 2019-01-11 14:17:12

name=Pzao
reffa=/ifs/TJPROJ3/Plant/zihailing/project/P101SC16120962_pear/Variation_calling/Pzao
datapath=/ifs/TJPROJ3/Plant/zihailing/project/P101SC16120962_pear/Variation_calling/00.genomes/Pdan.genome.fa
softBedtools=/ifs/TJPROJ3/Plant/chenjun/mytools/tools_bed
softBlast=/PUBLIC/software/public/Alignment/blast-2.2.26/bin

cp allstart.00.sh.log.bak allstart.00.sh.log.bak2 &>/dev/null
cp allstart.00.sh.log allstart.00.sh.log.bak &>/dev/null
>allstart.00.sh.log

# 01.run_getBedSeq.sh    # v=0.1g,p=0
# ********************************************************************************
ln -s $datapath/Novel_sequence/all.chain.filter.tnet.synnet.axt.tp.bed.merge.unmap tar.bed &>/dev/null
ln -s $datapath/index/tar.fa tar.fa &>/dev/null

echo `date +%F'  '%H:%M:%S` '00 all start' &>>allstart.00.sh.log
python3 $softBedtools/01.runExtrct_BedSeq.py tar.bed tar.fa tar_BedSeq.fa  &&\
echo `date +%F'  '%H:%M:%S` '00 getd tar_BedSeq.fa' >>allstart.00.sh.log



# run_blast.sh
# ********************************************************************************
ln -s $datapath/index/ref.fa ref.fa &>/dev/null

target=tar_BedSeq.fa
query=$reffa

echo `date +%F'  '%H:%M:%S` '01 blast start' >>allstart.00.sh.log
$softBlast/formatdb -i $target -p F
$softBlast/blastall -i $query -d $target -p blastn -e 1e-20 -a 20 -F F -m 8 -o $name.blast  &&\
echo `date +%F'  '%H:%M:%S` '01 blast over' >>allstart.00.sh.log

echo `date +%F'  '%H:%M:%S` '02 get bed satrt' >>allstart.00.sh.log
awk '{print $2"\t"$7"\t"$8}' $name.blast > $name.blast.bed.tmp
python3 $softBedtools/02.getbedFromBlast.py $name.blast.bed.tmp $name.blast.bed  &&\
echo `date +%F'  '%H:%M:%S` '02 get bed over' >>allstart.00.sh.log



# run_bedtools.sh
# ********************************************************************************
ln -s $datapath/Novel_sequence/novel_gene.gff3 ref.bed.gff3 &>/dev/null
awk '{print $1"\t"$4"\t"$5}' ref.bed.gff3 > ref.bed

tarbed=$name.blast.bed
refbed=ref.bed

echo `date +%F'  '%H:%M:%S` '03 get resultbed satrt' >>allstart.00.sh.log
source /home/likui/.bashrc
bedtools subtract -a $tarbed -b $refbed >result_$name.bed  &&\
echo `date +%F'  '%H:%M:%S` '02 geted resultbed over' >>allstart.00.sh.log
