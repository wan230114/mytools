# 记录脚本所在文件夹
script_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

# 导入环境变量
if [ -e /ifs/TJPROJ3/Plant/chenjun/mytools ]; then
    source ${script_path}/bashrc
elif [ -e /NJPROJ2/Plant/chenjun/mytools ]; then
    source ${script_path}/bashrc_nj
fi
