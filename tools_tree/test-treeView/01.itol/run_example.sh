# 实例1：转换ceshi.tre为newname.svg输出至"out/aa"下
/ifs/TJPROJ3/Plant/chenjun/software/python3.5/bin/python3 /ifs/TJPROJ3/Plant/chenjun/mytools/itol/itol.py ceshi.tre out/aa/newname
# 实例2：转换ceshi.tre为newname.svg,pdf,png输出至"out/bb"下
/ifs/TJPROJ3/Plant/chenjun/software/python3.5/bin/python3 /ifs/TJPROJ3/Plant/chenjun/mytools/itol/itol.py ceshi.tre out/bb/newname --option "--format svg,pdf,png"

# 实例3：转换ceshi.tre为myname.svg、myname.pdf和myname.png输出至"out/"下
# 设置option参数：选择输出格式，使用圈形，显示支长
# 注意: option参数后面必须为一个完整参数。可用引号引起来, 或转义空格:"\ "
/ifs/TJPROJ3/Plant/chenjun/software/python3.5/bin/python3 /ifs/TJPROJ3/Plant/chenjun/mytools/itol/itol.py ceshi.tre out/myname \
    --option "
    --format svg,pdf,png,eer 
    --display_mode 2 
    --branchlength_display 1"
