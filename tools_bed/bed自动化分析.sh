run-workdir
    Sample1
        01.tiqu/
        02.blast/
        03.bedtools/
    Sample2
        01.tiqu/
        02.blast/
        03.bedtools/
    Sample3
        01.tiqu/
        02.blast/
        03.bedtools/
    00.sh
    runAllstart.sh
01.list.txt
02.softpath.txt
getPipe.sh



********************************************************************************
01.list.txt
********************************************************************************
Pdul
/TJNAS01/PAG/Plant/zihailing/P101SC16120962_pear/Pdul
Pnan
/TJNAS01/PAG/Plant/zihailing/P101SC16120962_pear/Pnan
Pcui
/ifs/TJPROJ3/Plant/zihailing/project/P101SC16120962_pear/Variation_calling/Pcui
Phai
/ifs/TJPROJ3/Plant/zihailing/project/P101SC16120962_pear/Variation_calling/Phai
Phei
/ifs/TJPROJ3/Plant/zihailing/project/P101SC16120962_pear/Variation_calling/Phei
Pkue
/ifs/TJPROJ3/Plant/zihailing/project/P101SC16120962_pear/Variation_calling/Pkue
Ptia
/ifs/TJPROJ3/Plant/zihailing/project/P101SC16120962_pear/Variation_calling/Ptia
Pzao
/ifs/TJPROJ3/Plant/zihailing/project/P101SC16120962_pear/Variation_calling/Pzao
********************************************************************************

********************************************************************************
02.softpath.txt
********************************************************************************
path_bedtools=/ifs/TJPROJ3/Plant/chenjun/mytools/tools_bed
path_blast=/PUBLIC/software/public/Alignment/blast-2.2.26/bin
********************************************************************************

********************************************************************************
getPipe.sh
********************************************************************************
python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_bed/bed2bed.py 01.list.xls 02.softpath.txt 
********************************************************************************

********************************************************************************
runAllstart.sh
********************************************************************************

********************************************************************************

01.tiqu
********************************************************************************
01.run_getBedSeq.sh    # v=0.1g,p=0
********************************************************************************
bed=%s/Novel_sequence/all.chain.filter.tnet.synnet.axt.tp.bed.merge.unmap
fa=%s/index/tar.fa
name=%s
ln -s $bed input.bed
ln -s $fa input.fa
python3 %s/01.runExtrct_BedSeq.py input.bed input.fa result.fa
********************************************************************************


02.blast/
    -a 5 
    #大约一个任务需要5cpu,1.7g的资源
    qsub -cwd -l vf=1.8g,p=5 run_blast.sh
    -a 1 默认
    qsub -cwd -l vf=0.5g,p=1 run_blast.sh
    -a 30 
    #大约一个任务需要30cpu,12g的资源
    qsub -cwd -l vf=1.8g,p=5 run_blast.sh
********************************************************************************
run_blast.sh
********************************************************************************
target=00.result.fa
query=00.ref.fa
name=%s

ln -s ../01.tiqu/00.result.fa
ln -s ../index/00.ref.fa
cp run_blast.sh.log.bak run_blast.sh.log.bak2
cp run_blast.sh.log run_blast.sh.log.bak
>run_blast.sh.log

echo `date +%%F'  '%%H:%%M:%%S` '00 all start' >>run_blast.sh.log
%s/formatdb -i $target -p F
%s/blastall -i $query -d $target -p blastn -e 1e-20 -a 30 -F F -m 8 -o $name.blast   &&\
echo `date +%%F'  '%%H:%%M:%%S` '01 blast over' >>run_blast.sh.log

echo `date +%%F'  '%%H:%%M:%%S` '02 geted bed satrt' >>run_blast.sh.log
awk '{print $2"\t"$7"\t"$8}' $name.blast > $name.blast.bed.tmp
python3 %s/02.getbedForBlast.py $name.blast.bed.tmp $name.blast.bed
echo `date +%%F'  '%%H:%%M:%%S` '02 geted bed over' >>run_blast.sh.log
********************************************************************************

03.bedtools/
********************************************************************************
run_bedtools.sh
********************************************************************************
tarbed=Sec.blast.bed
refbed=novel_gene.gff3.bed

awk '{print $1"\t"$4"\t"$5}' novel_gene.gff3.bed > novel_gene.gff3
source /home/likui/.bashrc
bedtools subtract -a $tarbed -b $refbed >result.bed

********************************************************************************



# ********************************************************************************
# run02_bed.sh
# ********************************************************************************
# name=%s

# perl /TJPROJ1/DENOVO/PROJ1/ceshi/solar.pl -a bac2bac -f m8 $name.blast >$name.blast.solar   &&\
# echo `date +%%F'  '%%H:%%M:%%S` '02 blast.solar over' >>run_blast.sh.log

# perl /TJPROJ1/DENOVO/PROJ1/ceshi/solar_add_realLen.pl $name.blast.solar $target $query >$name.blast.solar.addlen   &&\
# echo `date +%%F'  '%%H:%%M:%%S` '03 blast.solar.addlen over' >>run_blast.sh.log

# perl /TJPROJ1/DENOVO/PROJ1/ceshi/solar_add_identity.pl --solar $name.blast.solar.addlen --m8 $name.blast >$name.blast.solar.addlen.cov   &&\
# echo `date +%%F'  '%%H:%%M:%%S` '04 blast.solar.addlen.cov over' >>run_blast.sh.log
# ********************************************************************************


