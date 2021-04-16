########################################################
###################### 系统配置 ########################
########################################################

#################### Language set ######################
#export LC_ALL="en_US.utf8"
#export LANG="en_US.utf8"

#export LC_ALL="zh_CN.utf8"
#export LANG="zh_CN.utf8"

######## User specific aliases and functions ########
export HISTTIMEFORMAT='%F %T '
export HISTSIZE=100000
export HISTFILESIZE=100000
export HISTCONTROL=erasedups
export HISTIGNORE='pwd:ls:ls -ltr:cd:ll:history:'
export PROMPT_COMMAND="history -a"
export HISTFILE=~/.bash_history
alias h="history |less -S"
alias hh="history |grep -e \"[0-9] cd.* /\"|tail -20"
alias hhh="h|grep -e \"[0-9] *nohup*\" |tail -20"
alias ht="h|cut -f 5- -d ' '|uniq"

#################### Color set ######################
export CLICOLOR=1
export LSCOLORS=gxfxaxdxcxegedabagacad
## 30黑,31红,32绿, 33黄,34蓝,35洋红,36青,37白
#PS1="\[\e[1;33m\][\u@\h:\[\e[1;34m\] \t \[\e[32m\]\w]\n\[\e[33m\]$\[\e[m\]"
#PS1="\[\e[1;31m\][\u@\h:\[\e[1;31m\] \t \[\e[31m\]\w]\n\[\e[31m\]# \[\e[m\]"  # root red color

## 30黑,31红,32绿, 33黄,34蓝,35洋红,36青,37白
## 30 black, 31 red, 32 green, 33 yellow, 34 blue, 35 magenta, 36 cyan, 37 white
PS1="\[\e[1;32m\][\u@\h:\[\e[1;36m\] \t \[\e[31m\]\"\w/\"]\n\[\e[32m\]$ \[\e[m\]"
PS1=`echo ${PS1}|sed 's#"\\\\w/"#"$PWD/"#'`  # "~/" --> "/home/user/"

##################  常用命令  ########################
alias l="ls -lhrt"
alias ll="ls -lh"
alias lll="ls -l"
alias vi="vim"
alias grep='grep --color'
alias les="less -S"
alias e="less -S"
alias ee="less -SN"
alias eee="less"
alias ca="cat"
alias vb="vim ~/.bashrc"
alias vbs="source ~/.bashrc"
alias cr="crontab -e"

ff_function(){
if [ "$@" ]; then
  find $PWD -name "$@"
else
  find -L .|grep -v -x -f <(find -L . -type d)|sort
fi
}
alias ff=ff_function

#alias cp="cp -iv"
alias mv="mv -iv"
#alias rm="rm -iv"

#####################################################
#################### mynote #########################
#####################################################
#tools_path="$( cd $(dirname $0) && pwd)"
tools_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
alias vb1="vim ${tools_path}/bashrc_my.sh "
alias vb2="vim ${tools_path}/bashrc_Tools.sh "
alias vbb="vim ${tools_path}/Note.sh "
alias cdcm="cd ${tools_path}/"

#
alias vc="vim ~/.ssh/config"

# 
alias sc='conda deactivate; conda activate '

###  路径管理工具  ###
# 用于返回当前文件(夹)绝对路径
pwdfile(){
	if [ "`echo $@`" ]; then
		#for idx in $(seq $#); do eval echo `pwd`/"$"$idx; done
		#echo -e $@|while read x; do echo `pwd`/$x; done
        for x in `echo -e "$@"`; do echo `pwd`/$x; done
	else
        if [ "`ls|wc -l`" -gt "0" ] ;then ls -trd *|while read x; do echo `pwd`/$x; done; fi
	fi
}
alias f=pwdfile  # 用于返回当前文件夹某文件或目录的路径, f [file/dir] [file/dir]...
realpath_func(){
    if [ "`echo $@`" ]; then
        for idx in $(seq $#); do eval "realpath \${$idx}"; done
    else
        if [ "`ls|wc -l`" -gt "0" ] ;then ls -trd *|while read x; do realpath $x; done;fi
    fi
}
alias r="realpath_func "
# 用于快速切换目录用
ffcd(){
    if [ "$1" ]; then if sh -c "cd $1 2>/dev/null" ; then cd $1 && l; else cd `dirname $1` && l ; fi ; else cd . && l; fi
}
alias c=ffcd

