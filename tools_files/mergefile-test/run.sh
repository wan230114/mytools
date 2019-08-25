# 默认参数：第一个文件指定列合并相同值，合并的符号默认为空格，默认不输出键值未在第二个文件中匹配到的行
python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_files/mergefile.py \
		-f1 test1 1 -f2 test2 1 \
		-fo test.result \

# 修改默认符号
python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_files/mergefile.py \
		-f1 test1 1 -f2 test2 1 \
		-fo test.result1 \
		--sep ","

# 修改参数，输出键值未在第二个文件中匹配到的行
python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_files/mergefile.py \
		-f1 test1 1 -f2 test2 1 \
		-fo test.result2 \
		--sep "," \
		--showlost

# 不合并，按第一个文件顺序输出
python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_files/mergefile.py \
		-f1 test1 1 -f2 test2 1 \
		-fo test.result3 \
		--sep "," \
		--keep

echo
echo "------------show files------------"
head test*
