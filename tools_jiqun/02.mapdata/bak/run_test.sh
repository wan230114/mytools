# 开发中（已丢弃，有时候没有大小统计文件，耦合度太高，不好用）
python3 ../get_xiangmu_size.py lst.merge.tiqu 4 lst.merge.final result.path.size


python3 quite.py nj.list.tmp 1 xiajiALL.list 10 >nj.list.merge


# # 统计
# awk -F '\t' '{OFS="\t"; print $1,$2,$25,$24,$5,$6}' lst.merge.final >lst.merge.tiqu2
# cat lst.merge.tiqu2|cut -f3-6 |sort |uniq -c |sort -k1,1nr >lst.merge.tiqu3
# # 格式化lst.merge.tiqu，合并相同项目名
# python3 ${tools_path}/tools_jiqun/02.mapdata/get_tiqu_final.py lst.merge.tiqu3 >lst.merge.tiqu
