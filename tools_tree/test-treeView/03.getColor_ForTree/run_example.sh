export PATH=/ifs/TJPROJ3/Plant/chenjun/software/python3.5/bin:$PATH

# 版本1
python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tree/getTree.py ceshi.tre M

# 版本2，最新版
# 实例1：选取以t为开头的基因为参考基因，转换树标记颜色
python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tree/getTree_fromFile.py ceshi.tre -mod zc t
# 实例2：选取以M为开头的基因为目标基因，除去目标基因为外的基因为参考基因，转换树标记颜色
python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tree/getTree_fromFile.py ceshi.tre -mod zm M
# 实例3：选取以文件file中的列表基因为参考基因，转换树标记颜色
python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tree/getTree_fromFile.py ceshi.tre -mod f cankao.list
