echo '''
本工具用于可视化某个文件夹(包含子文件夹)下指定格式的文件于单个网页，目前支持png,pdf,svg
输入:
    参数1：当前路径的文件夹inputdir
    参数2：预可视化的文件类型，可选择：png / pdf / svg
输出:
    filedir-*View.html
'''

# 定义输入的文件夹
# dirname=$1
dirname=filedir

# 生成预览$dirname文件夹中所有.png的网页
python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tree/imgdirView.py $dirname/ png
# 生成预览$dirname文件夹中所有.pdf的网页
python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tree/imgdirView.py $dirname/ pdf
# 生成预览$dirname文件夹中所有.svg的网页
python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tree/imgdirView.py $dirname/ svg

