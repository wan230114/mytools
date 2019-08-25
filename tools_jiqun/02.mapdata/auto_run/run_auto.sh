echo '''--------------------------------------------------------------------------
注意事项：
  投递运行完成后，请进入当前日期文件夹去看日志，如：work.sh.o6227882，
  因有map存在包含模式，为防止map出错造成数据误删，
  请check后进行删除处理。
--------------------------------------------------------------------------
'''

if [ -e "/ifs/TJPROJ3/Plant/chenjun/Admin/04.mapXiaji" ]; 
then
    mapPATH=/ifs/TJPROJ3/Plant/chenjun/mytools/tools_jiqun/02.mapdata/auto_run/auto-mod; 
else
    mapPATH=/NJPROJ2/Plant/chenjun/mytools/tools_jiqun/02.mapdata/auto_run/auto-mod; 
fi

logtime=`date  +%Y-%m-%d`
echo $logtime >lastdate

if mkdir ${logtime};
then 
    cp ${mapPATH}/* $logtime/ ;
    cp run_auto.sh.cfg $logtime/ ;
    cd ${logtime}/ ;
    sh qsub--work.sh ;
else
    echo -e "\n文件夹${logtime}已存在"
    read -p "是否覆盖\"${logtime}\"( y-->yes, n-->no ):" pread
    if [ $pread == "y" ];
    then
        cp ${mapPATH}/* $logtime/ ;
        cp run_auto.sh.cfg $logtime/ ;
        cd ${logtime}/ ;
    else
        echo 已跳过创建文件夹
    fi
fi
