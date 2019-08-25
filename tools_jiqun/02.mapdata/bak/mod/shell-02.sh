listname=lst
# 处理每一行为文库名\t路径
python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_jiqun/02.mapdata/getlineWenku.py ${listname} >${listname}.tmp
#
cut -f 1,2 ${listname}.tmp |sort|uniq >${listname}.tmp.ID
#
#python3 quite.py nj.list.tmp 1 xiajiALL.list 10 >nj.list.merge

#cp tj4.list tj4.list.tmp.ID


# 去重并合并xiajiWENKU.list后，去查找
#python3 mergefile.py -f1 ${listname}.tmp.ID 1 -f2 xiajiWENKU.list 10 -fo ${listname}.merge  --sep "|" --keep
python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_files/mergefile.py -f1 ${listname}.tmp.ID 1 -f2 xiajiALL.list 10 -fo ${listname}.merge --include  --sep "|" --keep

cut -f 1,3-100 ${listname}.merge >${listname}.merge.final
awk -F '\t' '{OFS="\t"; print $1,$2,$25,$24,$5,$6}' ${listname}.merge.final >${listname}.merge.tiqu2
#awk -F '\t' '{OFS="\t"; print $1,$24,$23,$4,$5}' ${listname}.merge.final >tj4.list.merge.tiqu2
#cat ${listname}.merge.tiqu2|cut -f2-6 |sort |uniq -c |sort -k1,1nr >${listname}.merge.tiqu
cat ${listname}.merge.tiqu2|cut -f3-6 |sort |uniq -c |sort -k1,1nr >${listname}.merge.tiqu

python /NJPROJ2/Plant/chenjun/mytools/sendmail.py 1170101471@qq.com -c "merge完毕"

