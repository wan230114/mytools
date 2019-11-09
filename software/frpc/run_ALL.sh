#!/usr/bin/env bash                                                                                                                                                                                
shelp="""usage:
  run_ALL.sh argument

This is a monitoring tools for frpc.

positional arguments:
  start       start frpc.
  stop        stop all frpc.
  restart     restart frpc.
  clean       clean log, keep 20000 lines.
optional arguments:
  -h/--help   show this help message and exit 1.
"""
shelp2=" [please run -h/--help to get help doc.]"

tools_path=$(cd $(dirname ${BASH_SOURCE[0]})>/dev/null && pwd )

#echo "[input args: $*]"
array_args=($*)
for i in ${array_args[@]}
do
    [ "$i" == "-h" ] && echo -e "$shelp" && exit 0
    [ "$i" == "--help" ] && echo -e "$shelp" && exit 0
done
# 判断参数是否正确
[ $# -eq 0 ] && echo -e "$shelp" && exit 1
[ $# -ne 1 ] && echo -e "args num input eero, ${shelp2}" && exit 1
p=0
array=("start" "stop" "restart" "clean")
for x in ${array[@]}
do
    [ "$1" == "$x" ] && break
	((p++))
done
[ $p -eq 4 ] && echo -e "args input eero, ${shelp2}" && exit 1

# main
cd ${tools_path}
if [ "$1" == "start" ]; then
    #echo start frpc...
    if [ "`ps x|grep frpc|grep -v " grep "`" != "" ]; then echo `date +%F' '%H:%M:%S` running >>moni.log; else sh -c "echo \`date +%F' '%H:%M:%S\` no running, will do it. >>moni.log; nohup ./frpc -c ./frpc.ini &>log &"; fi; 
elif [ "$1" == "stop" ]; then
    #echo stop frpc...
    nohup sh -c "nohup ps x|grep frp|grep -v ' grep '|awk '{print \$1}'|xargs -i kill -s 9 {} &>log.kill &" &>log.run_ALL &
elif [ "$1" == "restart" ]; then
    #echo restart frpc...
    nohup sh -c "nohup ps x|grep frp|grep -v ' grep '|awk '{print \$1}'|xargs -i kill -s 9 {} &>log.kill &; nohup ./frpc -c ./frpc.ini &>log &" &>log.run_ALL &
elif [ "$1" == "clean" ]; then
    #echo clean log...
    tail -n 20000 moni.log >moni.log.last && >moni.log
fi

# if [ "`ps aux|grep frpc|grep -v " grep "`" != "" ]; then echo `date +%F' '%H:%M:%S` running >>/var/www/frp/moni.log; else sh -c "cd /var/www/frp; echo \`date +%F' '%H:%M:%S\` no running, will do it. >>moni.log; nohup ./frpc -c ./frpc.ini &>./frpc.ini.log &"; fi;

# 设置定时启动
# 0 */1 * * * /var/www/frp/moni.sh
# 0 0   1 * * /var/www/frp/moni.log-clean.sh
# 设置开机启动
