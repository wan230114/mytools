#/bin/bash
tools_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
kwword=$1
if [ "$2" ]; then mymail=$2; fi
echo keywords: ${kwword} ${mymail}

if [ "${kwword}" ];then

echo -e "\ndate\tuser\tpid\t%cpu\t%mem\trss\tvsz\tvsz(F)"

res="$(ps -eo user,pid,%cpu,%mem,rss,vsz|grep ${kwword}|getsize -n 6)"
datetime=`date "+%F_%H:%M:%S"`
while [ "$res" ];do
echo -e "${datetime}\t${res}"
res="$(ps -eo user,pid,%cpu,%mem,rss,vsz|grep ${kwword}|getsize -n 6)"
datetime=`date "+%F_%H:%M:%S"`
sleep 30;
done

if [ "${mymail}" ];then ${tools_path}/../bin/pysend ${mymail} ${kwword} -c 进程运行${keyword}结束; fi

fi

