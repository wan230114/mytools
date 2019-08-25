#/bin/bash
while [ "`ps xjf|grep $2 |grep -v grep`" ];do sleep 20;done && python /ifs/TJPROJ3/Plant/chenjun/mytools/sendmail.py $1 -c "进程运行$2结束" &

