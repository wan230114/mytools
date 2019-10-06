#tools_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
tools_path="$( cd $(dirname $0) && pwd)"

if [ "$1" != "y" ]; then
    #echo do1
    file=/dev/stdout
else
    #echo do2
    file=~/.bashrc
fi

echo >>$file
echo "# >>> bashrc >>>"  >>$file
echo source ${tools_path}/bashrc_my.cfg  >>$file
echo mymail=\"1170101471@qq.com\"  >>$file
echo source ${tools_path}/Tools_bashrc.sh  >>$file

echo source ~/.bashrc|bash
