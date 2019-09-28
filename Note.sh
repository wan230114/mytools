# python 管理
pip3 install -i  https://pypi.tuna.tsinghua.edu.cn/simple/  

############################################################
####################### 1.集群管理 #########################
############################################################

### 常用 ###
# 集群投递管理脚本
perl /PUBLIC/software/DENOVO/bio/annotation/pipeline_v2.0/scripts/qsub-sge.pl
# 下机数据 rm脚本check
perl /home/liuwenbin/STAT/CheckrmScript/CheckrmScript.v2.pl  --group 1908,1919,1920  --dnum /TJPROJ4/XJ/department_data-nova/1919  rm.plant_1908_tj4_190624.sh
perl /NJPROJ2/home/liuwenbin/STAT/CheckrmScript/CheckrmScript.v2.pl  --group 1908,1919,1920,0216 --dnum /NJPROJ3/XJ/Data_production/department_data_Nova/1908  rm.plant_nj_190705.sh >rm.plant_nj_190705.sh--check.log

### 上传阿里云冷存储 ###
alias lsy="/TJNAS01/PAG/Plant/zhangwenlin/Cluster_management/Aliyun/JieDong/bin/ossutil64  -c /TJPROJ1/DENOVO/PROJECT/zhangkaijian/program/Aliyun/bin/general_ossutilconfig"                                     
# 身份验证配置文件，用于-c后面
/TJPROJ1/DENOVO/PROJECT/zhangkaijian/program/Aliyun/bin/general_ossutilconfig
/NJPROJ2/Plant/Projects/Plant2/zhangkaijian/program/Aliyun/bin/general_ossutilconfig
# 天津上传or下载（原始脚本）
# 南京上传or下载（原始脚本）
/NJPROJ2/Plant/zhangwenlin/Cluster_management/Aliyun/xiazai/bin/ossutil64 -c /NJPROJ2/Plant/Projects/Plant2/zhangkaijian/program/Aliyun/bin/general_ossutilconfig cp -r /NJPROJ2/Plant/chenjun/prj/01.WGS/X101SC19010440-Z01_184caomei/00.data-all-rawdata/wenku/01.0226.rawdata/BDSW190002954-1a/BDSW190002954-1a_L4_1.fq.gz oss://plant-nj/Plant_Group2/X101SC19010440-Z01_184caomei/00.data-all-rawdata/wenku/01.0226.rawdata/BDSW190002954-1a/BDSW190002954-1a_L4_1.fq.gz
# 现成封装开发脚本，可以直接运行，会自动投递
/NJPROJ1/PAG/Plant/Projects/Business/GWAS/WGS/P101SC17071673-01_300_yama/10.release/work_aliyun_Data.sh


############################################################
####################### 2.软件记录 #########################
############################################################
### 软件语法 ###
# blast语法
blastall -d $db -i $qu  -m 8  -F F -p blastn

### 软件脚本 ###
# 画circos图：
alias circos="/PUBLIC/software/public/System/Perl-5.18.2/bin/perl /PUBLIC/software/public/Graphics/circos-0.64/bin/circos "


# 软件建立索引：
ref=App.fa
#建立bwa比对所需要的index	#超过1G的用这个
#/PUBLIC/software/public/Alignment/bwa/bwa-0.7.8/bwa index -a bwtsw $ref
#建立bwa比对所需要的index	#小于1G的用这个
#/NJPROJ2/Crop/share/pipeline/current/BSA/00.bin/indBin/bwa index -a is $ref
#建立samtools检测SNP所需要的index
#/NJPROJ2/Crop/share/pipeline/current/BSA/00.bin/indBin/samtools  faidx $ref
#建立dist文件
#/NJPROJ2/Crop/share/software/picard-tools-1.96/CreateSequenceDictionary.jar R=$ref O=ref.dict TMP_DIR=/NJPROJ2/Crop/share/pipeline/current/BSA/00.bin
#soap
/NJPROJ1/PAG/Crop/share/software/appLinkPath/bowtie-1.0.1 $ref
#bwa
/NJPROJ1/PAG/Crop/share/software/appLinkPath/bwa index -a bwtsw $ref
#sam
/NJPROJ1/PAG/Crop/share/software/appLinkPath/samtools faidx $ref
#base_stat
/NJPROJ1/PAG/Plant/Projects/Business/Variation/WGS/P101SC17091285-01_tomato/sample_26/00.ref/base-stat.pl $ref > $ref.base.stat.xls
#建立dist文件
/NJPROJ2/Crop/share/software/picard-tools-1.96/CreateSequenceDictionary.jar R=$ref O=./App


###### crontab -e 备份 ######
shelp="""
#################################### tj #####################################
# 磁盘挂起
#*/5 * * * * /PUBLIC/software/RESEQ/software/SGE/setup/cluster_tools/watchDisk/disk_monitor_client.pl
#*/50 * * * * /PUBLIC/software/RESEQ/software/SGE/setup/cluster_tools/watchDisk/disk_monitor_client.pl
#*/5 7-20  * * * /PUBLIC/software/RESEQ/software/SGE/setup/cluster_tools/watchDisk/disk_monitor_client.pl
#*/5 7-8  * * * /PUBLIC/software/RESEQ/software/SGE/setup/cluster_tools/watchDisk/disk_monitor_client.pl

# 每日磁盘大小统计
0 8 * * * /ifs/TJPROJ3/Plant/chenjun/software/fileshare/00.get2mail.sh
#*/1 * * * * /ifs/TJPROJ3/Plant/chenjun/software/fileshare/test.sh

# 自动扫盘，每月14日和28日开始扫盘投递
0 0 */14 * *  /bin/sh /ifs/TJPROJ3/Plant/chenjun/Admin/02.saopan/shell.sh
#0 0 * * 0    /bin/sh /ifs/TJPROJ3/Plant/chenjun/Admin/02.saopan/shell.sh
0 9 * * *  /bin/sh /ifs/TJPROJ3/Plant/chenjun/Admin/02.saopan/get-result.sh


# 集群job上限超过设定值提醒，参数1为邮箱，参数2为提醒的job数量
*/1 * * * * /ifs/TJPROJ3/Plant/chenjun/mytools/Shell/jobjk.sh 1170101471@qq.com 1850



# 使用方法
# {minute} {hour} {day-of-month} {month} {day-of-week} {full-path-to-shell-script} 
# o minute: 区间为 0 – 59 
# o hour: 区间为0 – 23 
# o day-of-month: 区间为0 – 31 
# o month: 区间为1 – 12. 1 是1月. 12是12月. 
# o Day-of-week: 区间为0 – 7. 周日可以是0或7.


#################################### nj #####################################
# 磁盘挂起
#*/5 * * * * /NJPROJ2/Plant/users/wangyayun/software/watchDisk/disk_monitor_client.pl
#*/50  * * * * /NJPROJ2/Plant/users/wangyayun/software/watchDisk/disk_monitor_client.pl
#*/5 7-8 * * * /NJPROJ2/Plant/users/wangyayun/software/watchDisk/disk_monitor_client.pl

# 每日磁盘统计
52-55/1 7 * * * /NJPROJ2/Plant/chenjun/software/fileshare/00.givedata.sh
#*/1 * * * * /NJPROJ2/Plant/chenjun/software/fileshare/test.sh

# 自动扫盘
0 0 */14 * *  /bin/sh /NJPROJ2/Plant/chenjun/Admin/02.saopan/shell.sh
0 9 * * *  /bin/sh /NJPROJ2/Plant/chenjun/Admin/02.saopan/get-result.sh

"""
