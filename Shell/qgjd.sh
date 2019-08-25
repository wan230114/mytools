path=`pwd` && mkdir ~/tmplog 2>/dev/null
cd ~/tmplog
if [ "`ls /ifs/TJPROJ3/Plant/chenjun/mytools/Shell 2>/dev/null`" ]
then
    nohup python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_jiqun/moni_qalter.py $1 $2 $3 >nohup.out-moni_qalter.py && echo && echo "改节点命令结束！" && echo && cat ~/tmplog/nohup.out-moni_qalter.py &
else
    nohup python3 /NJPROJ2/Plant/chenjun/mytools/tools_jiqun/moni_qalter.py $1 $2 $3 >nohup.out-moni_qalter.py && echo && echo "改节点命令结束！" && echo && cat ~/tmplog/nohup.out-moni_qalter.py &
fi

echo 改节点命令后台运行中...
echo [keyword: $1 , 模式: $2 , 附加参数: $3]
echo 日志文件: ~/tmplog/moni_qalter.py.log.$1.$2
cd $path

