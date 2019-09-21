# 导入环境变量
source ./mod/bashrc_source.sh

# 进入当前文件夹
script_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd ${script_path}


cp mod/result_stat_scan/* `cat lastdate`/result_stat_scan/
#cat lastdate |xargs -i echo "cd {}/result_stat_scan && sh qsub-run.sh"|sh
echo "cd `cat lastdate`/result_stat_scan && sh qsub-run.sh"|sh
