echo start at time `date +%F'  '%H:%M` 'test hello' >>/ifs/TJPROJ3/Plant/chenjun/software/fileshare/test.sh.txt

export PATH=/ifs/TJPROJ3/Plant/chenjun/software/python3/bin/:$PATH

echo start at time `date +%F'  '%H:%M` 'test hello' |	/ifs/TJPROJ3/Plant/chenjun/software/python3/bin/python3 /ifs/TJPROJ3/Plant/chenjun/software/fileshare/sendmail.py 1170101471@qq.com -c '天津测试ok' &>/ifs/TJPROJ3/Plant/chenjun/software/fileshare/test.sh.log

sh /ifs/TJPROJ3/Plant/chenjun/software/fileshare/dfa.sh &>/ifs/TJPROJ3/Plant/chenjun/software/fileshare/dfa.sh.log
