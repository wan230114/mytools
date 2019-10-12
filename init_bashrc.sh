#! /bin/bash

tools_path="$( cd $(dirname $0) && pwd)"
#tools_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

if [ "$1" == "-p" ]; then
    #echo do1
    file=/dev/stdout
else
    #echo do2
    file=~/.bashrc
    cp -i ./bashrc/.*rc ~/
fi

echo >>$file
echo "# >>> bashrc >>>"  >>$file
echo source ${tools_path}/bashrc_my.cfg  >>$file
echo mymail=\"1170101471@qq.com\"  >>$file
echo source ${tools_path}/bashrc_Tools.sh  >>$file
tools_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

echo ${tools_path}/
read -p "input a val:" val echo $val

