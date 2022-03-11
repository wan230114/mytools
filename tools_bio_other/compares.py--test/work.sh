###################
### compares.py
###################

# conda activate mytools

# 数据准备
mkdir -p datas
echo A B C D E F G |xargs -n 1  >datas/a1.txt
echo   B C D E F G |xargs -n 1  >datas/a2.txt
echo     C D E F G |xargs -n 1  >datas/a3.txt
echo       D E F G |xargs -n 1  >datas/a4.txt
echo         E F G |xargs -n 1  >datas/a5.txt
echo           F G |xargs -n 1  >datas/a6.txt
echo             G |xargs -n 1  >datas/a7.txt

# 1) 比较。直接给定文件参数, -o 未指定时 默认 --> des.xls
echo -e "\n\n"=== demo 1 ====
echo -e "\n$ compares.py  datas/* 
cat des.xls"
compares.py  datas/* 
cat des.xls

echo -e "\n\n"=== demo 2 ====
echo -e "\n$ compares.py  datas/a{3,2,4}.txt -o des2.xls
cat des2.xls"
compares.py  datas/a{3,2,4}.txt -o des2.xls
cat des2.xls

# 2) 比较
echo -e "\n\n"=== demo 3 ====
echo -e "\n$ ls  datas/*  >intable
compares.py -i intable -o des3.xls; cat des3.xls"
ls  datas/*  >intable
compares.py -i intable -o des3.xls
cat des3.xls


###################
### compare
###################
echo -e "\n\n"=== demo of compare ====
compare  datas/a1.txt  datas/a2.txt  datas/a3.txt
