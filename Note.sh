perl /PUBLIC/software/DENOVO/bio/annotation/pipeline_v2.0/scripts/qsub-sge.pl
# rm脚本check
perl /home/liuwenbin/STAT/CheckrmScript/CheckrmScript.v2.pl  --group 1908,1919,1920  --dnum /TJPROJ4/XJ/department_data-nova/1919  rm.plant_1908_tj4_190624.sh

# blast语法
blastall -d $db -i $qu  -m 8  -F F -p blastn

# python 管理
pip3 install -i  https://pypi.tuna.tsinghua.edu.cn/simple/  
