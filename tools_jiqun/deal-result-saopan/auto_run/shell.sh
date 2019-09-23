# 进入当前文件夹
script_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd ${script_path}

# 导入环境变量
source ./mod/bashrc_source.sh

# 创建运行目录
logtime=`date  +%Y-%m-%d`
if [ -e $logtime] ;
then
    echo 已跳过复制 $logtime >>log
else
    echo $logtime >lastdate 
    # 删除最后两次以前的内容（只sed一次的原因是本次还要生成一次）
    ls */scan/01.scan_results/|grep :|tr -d :|sed '$d'|xargs rm -r
    # 杀上次任务及进程
    echo "ps xjf |grep scan/00.bin/scan_shell/shell_file_list|grep -v \"_ grep\"|awk '{print \$3}'|xargs -i grep {} <(ps xjf)|awk '{print \$2}'"|bash|xargs kill
    vjob|grep scan/00.bin/scan_shell/shell_file_list|awk '{print $1}'|xargs qdel
    # 生成目录
    cp mod/ $logtime/ -rL && echo 已成功创建文夹 $logtime >>log
    # 投递
    cd $logtime && nohup sh work.sh &
fi



# 使用方法
shelp="""
一、功能简介
    每周日零点投递扫盘（同时终止上次扫盘运行），每天在统计目录下获取最新扫盘结果统计。

二、使用简介：
    准备三个文件(夹)：get-result.sh、mod、shell.sh 于工作文件夹，然后打开crontab -e加入以下命令：
     - shell.sh  用于投递扫盘
     - mod       用于投递扫盘所需要的运行文件，
                 位于/ifs/TJPROJ3/Plant/chenjun/mytools/tools_jiqun/deal-result-saopan/auto_run/mod_tj/
                 或/NJPROJ2/Plant/chenjun/mytools/tools_jiqun/deal-result-saopan/auto_run/mod_nj/
     - get-result.sh  用于对扫盘后的结果进行格式化统计

三、示例：
    1.准备工作路径，复制三个文件或软链接于工作路径， 如：/NJPROJ2/Plant/chenjun/Admin/02.saopan/
    2.打开crontab -e：加入以下定时运行的命令，如：

# 天津，每周日投递一次
0 0 * * 0  /bin/sh /NJPROJ2/Plant/chenjun/Admin/02.saopan/shell.sh
0 9 * * *  /bin/sh /NJPROJ2/Plant/chenjun/Admin/02.saopan/get-result.sh

# 南京，每两周投递一次扫盘（每月14日和28日）
0 0 */14 * * /bin/sh /NJPROJ2/Plant/chenjun/Admin/02.saopan/shell.sh
0 9 * * *    /bin/sh /ifs/TJPROJ3/Plant/chenjun/Admin/02.saopan/get-result.sh

# crontab -e的时间语法说明：
# {minute} {hour} {day-of-month} {month} {day-of-week} {full-path-to-shell-script}
# o minute: 区间为 0 – 59
# o hour: 区间为0 – 23
# o day-of-month: 区间为0 – 31
# o month: 区间为1 – 12. 1 是1月. 12是12月.
# o Day-of-week: 区间为0 – 7. 周日可以是0或7.

"""

