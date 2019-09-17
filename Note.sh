# python 管理
pip3 install -i  https://pypi.tuna.tsinghua.edu.cn/simple/  


############################################################
######################## 软件记录 ##########################
############################################################
### 软件语法 ###
# blast语法
blastall -d $db -i $qu  -m 8  -F F -p blastn

### 软件脚本 ###
# 画图
alias circos="/PUBLIC/software/public/System/Perl-5.18.2/bin/perl /PUBLIC/software/public/Graphics/circos-0.64/bin/circos "


############################################################
######################## 集群管理 ##########################
############################################################
### 常用 ###
# 集群投递管理脚本
perl /PUBLIC/software/DENOVO/bio/annotation/pipeline_v2.0/scripts/qsub-sge.pl
# rm脚本check
perl /home/liuwenbin/STAT/CheckrmScript/CheckrmScript.v2.pl  --group 1908,1919,1920  --dnum /TJPROJ4/XJ/department_data-nova/1919  rm.plant_1908_tj4_190624.sh

### 上传阿里云冷存储 ###
# 身份验证配置文件，用于-c后面
/NJPROJ2/Plant/Projects/Plant2/zhangkaijian/program/Aliyun/bin/general_ossutilconfig
/TJPROJ1/DENOVO/PROJECT/zhangkaijian/program/Aliyun/bin/general_ossutilconfig
# 天津上传or下载（原始脚本）
...
# 南京上传or下载（原始脚本）
/NJPROJ2/Plant/zhangwenlin/Cluster_management/Aliyun/xiazai/bin/ossutil64 -c /NJPROJ2/Plant/zhangwenlin/Cluster_management/Aliyun/xiazai/bin/ossutilconfig cp -r /NJPROJ2/Plant/chenjun/prj/01.WGS/X101SC19010440-Z01_184caomei/00.data-all-rawdata/wenku/01.0226.rawdata/BDSW190002954-1a/BDSW190002954-1a_L4_1.fq.gz oss://plant-nj/Plant_Group2/X101SC19010440-Z01_184caomei/00.data-all-rawdata/wenku/01.0226.rawdata/BDSW190002954-1a/BDSW190002954-1a_L4_1.fq.gz
# 现成封装开发脚本，可以直接运行，会自动投递
/NJPROJ1/PAG/Plant/Projects/Business/GWAS/WGS/P101SC17071673-01_300_yama/10.release/work_aliyun_Data.sh
