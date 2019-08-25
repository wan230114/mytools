path=`pwd` && mkdir ~/tmplog 2>/dev/null

# 决定是在当前目录下执行还是 ~/tmplog 下，第三个参数不为空则在当前目录下
if [ "$3" ]; then sleep 0; else cd ~/tmplog; fi

if [ "`ls /ifs/TJPROJ3/Plant/chenjun/mytools/Shell 2>/dev/null`" ]
then
    nohup python /ifs/TJPROJ3/Plant/chenjun/mytools/tools_jiqun/moni_renwu.py $1 $2 >nohup-moni_renwu.py.o && echo &&echo "监控完成！" && cat nohup-moni_renwu.py.o &
else
    nohup python /NJPROJ2/Plant/chenjun/mytools/tools_jiqun/moni_renwu.py     $1 $2 >nohup-moni_renwu.py.o && echo &&echo "监控完成！" && cat nohup-moni_renwu.py.o &
fi

echo 监控命令后台中...
echo [keyword: $2]
echo 日志文件: `pwd`/moni_renwu.py.log_`echo $2|sed 's#/#_#g'`
cd $path

