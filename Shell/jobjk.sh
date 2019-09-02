source /etc/profile
#source /home/chenjun/.bashrc
setjob="1850";
numjob=`/opt/gridengine/bin/linux-x64/qstat -u chenjun|sed '1d'|sed '1d'|wc -l`; /opt/gridengine/bin/linux-x64/qstat &>/home/chenjun/tmplog/log_jobnums1;
if (("$numjob" >= "$setjob")); then echo "h `date +%F` $numjob / $setjob"; /PUBLIC/software/public/Python-2.7.6/bin/python /ifs/TJPROJ3/Plant/chenjun/mytools/sendmail.py 1170101471@qq.com -c "Warning, job beyongd your set: $setjob ,now is $numjob."; else echo "l `date +%F` $numjob / $setjob";fi &>/home/chenjun/tmplog/log_jobnums
