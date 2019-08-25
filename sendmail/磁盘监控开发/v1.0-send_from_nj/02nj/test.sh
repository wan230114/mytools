cd /NJPROJ2/Plant/chenjun/software/fileshare
echo start at time `date +%F'  '%H:%M` 'test hello' &>test.sh.log

/NJPROJ2/Plant/chenjun/software/python3/python3.7/bin/python3 file-client.py &>>test.sh.log

#echo start at time `date +%F'  '%H:%M` 'test hello'|xargs /NJPROJ2/Plant/chenjun/software/python3/python3.7/bin/python3 /NJPROJ2/Plant/chenjun/mytools/sendmail.py 1170101471@qq.com -c test-over &>>test.sh.log
