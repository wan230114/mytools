# 本程序用于计算gap的长度(即N的长度)，及其初始位置
# 设计思路重点：

import time

print(">>>运行中, 正在将文件写入答题主文件夹下的2.1work3.result.txt")
t0 = time.time()
filename = "Missing_File/Programming_exercise_1.data.fa"
# filename = "test.txt"
file = open(filename)
file2 = open("2.1work3.result.txt","w")
count = 0  # 用于记录序列位置
s = 0  # 用于记录gap的长度
sp = 0  # 用于记录gap的初始位置
start = ""
n = 0

while True:
    try:
        data = file.next().strip()
        n += 1
        if data.startswith(">"):
            start = data.replace(">", "")
            count = 0
            s = 0
            sp = 0
            continue
        # print(data, len(data))
        for i in data:
            count += 1
            if i == "N":
                if sp == 0:
                    sp = count
                s += 1
                # print("s:", s, "count:", count, "sp:", sp)
            elif (i != "N") & (sp != 0):
                # print(start, sp, sp + s - 1, s, sep='\t')
                file2.write("%s\t%d\t%d\t%d\n"%(start, sp, sp + s - 1, s))
                # print("第%d行："%n, start, sp, sp + s - 1, s, sep='\t')
                s = 0
                sp = 0
    except StopIteration:
        # print(start, sp, sp + s - 1, s, sep='\t') #因为N为文件结尾，后面没有触发打印的条件，故最后一次打印
        file2.write("%s\t%d\t%d\t%d\n"%(start, sp, sp + s - 1, s))
        break
print("运行结束，耗时%f秒" % (time.time() - t0))
