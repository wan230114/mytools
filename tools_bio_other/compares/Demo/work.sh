# 数据准备
mkdir -p datas
echo A B C D E F G |xargs -n 1  >datas/a1.txt
echo   B C D E F G |xargs -n 1  >datas/a2.txt
echo     C D E F G |xargs -n 1  >datas/a3.txt
echo       D E F G |xargs -n 1  >datas/a4.txt
echo         E F G |xargs -n 1  >datas/a5.txt
echo           F G |xargs -n 1  >datas/a6.txt
echo             G |xargs -n 1  >datas/a7.txt

head datas/*

# 1) 比较。直接给定文件参数, -o 未指定时 默认 --> des.xls
python  ../compares.py  datas/*
# 2) 比较
ls  datas/*  >intable
python  ../compares.py -i intable -o des2.xls
