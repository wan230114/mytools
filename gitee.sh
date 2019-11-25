# https://gitee.com/wan230114/mytools.git
echo 拉取中...
sh Get_gitee.sh

echo
echo 上传中...
git add -A
git commit -a -m "`date "+%F  %H:%M:%S"` $1"
git push -u origin master        # 上传仓库到码云
