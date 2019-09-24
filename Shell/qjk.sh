set -e
path=`pwd`

# 决定是在当前目录下执行还是 ~/tmplog 下，第三个参数不为空则在当前目录下
if [ "$3" ]; 
then
    sleep 0; 
else 
    if [ -e ~/tmplog ]; then sleep 0 ; else mkdir ~/tmplog; fi
    cd ~/tmplog; 
fi

# 投递任务
if [ -e "/ifs/TJPROJ3/Plant/chenjun/mytools/Shell" ]
then
    nohup python /ifs/TJPROJ3/Plant/chenjun/mytools/tools_jiqun/moni_renwu.py $1 $2 &>nohup-moni_renwu.py.o && echo && echo "监控完成！"  &
else
    nohup python /NJPROJ2/Plant/chenjun/mytools/tools_jiqun/moni_renwu.py     $1 $2 &>nohup-moni_renwu.py.o && echo && echo "监控完成！"  &
fi

echo 监控命令后台中...
echo [keyword: $2]
echo 日志文件: `pwd`/moni_renwu.py.log_`echo $2|sed 's#/#_#g'`
cd $path

