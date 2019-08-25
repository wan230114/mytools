#/bin/bash

if [ "`ls /ifs/TJPROJ3/Plant/chenjun/mytools/Shell 2>/dev/null`" ]
then
tools_path="/ifs/TJPROJ3/Plant/chenjun/mytools"
else
tools_path="/NJPROJ2/Plant/chenjun/mytools"
fi

echo -e "Input args: [$@]"
if test "`grep "\-\-help" <(echo $@)`";
then
    python3 ${tools_path}/tools_jiqun/md5q.py --help;
else
    logfile=log.md5q.`date  +%F'_'%H.%M.%S.%N`
    echo Running md5q in the background...
    echo Log file: ~/tmplog/$logfile
    mkdir ~/tmplog 2>/dev/null
    nohup python3 ${tools_path}/tools_jiqun/md5q.py $@ -l $logfile 1>~/tmplog/$logfile 2>&1 && echo &&echo "统计完成！" && cat ~/tmplog/$logfile &
    sleep 0.5
    echo
    cat ~/tmplog/$logfile
fi
