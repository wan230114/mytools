# 该命令格式转换会保留图像大量白边
convert testdir-bak/test.svg testdir-bak/test.png
# 当文件数量过多时，如何批量去除呢？


# 实例1：对文件夹所有文件进行覆盖式白边裁剪
rm -r testdir1 ;  cp -r testdir-bak testdir1
/ifs/TJPROJ3/Plant/chenjun/software/python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tree/imgcut.py testdir1


# 实例2：对文件夹过滤png文件进行复制式白边裁剪(保留原文件，生成裁剪后新文件)
# 可选参数可以缩写为1个字母
rm -r testdir2 ;  cp -r testdir-bak testdir2
/ifs/TJPROJ3/Plant/chenjun/software/python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tree/imgcut.py testdir2 --filter png --bak
rm -r testdir2 ;  cp -r testdir-bak testdir2
/ifs/TJPROJ3/Plant/chenjun/software/python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tree/imgcut.py testdir2 -f png -b

# 实例3：对指定文件裁剪
rm -r testdir2 ;  cp -r testdir-bak testdir2
/ifs/TJPROJ3/Plant/chenjun/software/python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tree/imgcut.py testdir2/test.png

