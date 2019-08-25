mails="chenjun4663@novogene.com,1170101471@qq.com"
source ./run_auto.sh.cfg

# 00) 初始化工具包路径
if [ "`ls /NJPROJ2/Plant/chenjun/mytools 2>/dev/null`" ]
then
    export PATH=/NJPROJ2/Plant/chenjun/software/Miniconda3/miniconda3/bin:$PATH
    tools_path="/NJPROJ2/Plant/chenjun/mytools"
else
    export PATH=/ifs/TJPROJ3/Plant/chenjun/software/Miniconda3/miniconda3/bin:$PATH
    tools_path="/ifs/TJPROJ3/Plant/chenjun/mytools"
fi

# 01) 处理和链接扫盘结果
mkdir 01.mapfile
cd 01.mapfile
ln -s ../xiajiALL.list
ln -s ../00.saopan/result.path
cut -f 2 result.path >lst.tmp
# 处理每一行为： 文库名 <\t> 路径
python3 ${tools_path}/tools_jiqun/02.mapdata/getlineWenku.py lst.tmp |cut -f 1,2 |sort|uniq >lst

# 02) merge查找
python3 ${tools_path}/tools_files/mergefile_V2.py \
    -f1 lst 1 \
    -f2 xiajiALL.list 10 \
    -fo lst.merge \
    --include \
    --sep "|" \
    --keep
cut -f 1,3- lst.merge >lst.merge.final--alltime

# 03) 日期筛选
# 筛选25天之前的文库（修改参数25）
python3 ${tools_path}/tools_jiqun/02.mapdata/filter_time.py lst.merge.final--alltime 25 >lst.merge.final--filter_time.1
# 得到25天之内的
comm lst.merge.final--filter_time.1 lst.merge.final--alltime -13 >lst.merge.final--filter_time.2
# 去除25天前中包含在25天内的项目，避免一个项目删一半，后面又要删一次，减少人力消耗
echo "grep -vf <(cut -f 6 lst.merge.final--filter_time.2|sort|uniq|awk NF) lst.merge.final--filter_time.1"|bash >lst.merge.final

# 04) 项目统计01，按项目统计文库数量。
python3 ${tools_path}/tools_jiqun/02.mapdata/get_tiqu_final.py lst.merge.final >lst.merge.tiqu

# 05) 项目统计02，在01的基础上加入文件大小统计
    # 输入：tiqu文件，第4列项目名，下机文库对应信息，文件大小列表。
    # 输出：下机文库对应信息--tongji.html/--tongji.txt/--tongji.xlsx
python3 ${tools_path}/tools_jiqun/02.mapdata/get_xiangmu_size_FOR_tiqu.py lst.merge.tiqu  4  lst.merge.final  result.path

# 发送通知邮件，根据实际使用情况，更改邮箱
python ${tools_path}/sendmail/sendmail_novomail.py ${mails} -c "`cat lst.merge.final--tongji.html`"

# 清空文件，占用太大
>xiajiALL.list

cd -
