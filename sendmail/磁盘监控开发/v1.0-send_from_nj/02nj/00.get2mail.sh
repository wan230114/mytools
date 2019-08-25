
cd /NJPROJ2/Plant/chenjun/software/fileshare/
echo start at time `date +%F'  '%H:%M`  >>00.get2mail.sh.log

rm log /sharedir/log &>/dev/null                

/NJPROJ2/Plant/chenjun/software/python3/python3.7/bin/python3 file-client.py >>file-client.py.log 2>>00.get2mail.sh.log   && echo 01 done. >>00.get2mail.sh.log

echo -e '天津：' >sendmail.txt  &&  cat sharedir/log >>sendmail.txt && echo -e '南京：' >>sendmail.txt  && echo -e "/NJPROJ1/PAG/Plant/ \n/NJPROJ2/Plant/     \n/NJPROJ3/Plant/     "|xargs -i sh -c """df {}|sort|head -1|awk '{print \$3}'|awk '{if(int(\$0) < 5368709120) print \"{}\t  \"\$0/1024/1024/1024\"T\"}'""" >>sendmail.txt 2>>00.get2mail.sh.log   && echo 02 done. >>00.get2mail.sh.log

/NJPROJ2/Plant/chenjun/software/python3/python3.7/bin/python3 sendmail.py &>/dev/null  &&  echo start at time `date +%F'  '%H:%M` 'send success.' >>sendmail.py.log 2>>00.get2mail.sh.log   && echo -e "03 done.\n" >>00.get2mail.sh.log
