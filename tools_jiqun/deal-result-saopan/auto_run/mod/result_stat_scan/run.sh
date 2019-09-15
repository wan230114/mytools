#! /bin/bash
# 配置统计参数: num代表需要关注的文件大小，既筛选的文件路径大小最小值，单位为M；
Num=10


# 导入环境变量
source ../../mod/bashrc_source.sh

##################################################### ################################################
#########################################  s t a r t  ################################################
##################################################### ################################################

# 文件处理
rm -r result/* raw-result/ 2>/dev/null
ls -tr run.sh.*|sed '$d'|sed '$d'|xargs rm 2>/dev/null
mkdir result/ raw-result/ 2>/dev/null

# 处理参数
scan_path=../scan/01.scan_results/02.formatted_results_from_scan_shell_out/
Num_b=$(($Num*1024**2))
Numname=all
if [ "$Num" -gt "0"  ]; then Numname=${Num}M; fi

# 控制最大进程数为3
i=0
for name in `ls ${scan_path}`; do ((i++)); echo "cat ${scan_path}/${name}/*|awk -v numb=${Num_b} '{if(\$5>=numb){OFS=\"\\t\";print \$3,\$5,\$9,\$6}}' >result/${name}_${Numname} &"; if [ "$((${i}%3))" == "0" ]; then echo wait; fi;done|awk '{print}END{print "wait"}'|sh
echo getSIZE done.

# 统计总览(此脚本尚待优化，因为pandas是一次性将数据读入内存，当输入数据过大会耗费大量资源)
python3 ${tools_path}/tools_jiqun/deal-result-saopan/main_xiangmu.py result
# 给统计结果第二列后面一列，加上大小的单位统计，利于信息查找
mv result/* raw-result/
for name in `ls raw-result/`; do ((i++)); echo "python3 ${tools_path}/tools_jiqun/getsize.py -i raw-result/${name} -n 2 --add >result/${name} &"; if [ "$((${i}%3))" == "0" ]; then echo wait; fi;done|awk '{print}END{print "wait"}'|sh


# 移动到对应日期文件夹
new_dir="result_`date +%m%d`"
rm -r ${new_dir} 2>/dev/null
mkdir ${new_dir}
mv raw-result/ result/ result-tongji.txt*  ${new_dir}

# 删除之前统计结果，只保留最后两次统计的
ls|grep result_|sed '$d'|sed '$d'|xargs rm -r
rm Result 2>/dev/null
ln -s ./${new_dir}/ Result

