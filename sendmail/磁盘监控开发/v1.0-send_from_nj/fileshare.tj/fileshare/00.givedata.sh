cd /ifs/TJPROJ3/Plant/chenjun/software/fileshare
echo start at time `date +%F'  '%H:%M`  &>>00.givedata.sh.log
mkdir sharedir &>/dev/null   ; echo 01 mkdir sharedir. >>00.givedata.sh.log

echo \*\*\*`/ifs/TJPROJ3/Plant/chenjun/software/python3.5/bin/python3 gettime.py`\*\*\* >sharedir/log
echo -e "/TJNAS01/PAG/Plant/ \n/TJPROJ1/DENOVO/   \n/ifs/TJPROJ3/Plant/ "|xargs -i sh -c """df {}|sort|head -1|awk '{print \$3}'|awk '{if(int(\$0) < 5368709120) print \"{}\t  \"\$0/1024/1024/1024\"T\"}'""" >>sharedir/log 2>>00.givedata.sh.log      && echo 02 geted log. >>00.givedata.sh.log
#/ifs/TJPROJ3/Plant/chenjun/software/python3.5/bin/python3 file-client.py &>>file-client.py.log       && echo -e "03 send mail success.\n" >>00.givedata.sh.log

