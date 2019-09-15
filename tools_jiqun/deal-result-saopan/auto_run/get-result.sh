# 导入环境变量
if [ -e /ifs/TJPROJ3/Plant/chenjun/mytools ]; then 
    source ./mod/bashrc
elif [ -e /NJPROJ2/Plant/chenjun/mytools ]; then
    source ./mod/bashrc_nj
fi


cd /ifs/TJPROJ3/Plant/chenjun/Admin/02.saopan
cp mod/result_stat_scan/* `cat lastdate`/result_stat_scan/
#cat lastdate |xargs -i echo "cd {}/result_stat_scan && sh qsub-run.sh"|sh
echo "cd `cat lastdate`/result_stat_scan && sh qsub-run.sh"|sh
