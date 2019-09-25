git add -A
git commit -a -m "`date "+%F  %H:%M:%S"` $1"
git push -u origin master        # 上传仓库到码云
