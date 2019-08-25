name=$2.blastgenome
genome=$1
pep=$2
name2=$3

#	awk '$5>=0.7 && $13>=60{print}' $name.blast.solar.addlen.cov >$name.blast.solar.addlen.cov.filter
        perl /ifs/TJPROJ3/Plant/xuwei/BJpan/putao/12xv2/new_all.genewise2/pickcscore.pl  $name2.blast.solar.addlen.cov  >$name2.blast.solar.addlen.cov.filter
	perl  /ifs/TJPROJ3/Plant/xuwei/yanfa/genewise_pipeline/get_pos.pl $name2.blast.solar.addlen.cov.filter >$name2.blast.solar.addlen.cov.filter.pos
	awk '{print $1 "  "$3}' $name2.blast.solar.addlen.cov.filter.pos >$name2.blast.solar.addlen.cov.filter.pos.strandList

	mkdir $name2.genewise

	perl  /ifs/TJPROJ3/Plant/xuwei/yanfa/genewise_pipeline/v2/extract_sequence.pl  --pos $name2.blast.solar.addlen.cov.filter.pos --fasta $genome --extent 5000 >$name2.genewise/$name2.nuc
	perl  /ifs/TJPROJ3/Plant/xuwei/yanfa/genewise_pipeline/prepare_pep.pl $name2.blast.solar.addlen.cov.filter.pos $pep >$name2.genewise/$name2.pep
	perl /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/testv5/call_genewise.pl --pep $name2.genewise/$name2.pep --nuc $name2.genewise/$name2.nuc --list $name2.blast.solar.addlen.cov.filter.pos.strandList --key $name2 --out $name2.genewise/ --num 1


	cd $name2.genewise
	cat ./result/*.gw >$name2.gw
	perl  /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/testv5/gw_parser.pl --gw $name2.gw --pep $name2.pep --ac 0 --id 0 --type 1 >$name2.gw.alg
	perl  /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/testv5/gw_parser.pl --gw $name2.gw --pep $name2.pep --ac 0 --id 0 --type 2 >$name2.gw.mut
	perl /ifs/TJPROJ3/Plant/xuwei/BJpan/putao/12xv2/new_all.genewise2/merge_overlap.pl  $name2.gw.alg 0.3 >$name2.gw.alg.nr
	#awk '$9>0.3' $name.gw.alg.nr >$name.gw.alg.nr.filter
        perl /ifs/TJPROJ3/Plant/xuwei/BJpan/putao/12xv2/new_all.genewise2/pickcscoregw.pl   $name2.gw.alg.nr > $name2.gw.alg.nr.filter
	mkdir nrResult
	perl /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/testv5/cat_file.pl ./result $name2.gw.alg.nr.filter >./nrResult/$name2.gw
	perl /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/testv5/gw_parser.pl --gw ./nrResult/$name2.gw --pep $name2.pep --ac 0 --id 0 --type 1 >./nrResult/$name2.gw.alg
	perl /ifs/TJPROJ3/Plant/xuwei/yanfa/anno/genesearch/testv5/gw_parser.pl --gw ./nrResult/$name2.gw --pep $name2.pep --ac 0 --id 0 --type 2 >./nrResult/$name2.gw.mut

	perl  /ifs/TJPROJ3/Plant/xuwei/yanfa/genewise_pipeline/v2/gw_to_gff.pl  ./nrResult/$name2.gw ./$name2.pep >./nrResult/$name2.gw.gff
	perl  /ifs/TJPROJ3/Plant/xuwei/yanfa/genewise_pipeline/v2/getGene.pl ./nrResult/$name2.gw.gff $genome >./nrResult/$name2.gw.cds
	perl /ifs/TJPROJ3/Plant/wangkai/pipeline/scripts/cds2aa.pl ./nrResult/$name2.gw.cds >./nrResult/$name2.gw.pep
