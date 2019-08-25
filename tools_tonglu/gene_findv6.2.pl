#!/usr/bin/perl
use Cwd qw(getcwd);
use Getopt::Long;
my $useage=<<E;
****************************************************************************************************
version 6.2
auther  xw
perl gene_findv6.2.pl   -pep  <pep> -cds <cds> -objgenedir <dir>
--pep                    :目标物种的PEP序列，填写绝对路径，必填
--cds                    :目标物种的CDS序列，填写绝对路径，必填
--identity               :序列蛋白比对的相似性阀值，选填，默认50
--overlap                :序列蛋白比对的overlap阀值，选填，默认0.5
--Soverlap               :blast 到的目标基因的overlap，选填。默认 0
--evalue                 ：序列蛋白比对的E-value，选填，默认1e-5
--cscore                 ：采用最大score的一定百分比来过滤，如果定义此选项，identity 和 overlap 将不起作用，选填
--cutdomain              ：设置过滤时的结构域情况（ABCD），默认A。例如A,B,C,即筛选ABC  类型均符合条件
--union                  ：通过相似性，overlap 或者Cscore 筛选的基因与结构域完全一致的基因取并集。如不设置此选项默认取交集。
--genewise               ：是否采用genewise进行全基因搜索，如果填写，genome 和 gff 选项也要填。选填
--rpkm                   ：全部基因的rpkm值，用于画热图，选填
--anno                   ：全部基因的功能注释信息，用于提取筛选的基因功能注释。选填
--gff                    ：目标物种的gff文件，选填
--genome                 ：目标物种的全基因组fa文件，选填
--objgenedir             ：存放下载的目标基因的蛋白文件的文件夹，以fa结尾，必填
--peptree                ：是否生成构建蛋白树的脚本及准备文件，下列两个选项类似。选填
--cdstree                ：选填
--promotertree   ：选填
******************************************************************************************************

E
GetOptions("result=s"=>\$result,
"pep=s"=>\$pep,
"cds=s"=>\$cds,
"identity=s"=>\$identity,
"overlap=s"=>\$overlap,
"Soverlap=s"=>\$soverlap,
"evalue=s"=>\$evalue,
"cscore=s"=>\$Cscore,
"cutdomain=s"=>\$cutdomain,
"union+"=>\$union,
"genewise+"=>\$genewise,
"rpkm=s"=>\$rpkm,
"anno=s"=>\$anno,
"gff=s"=>\$gff,
"genome=s"=>\$genome,
"objgenedir=s"=>\$objgenedir,
"peptree+"=>\$peptree,
"cdstree+"=>\$cdstree,
"promotertree+"=>\$promotertree,
"help+"=>\$help,
);
if(defined $help){print  "$useage"; exit}
$identity||=50;
if (!defined $overlap  ){$overlap=0.5};
$soverlap||=0;
$evalue||=1e-5;
$result||=join('_',(split(/\s/,`date`))[1,2,3]);
#$result||='result';
$cutdomain='ABCD' if defined $union;
$cutdomain||='A';

my $flag=0;
my $dir=getcwd();
if (!defined $pep || !defined $cds ||!defined $objgenedir){ die "$useage\n pep,cds,objgenedir are must needed!!$!";}
if (! -d "${objgenedir}.$result"){mkdir "${objgenedir}.$result" or die "$!"; }
if(defined $genewise && (!defined $gff || !defined $genome)){die "$useage\n genewise error :file is not enough$!";} 
elsif(defined  $genewise ){open GW,">$dir/${objgenedir}.$result/genewise.sh" or die $!}
#my $rpkm=$ARGV[3];
#my $anno=$ARGV[4];
#my $gff=$ARGV[5];
#my $genome=$ARGV[6];
open O,">${objgenedir}.$result/blastall$result.sh";
unlink "${objgenedir}.$result/$result.xls";
system( "rm ${objgenedir}.$result/*pfam.out");
open T,">${objgenedir}.$result/$result.xls";
print T "file name\tquery gene\tsubject gene\tQoverlap\tSoverlap\tidentity\tScore\tQPFAM\tSPFAM\tA/B/C/D/E\tcds num\tcds length\tGO\tIntroPro\tSwissport\tKEGG\tTrembl\taa\tcds\n";
close T;
#open P,">pfamall.sh";
if (! -e "$pep.psd"){!system("sh /ifs/TJPROJ3/Plant/xuwei/qiangwei/flower/makeblastdb.sh  $pep") or die "$!";}
if(defined $genewise && ! -e "$genome.nsd"){!system("sh /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/testv5/makeblast.sh  $genome") or die "$!"}
my @redir=split /,/,$objgenedir;
my $se;
foreach my $i (@redir){if(!$se){$se=qr/$i/;}else{$se=qr/$se|$i/;}}
opendir  D,$dir or die $!;
while(readdir D)
{
next unless (/^$se$/);
#next unless (/ganyoushanzhi2/);
print $_,"\n";
opendir my $d ,"$dir/$_" or die $!;
my $d1="$dir/$_";
my $D=$_;
while(readdir $d){
next if /^[.]{1,2}$/;
print $_,"\n";
if(/.*\.fa$/i){
print O "cd  $dir/${objgenedir}.$result \n";
if (defined $genewise){
print GW "cd $dir/${objgenedir}.$result\n"; if (!-e "$dir/${objgenedir}.$result/$_.blastgenome.blast.solar.addlen.cov"){print GW "sh /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/testv5/run_blast.x.sh $genome   $d1/$_  $dir/${objgenedir}.$result/$_\n";}
print GW "sh /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tonglu/run_genewise.sh  $genome  $d1/$_ $_.blastgenome\n";
}
print O "sh  /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/testv5/runblastbest.x.sh  $d1/$_  $pep  $evalue ./$_\n";
print O "sh  /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/testv5/pfam.x.sh    $d1/$_   $_\n";
if(defined $Cscore){
print O "perl /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/testv5/filt.pl  $_.pep.$evalue.blast.solar.adLen.cor.best $overlap  $identity $soverlap  $Cscore >$_.IDtable\n";
}
else {
print O "perl /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/testv5/filt.pl  $_.pep.$evalue.blast.solar.adLen.cor.best $overlap  $identity $soverlap 0 >$_.IDtable\n";
}
print O "perl /TJPROJ1/DENOVO/PROJECT/xuwei/pangxie/geneblast/find_gene_from_fasta_by_ID.pl  $pep    $_.IDtable  $_.id.fast\n";
print O "perl /TJPROJ1/DENOVO/PROJECT/xuwei/pangxie/geneblast/find_gene_from_fasta_by_ID.pl  $cds    $_.IDtable  $_.id.cds.fast\n";
if(defined $union){
print O "perl  /TJPROJ1/DENOVO/PROJECT/xuwei/pangxie/geneblast/find_gene_from_fasta_by_ID_union.pl    $pep     $_.pep.$evalue.blast.solar.adLen.cor.best     $_.union.fast\n";
print O "perl  /TJPROJ1/DENOVO/PROJECT/xuwei/pangxie/geneblast/find_gene_from_fasta_by_ID_union.pl    $cds     $_.pep.$evalue.blast.solar.adLen.cor.best     $_.union.cds.fast\n";
print O "sh /TJPROJ1/DENOVO/PROJECT/xuwei/pangxie/geneblast/pfam.sh  $_.union.fast\n";
     if(defined $anno){
print O "perl /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/testv5/search5_union.pl  -query $_.pfa  -subj  $_.union.fast.pfa     -table  $_.IDtable -anno   $anno -result  $_  -blastf $_.pep.$evalue.blast.solar.adLen.cor.best -gff  $gff \n";
                     }
     else{
print O "perl /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/testv5/search5_union.pl  -query $_.pfa  -subj  $_.union.fast.pfa     -table  $_.IDtable   -result  $_  -blastf $_.pep.$evalue.blast.solar.adLen.cor.best  -gff  $gff \n";
         }
print O "perl   /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/testv5/find_gene_from_fasta_by_IDx.pl        $pep  $_.xls  $_.result_aa.fasta $cutdomain\n";
print O "perl   /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/testv5/find_gene_from_fasta_by_IDx.pl        $cds  $_.xls  $_.result_cds.fasta  $cutdomain\n";
     if (defined $gff &&  defined $genome){
$flag=1;
print O "python /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/promoter/promoter.py $gff $genome  $_.xls  >$_.result_promoter.fasta\n";
print O "perl /TJPROJ1/DENOVO/PROJECT/xuwei/pangxie/geneblast/merxls.pl $D/$_  $_.union.fast   $_.union.cds.fast  $_.xls $dir/${objgenedir}.$result/$result.xls $_.result_promoter.fasta\n";
        }
     else {
print O "perl /TJPROJ1/DENOVO/PROJECT/xuwei/pangxie/geneblast/merxls.pl $D/$_   $_.union.fast   $_.union.cds.fast  $_.xls $dir/${objgenedir}.$result/$result.xls\n";
       }
print O "perl /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/testv5/plotdomain.pl $_.union.fast_pfam.out    $_.result_aa.fasta   ${objgenedir}.$result\n";
}

else{
print O "sh /TJPROJ1/DENOVO/PROJECT/xuwei/pangxie/geneblast/pfam.sh  $_.id.fast\n";
      if(defined $anno){
print O "perl /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/testv5/search5.pl  -query $_.pfa  -subj  $_.id.fast.pfa     -table  $_.IDtable -anno   $anno -result  $_ -gff  $gff\n";
              } 
      else {
print O "perl /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/testv5/search5.pl  -query $_.pfa  -subj  $_.id.fast.pfa     -table  $_.IDtable   -result  $_ -gff  $gff\n";
           } 
print O "perl /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/testv5/find_gene_from_fasta_by_IDx.pl  $pep  $_.xls  $_.result_aa.fasta $cutdomain\n";
print O "perl /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/testv5/find_gene_from_fasta_by_IDx.pl  $cds  $_.xls  $_.result_cds.fasta $cutdomain \n";
     if (defined $gff &&  defined $genome){
$flag=1;
print O "python /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/promoter/promoter.py $gff $genome  $_.xls  >$_.result_promoter.fasta\n";
print O "perl /TJPROJ1/DENOVO/PROJECT/xuwei/pangxie/geneblast/merxls.pl $D/$_  $_.id.fast   $_.id.cds.fast  $_.xls $dir/${objgenedir}.$result/$result.xls  $_.result_promoter.fasta\n";
      }
     else {
print O "perl /TJPROJ1/DENOVO/PROJECT/xuwei/pangxie/geneblast/merxls.pl $D/$_   $_.id.fast   $_.id.cds.fast  $_.xls $dir/${objgenedir}.$result/$result.xls\n";
     }
print O "perl /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/testv5/plotdomain.pl $_.id.fast_pfam.out    $_.result_aa.fasta  ${objgenedir}.$result  \n";
}

#print O "mv  *pfam.out   *.pfa  *.fasta  *.blast  *.best       $dir/${objgenedir}.$result\n";
print O "rm  *.IDtable  *.fa.xls  *.solar *.cor  *.adLen  *.fast \n";
#print P "cd $d1\n";
next;
}

if(-d "$d1/$_")
{
my $dd1="$d1/$_";
my $D2="$D/$_";
opendir  my $dd ,"$dd1" or die $!;
while(readdir $dd)
{
print $_,"\n";
if(/.*fa$/i){
print O "cd $dd1\n";
print O "sh /TJPROJ1/DENOVO/PROJECT/xuwei/pangxie/geneblast/runblastbest.sh  $_\n";
print O  "sh /TJPROJ1/DENOVO/PROJECT/xuwei/pangxie/geneblast/pfam.sh  $_\n";
print O "perl /TJPROJ1/DENOVO/PROJECT/xuwei/pangxie/geneblast/filt.pl  $_.pep.e_5.blast.solar.adLen.cor.best  >$_.IDtable\n";
print O "perl /TJPROJ1/DENOVO/PROJECT/xuwei/pangxie/geneblast/find_gene_from_fasta_by_ID.pl  /TJPROJ1/DENOVO/PROJECT/xuwei/pangxie/geneblast/pep.fast $_.IDtable  $_.id.fast\n";
print O "sh /TJPROJ1/DENOVO/PROJECT/xuwei/pangxie/geneblast/pfam.sh  $_.id.fast\n";
print O "perl /TJPROJ1/DENOVO/PROJECT/xuwei/pangxie/geneblast/search.pl  $_.pfa  $_.id.fast.pfa  $_.IDtable /TJPROJ1/DENOVO/PROJECT/xuwei/pangxie/geneblast/Esi.function.xls  $_\n";
print O "perl /TJPROJ1/DENOVO/PROJECT/xuwei/pangxie/geneblast/find_gene_from_fasta_by_ID.pl /TJPROJ1/DENOVO/PROJECT/xuwei/ganshu/ref/NH160643_Ref_TR_result/gene/Itr.clean.pep.fa  $_.result  $_.result_aa.fasta\n";
print O "perl /TJPROJ1/DENOVO/PROJECT/xuwei/pangxie/geneblast/find_gene_from_fasta_by_ID.pl /TJPROJ1/DENOVO/PROJECT/xuwei/ganshu/ref/NH160643_Ref_TR_result/gene/Itr.clean.cds.fa  $_.result  $_.result_cds.fasta\n";
print O "perl /TJPROJ1/DENOVO/PROJECT/xuwei/pangxie/geneblast/merxls.pl $D2/$_ $_.result_aa.fasta $_.result_cds.fasta $_.result\n";
#print O "rm *.IDtable  *.cor *.adLen *.out *.stat *.solar *.log   *.fast *.pfa\n";
#print P "cd $dd1\n";
next;
}
}
}}
}


if(defined $genewise){
print GW "cat `ls $dir/${objgenedir}.$result/*genewise/nrResult/*.gff`  >$dir/${objgenedir}.$result/genewise.all.gff\n";
print GW "perl    /ifs/TJPROJ3/Plant/xuwei/BJpan/putao/addgene/Nob/search.pl   $dir/${objgenedir}.$result/genewise.all.gff  $gff >$dir/${objgenedir}.$result/novel.genewise.gff\n";
}
close O;
close GW;


chdir "${objgenedir}.$result";
system ("sh blastall$result.sh");
system("sh genewise.sh") if (defined $genewise);
#system (qq? perl -ane 'if(\$F[0]=~/\\/([A-Za-z0-9]+).*\\.fa/){print \"\$1_\$F[2]\\n\";}' $ARGV[0] |sort -u >unique_gene.list ?);
system (qq? perl -F"\\t" -ane 'if(\$F[0]=~/\\/([A-Za-z0-9\-]+).*\\.fa/ && (\$i=\$1) && "$cutdomain"=~/\$F[9]/i ){print \"\${i}_\$F[2]\\n\";}' $result.xls |sort -u >$result.list ?);
#print   qq? perl -F"\\t" -ane 'if(\$F[0]=~/\\/([A-Za-z0-9\-]+).*\\.fa/ && (\$i=\$1) && $cutdomain=~/\$F[9]/i ){print \"\${i}_\$F[2]\\n\";}' $result |sort -u >$result.list ?;
#system (qq? perl -F"\\t" -ane 'if(\$F[0]=~/\\/([A-Za-z0-9\-]+).*\\.fa/){print \"\$1_\$F[2]\\n\";}' $result |sort -u >$result.list ?);
system (qq? perl -F"\\t" -ane 'if(\$F[0]=~/\\/([A-Za-z0-9\-]+).*\\.fa/ && (\$i=\$1) && "$cutdomain"=~/\$F[9]/i ){print \"\${i}\\t\$F[1]\\t\$F[2]\\n\";}' $result.xls |sort -u >$result.listv2 ?);
if ( defined  $rpkm){
system ("perl /TJPROJ1/DENOVO/PROJECT/xuwei/ganshu/ref/NH160643_Ref_TR_result/test/tirpkm.pl  $rpkm  $dir/${objgenedir}.$result/$result.list  >$dir/${objgenedir}.$result/$result.rpkm");
system  ("/PUBLIC/software/RNA/R-3.1.2/R-3.1.2/bin/Rscript  /TJPROJ1/DENOVO/PROJECT/xuwei/walnut/sex/melon_form_cca/plot_cluster.R  $dir/${objgenedir}.$result/$result.rpkm");
system ("perl /TJPROJ1/DENOVO/PROJECT/xuwei/walnut/sex/melon_form_cca/cut_rpkm.pl   $dir/${objgenedir}.$result/$result.rpkm");
}
if (defined $peptree || defined $cdstree || defined $promotertree){
open TR,">$dir/${objgenedir}.$result/runtree.sh" or dir $!;
if ($peptree&& $cdstree==0 && $promotertree==0){ 
print TR "perl /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/pretree.pl -xls $dir/${objgenedir}.$result/$result.xls   -peptre  -flag $flag   -gene $dir/${objgenedir}.$result/$result.list  -flag $flag -dir $dir/$objgenedir\n";
}
elsif($peptree && $cdstree && $promotertree==0){
print TR "perl /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/pretree.pl -xls $dir/${objgenedir}.$result/$result.xls   -peptre   -cdstre   -flag $flag  -gene $dir/${objgenedir}.$result/$result.list  -flag $flag -dir $dir/$objgenedir\n";
}
elsif ($peptree && $cdstree && $promotertree){
print TR "perl /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/pretree.pl -xls $dir/${objgenedir}.$result/$result.xls   -peptre   -cdstre  -protre -flag $flag  -gene $dir/${objgenedir}.$result/$result.list  -flag $flag -dir $dir/$objgenedir\n";
}
elsif ($peptree==0 && $cdstree==0 && $promotertree){
print TR "perl /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/pretree.pl -xls $dir/${objgenedir}.$result/$result.xls    -protre -flag $flag  -gene $dir/${objgenedir}.$result/$result.list  -flag $flag -dir $dir/$objgenedir\n";
}
elsif ($peptree==0 && $cdstree && $promotertree==0){
print TR "perl /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/pretree.pl -xls $dir/${objgenedir}.$result/$result.xls    -cdstree -flag $flag  -gene $dir/${objgenedir}.$result/$result.list  -flag $flag -dir $dir/$objgenedir\n";
}
elsif($peptree && $cdstree==0 && $promotertree){
print TR "perl /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/pretree.pl -xls $dir/${objgenedir}.$result/$result.xls    -cdstree -protre -flag $flag  -gene $dir/${objgenedir}.$result/$result.list  -flag $flag -dir $dir/$objgenedir\n";
}
else {die  "ERROR$!";}
system("sh  $dir/${objgenedir}.$result/runtree.sh");
}
chdir($dir);
