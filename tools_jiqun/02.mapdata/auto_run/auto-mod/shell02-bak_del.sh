mkdir 02.bak_del
cd 02.bak_del

# 筛选有匹配到的文库
ln -s ../01.mapfile/lst.merge.final
awk  -F "\t" '{if(NF>3)print}' lst.merge.final >lst.merge.final.filterall

# 此步需要手动去除需要保留的，这里示例假如没有，直接复制
cp lst.merge.final.filterall lst.merge.final.filter

# 生成删除脚本以及备份脚本
TIME=`cat ../time`
cut -f 2 lst.merge.final.filter |xargs -i echo rm -rf {} >rm.Plant_$TIME.sh
if [ "`ls /NJPROJ2/Plant/chenjun/mytools 2>/dev/null`" ]
then
    cut -f 2 lst.merge.final.filter |xargs -i echo /NJPROJ2/Plant/zhangwenlin/Cluster_management/Aliyun/xiazai/bin/ossutil64 -c /NJPROJ2/Plant/Projects/Plant2/zhangkaijian/program/Aliyun/bin/general_ossutilconfig cp -r {}/* oss://plant-nj/AutoBak/{} >oss_bk.Plant_$TIME.sh
else
    cut -f 2 lst.merge.final.filter |xargs -i echo /TJNAS01/PAG/Plant/zhangwenlin/Cluster_management/Aliyun/JieDong/bin/ossutil64 -c /TJPROJ1/DENOVO/PROJECT/zhangkaijian/program/Aliyun/bin/general_ossutilconfig cp -r {}/* oss://plant-tj/AutoBak/{} >oss_bk.Plant_$TIME.sh
fi

cd -
