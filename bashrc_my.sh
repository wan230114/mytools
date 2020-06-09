########################################################
###################### 系统配置 ########################
########################################################

#################### Language set ######################
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
## PS1="\[\e[1;33m\][\u@\h:\[\e[1;34m\] \t \[\e[32m\]\w]\n\[\e[33m\]$\[\e[m\]"
PS1="\[\e[1;31m\][\u@\h:\[\e[1;31m\] \t \[\e[31m\]\w]\n\[\e[31m\]# \[\e[m\]"
PS1="\[\e[1;32m\][\u@\h:\[\e[1;36m\] \t \[\e[31m\]\w]\n\[\e[32m\]$ \[\e[m\]"

##################  常用命令  ########################
alias l="ls -lh"
alias ll="ls -lhrt"
alias lll="ls -l"
fcd(){ 
cd $1 && ls -lh 
}
alias c=fcd
alias vi="vim"
alias grep='grep --color'
alias les="less -S"
alias e="less -S"
alias ee="less -SN"
alias eee="less"
alias ca="cat"
alias vb="vim ~/.bashrc"
alias vbs="source ~/.bash_profile ~/.bashrc"
alias cr="crontab -e"

#####################################################
#################### mynote #########################
#####################################################
#tools_path="$( cd $(dirname $0) && pwd)"
tools_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
alias vb1="vim ${tools_path}/bashrc_my.sh "
alias vb2="vim ${tools_path}/bashrc_Tools.sh "
alias vbb="vim ${tools_path}/Note.sh "
alias cdcm="cd ${tools_path}/"
