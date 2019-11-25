set -e
ps xjf |grep "./test -c cfg"|grep -v grep|awk '{print $2}' |xargs -i kill {}
sudo /etc/init.d/ssh start
nohup ./frpc -c frpc.ini &>>log &
nohup sleep 86400 && ps xjf |grep "./test -c cfg"|grep -v grep|awk '{print $2}' |xargs kill &
