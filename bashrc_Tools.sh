####################  导 入 工 具  ########################
# mymail="xxxx@xxx.com"
# source xxx/mytools/Tools_bashrc.sh
###########################################################

tools_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
#tools_path="$( cd $(dirname $0) && pwd)"
#tools_path=$(cd $(dirname ${BASH_SOURCE[0]}); cd - )
#echo  ${tools_path}


#######################################################################
###################  集 群 及 资 源 管 理 工 具  ######################
#######################################################################
export PATH=/home/leiyang/local/bin/:$PATH
export PATH=/NJPROJ2/home/leiyang/local/bin/:$PATH

# 1) 查看各种状态
# 磁盘
alias dfa='df -h  /TJNAS01/PAG/Plant/ /TJPROJ1/DENOVO/ /ifs/TJPROJ3/Plant/  /NJPROJ1/PAG/Plant/  /NJPROJ2/Plant/  /NJPROJ3/Plant/ 2>/dev/null'
# 任务
alias qs="qstat -u `whoami`"
alias q=vjob
alias vs=${tools_path}/Shell/vs
# 进程
alias pp="ps ux|head -1;ps ux|grep -v PID|sort -rn -k +3"  # 查看占用资源最多的进程
alias p="ps xjf" # 以进程树展示进程


# 2) 进程及任务操作
#alias ks="python3 ${tools_path}/tools_jiqun/ks.py"  # 批量杀进程，用法: `ks PGID/keyword`
alias qd="python3 ${tools_path}/tools_jiqun/qd.py"  # 批量杀任务，用法：`qd jobID/keyword`
alias qgjd="sh ${tools_path}/Shell/qgjd.sh"  # 批量改节点，用法: `qgjd mod keyword`，mod模式可选：1,2,3 (含义是：小节点，大节点，所有节点)
alias qjg="qmod -us "


# 3) 任务监控
alias qjk="${tools_path}/Shell/qjk.sh ${mymail} "
#alias pjk="sh ${tools_path}/Shell/pjk.sh ${mymail} "

# 4) oss集群互传工具
alias oss="python3 ${tools_path}/tools_jiqun/oss.py "

# 5) md5及size计算
alias md5="python3 ${tools_path}/tools_jiqun/md5.py"  # 本地计算当前目录md5和checksize, 用法: `md5 num`, num为进程数，最好不要超过10
alias md5q="sh ${tools_path}/Shell/md5q.sh"  # 自动投递集群计算当前目录md5和checksize, 用法: `md5q`

# 6) sjm流程提取工具
alias sjms="python3 ${tools_path}/tools_jiqun/sjms.py"

# 7) server
s_func(){
if [ "`echo $@`" ]; then port=$1; else port="8000";fi 
echo http://`ifconfig|grep inet|head -1|awk '{print $2}'`:$port
python3 -m http.server $port
}
alias s=s_func

#######################################################################
############################## myfunc #################################
#######################################################################
###  生信常用  ###
alias fas="python3 ${tools_path}/tools_fasta/fas.py"  # 碱基统计

###  日常工具  ###
# 发送邮件。可在搜狗输入法将邮箱等常用短语自定义添加，如输入qqqq会默认把邮箱放在输入法第一位。设置在: 搜狗输入法-->高级-->候选拓展-->自定义短语
#alias pysend="python ${tools_path}/sendmail/sendmail.py ${mymail}"  
#alias pywget="python3 ${tools_path}/tools_jiqun/pywget_file-client.py"
alias view="python3 ${tools_path}/tools_tree/imgdirView.py"  # 网页可视化文件夹svg,png,pdf
alias rep="python ${tools_path}/tools_files/rep_v2.py"  # 替换工具
alias ccut="python3 ${tools_path}/tools_files/ccut.py" # 补全cut不能去除末尾倒数多少列的问题，未开发完毕

### 文本格式化工具 ###
# markdown工具
alias mdc="python3 ${tools_path}/tools_md/markdowm_toc_change.py" # markdown升级或降级工具
# 格式化看脚本的命令，将各个参数自动换行，用法同cat一样
fcah(){  ## try"\n"-->"\t":[ sed ':label;N;s/\n/\t/;b label' ]
cat $@|sed ':label;N;s/ \\\n/ /;b label'|sed -e 's/[[:space:]][[:space:]]*/ /g'|sed 's# \-# \\\n    \-#g'|sed 's#^/#\n/#'|ca
}
alias cah=fcah  # 用于格式化打印脚本文件
alias cag="iconv -f gbk -t utf-8 "  # 打印gbk文件为utf8输出
alias ca="${tools_path}/Shell/common/ccat "

###  路径管理工具  ###
# 用于返回当前文件(夹)绝对路径
pwdfile(){
	if [ "`echo $@`" ]; then
		for idx in $(seq $#); do eval echo `pwd`/"$"$idx; done
	else
		ls -trd *|xargs -i echo `pwd`/{}
	fi
}
alias f=pwdfile  # 用于返回当前文件夹某文件或目录的路径, f [file/dir] [file/dir]...
alias r="realpath "
# 用于快速切换目录用
ffcd(){
if [ "$1" ]; then cd $1 && l; else cd . && l; fi
}
alias c=ffcd

###  文件磁盘管理工具  ###
# asum统计某一列的和，用法示例: `asum 1 file`
fasum(){
sh -c "awk 'BEGIN{sum=0}{sum+=\$$1; print \$0}END{print \"-----------\";print sum}' $2"
}
alias asum=fasum
#alias getsize="python3 ${tools_path}/tools_jiqun/getsize.py"  # 指定文件的某一列转换为计算机存储单位
#alias duc="du -bs ./*|sort -k1n|awk 'BEGIN{sum=0}{sum+=\$1;print \$0}END{print \"-----------\";print sum}'|getsize"
alias d="duc"  # 已在bin内

###  网络工具  ###
# 返回公网IP
# wget --tries=0 --recursive --restrict-file-names=windows --no-parent 
fg(){
echo $@|while read x;do ls `pwd`/$x|awk -v ip=`curl icanhazip.com 2>/dev/null` -F "fileshare" '{print "wget "ip":8999"$2}';done
}
fgg(){
find `pwd` -maxdepth 1 -type f |awk -v ip=`curl icanhazip.com 2>/dev/null` -F "fileshare" '{print "wget "ip":8999"$2}'
}
fIPinfo(){
curl https://ip.cn/index/php?ip=$1
}
alias g=fg
alias gg=fgg
alias IP="curl icanhazip.com 2>/dev/null"
alias IPa=fIPinfo

# unrar解压快捷方式定义
alias unrar2="while read x; do dirname=\`echo \$x|sed 's/.rar\$//'\`; mkdir \$dirname; unrar x -y \$x \$dirname; done"
