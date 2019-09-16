source /etc/profile
#source /home/chenjun/.bashrc

#mymail="1170101471@qq.com";
#setjob="150";
mymail=$1
setjob=$2


if [ -e ~/tmplog];then sleep 0; else mkdir ~/tmplog ; fi
cd ~/tmplog
/opt/gridengine/bin/linux-x64/qstat &>log_jobnums1;
numjob=`cat log_jobnums1|sed '1d'|sed '1d'|wc -l`;
if (("$numjob" >= "$setjob")); then echo "h `date +%F`  $numjob / $setjob"; /PUBLIC/software/public/Python-2.7.6/bin/python /ifs/TJPROJ3/Plant/chenjun/mytools/sendmail.py ${mymail} -c "Warning, job beyongd your set: $setjob ,now is $numjob."; else echo "l `date +%F`  $numjob / $setjob";fi &>log_jobnums
