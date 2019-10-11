#! /bin/bash
shelp="""usage:
  qjk email keyword [-d] [-h]

This is a monitoring tools for vjobs.

positional arguments:
  email       E-mail address. When the monitoring task ends, the sent E-mail address.
  keyword     vjob's monitoring task keyword

optional arguments:
  -h          show this help message and exit
  -d          Running under the current directory
"""

tools_path=`dirname $(cd $(dirname ${BASH_SOURCE[0]})>/dev/null && pwd )`
array=($*)

echo "[input args: $*]"
for i in ${array[@]}
do
    [ "$i" == "-h" ] && echo -e "$shelp" && exit 0
    [ "$i" == "--help" ] && echo -e "$shelp" && exit 0
done

x=0

if [ $# -eq 2 ]; then
    array=($*)
    p=0
    for i in ${array[@]}
    do
        ARGV=$i
        [ ${ARGV:0:1} == "-" ] && echo -e "args erro.  usage: qjk email keyword [-d] [-h]" && exit 0
    done
    echo 进入~/tmplog投递任务中
elif [ $# -eq 3 ]; then
    array=($*)
    for i in ${array[@]}
    do
        ARGV=$i
        [ $ARGV == "-h" ] && echo -e "$shelp" && exit 0
        [ $ARGV == "--help" ] && echo -e "$shelp" && exit 0
        [ $ARGV == "-d" ] && x=1 && echo 正在当前文件夹投递任务中
    done
    if [ $x -ne 1 ];then echo -e "args erro.  usage: qjk email keyword [-d] [-h]" && exit 0 ;fi
else
    echo -e "args erro.  usage: qjk email keyword [-d] [-h]" && exit 0
fi


set -e
path=`pwd`

# 决定是在当前目录下执行还是 ~/tmplog 下，第三个参数不为空则在当前目录下
if [ $x -eq 0  ]; 
then
    if [ -e ~/tmplog ]; then sleep 0 ; else mkdir ~/tmplog; fi
    cd ~/tmplog; 
fi

# 投递任务
echo do1: $?
nohup python ${tools_path}/tools_jiqun/moni_renwu.py $2 &>nohup-moni_renwu.py.o && \
    echo && echo "监控完成！keyword" $2  && \
    python ${tools_path}/sendmail/sendmail.py $1 -c "监控任务$2已跑完" &
echo do2: $?

if [ $? -ne 0 ]; then
    echo 监控命令后台中...
    echo [keyword: $2]
    echo 日志文件: `pwd`/moni_renwu.py.log_`echo $2|sed 's#/#_#g'`
else
    echo 任务投递失败，日志文件：`pwd`/nohup-moni_renwu.py.o
fi

cd $path
