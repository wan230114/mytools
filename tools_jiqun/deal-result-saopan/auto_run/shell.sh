source /home/chenjun/.bashrc

cd /ifs/TJPROJ3/Plant/chenjun/Admin/02.saopan
logtime=`date  +%Y-%m-%d`
if mkdir $logtime;
then
    echo $logtime >lastdate 
    # 删除最后两次以前的内容
    ls */scan/01.scan_results/01.scan_shell_out/|grep :|tr -d :|sed '$d'|sed '$d'|xargs rm -r
    # 杀上次任务及进程
    echo "ps xjf |grep scan/00.bin/scan_shell/shell_file_list|grep -v \"_ grep\"|awk '{print \$3}'|xargs -i grep {} <(ps xjf)|awk '{print \$2}'"|bash|xargs kill
    /home/leiyang/local/bin/vjob|grep scan/00.bin/scan_shell/shell_file_list|awk '{print $1}'|xargs qdel
    cp mod/* $logtime -r && echo 已成功创建文夹 $logtime >>log
    cd $logtime && nohup sh work.sh &
else
    echo 已跳过复制 $logtime >>log
fi

# 使用方法
shelp="""
一、功能简介
每周日零点投递扫盘（同时终止上次扫盘运行），每天在最新目录下进行扫盘结果统计。

二、使用简介：
复制三个文件(夹)：get-result.sh、mod、shell.sh 于工作文件夹，然后打开crontab -e加入以下命令：

三、示例：
1.准备工作路径，复制三个文件于工作路径：/NJPROJ2/Plant/chenjun/Admin/02.saopan/
2.打开crontab -e：

# 天津
0 0 * * 0  /bin/sh /NJPROJ2/Plant/chenjun/Admin/02.saopan/shell.sh
0 9 * * *  /bin/sh /NJPROJ2/Plant/chenjun/Admin/02.saopan/get-result.sh

# 南京
0 0 * * 0  /bin/sh /ifs/TJPROJ3/Plant/chenjun/Admin/02.saopan/shell.sh
0 9 * * *  /bin/sh /ifs/TJPROJ3/Plant/chenjun/Admin/02.saopan/get-result.sh
"""

