#! /bin/bash

tools_path=`pwd`
#tools_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

if [ "$1" == "-p" ]; then
    file=/dev/stdout
else
    file=~/.bashrc
    cp -i ./bashrc/.*rc ~/
fi

echo >>$file
echo "# >>> bashrc >>>"  >>$file
echo "source ${tools_path}/bashrc_my.sh"  >>$file
echo 'mymail="1170101471@qq.com"'  >>$file
echo "source ${tools_path}/bashrc_Tools.sh"  >>$file

#read -p "input a val:" val echo $val

