#! /bin/bash

tools_path=$(pwd)
#tools_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

#read -p "input a val:" val echo $val
cp -ir $(ls ./bashrc/.* -d | sed 1,2d) ~/

if [ "$(grep "# >>> bashrc >>>" ~/.bashrc)" ]; then
    file=/dev/stdout
else
    file=~/.bashrc
fi

echo "
# >>> bashrc >>>
source ${tools_path}/bashrc_my.sh
mymail=1170101471@qq.com
source ${tools_path}/bashrc_Tools.sh
export PATH=${tools_path}/bin:\$PATH
" >>$file

source ~/.bashrc
