# 记录脚本所在文件夹
script_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

# 导入环境变量
source ${script_path}/bashrc
