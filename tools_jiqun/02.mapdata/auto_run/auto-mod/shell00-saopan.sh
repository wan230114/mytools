dumps="0216,1908,1919,1920"
# 当参数存在时重新导入
source ./run_auto.sh.cfg

# 初始化工具包路径
if [ "`ls /NJPROJ2/Plant/chenjun/mytools 2>/dev/null`" ]
then
    export PATH=/NJPROJ2/Plant/chenjun/software/Miniconda3/miniconda3/bin:$PATH
    tools_path="/NJPROJ2/Plant/chenjun/mytools"
else
    export PATH=/ifs/TJPROJ3/Plant/chenjun/software/Miniconda3/miniconda3/bin:$PATH
    tools_path="/ifs/TJPROJ3/Plant/chenjun/mytools"
fi

# 下机xiajiALL.list获取
if [ "`ls /NJPROJ1/lims/XJ/ 2>/dev/null`" ]
then
    cat /NJPROJ1/lims/XJ/* /NJPROJ2/home/oms/*|sed '/^$/d'|grep -P "\t" >xiajiALL.list
else
    cat /home/oms/20* /TJPROJ1/lims/XJ/20*|sed '/^$/d'|grep -P "\t" >xiajiALL.list
fi

# 准备
date "+%y%m%d" >time
mkdir 00.saopan
cd 00.saopan


# 1) 获取扫盘路径，生成find.sh
cat ../xiajiALL.list|cut -f 20|sort|uniq >Plant.path.tmp
# 筛选出部门所有存在路径
python3 ${tools_path}/tools_jiqun/02.mapdata/get_path_from_OMS.py  Plant.path.tmp  ${dumps}|sort|uniq  >Plant.path.all
# 判断路径是否存在
cat Plant.path.all|xargs -i echo "if [ -e \"{}\" ] ;then echo {};fi"|sh >Plant.path
# 生成扫盘脚本
cat Plant.path|awk 'BEGIN{n=0}{n+=1;print "find",$0,"-type f|xargs -i du -b {} >tmp/"n,"  &&  echo",n,"ok &"}END{print "wait\ncat tmp/*|grep -v /DONE/|grep -v \\.lst|grep -v ^0 >result.path"}' >find.sh


# 2) 开始扫盘
rm -r tmp/ result.path 2>/dev/null
mkdir tmp/
#wc find.sh -l|awk '{print "qsub -sync y -cwd -l vf="$1*0.2"g,p=0 find.sh"}' >run--find.sh
#sh run--find.sh
sh find.sh

cd -
