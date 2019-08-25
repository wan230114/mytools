#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
用法：
python /home/chenjun/mytools/fas.py filename [argv]
[argv]
n  只统计总个数，默认缺省参数
y  输出细节
ys 输出细节并排序

快捷设置：在“~/.bashrc”中加入一行："alias fas="python /home/chenjun/mytools/fas.py "
之后可以直接：fas filename [argv]
"""
import time
import sys
from operator import itemgetter



def fPrint(fl, count): #
    global start, start2, p, allcount
    if p == 1:
        start = fl
        p *= -1
        if count == 0:
            return
        L.append([start2,count])
        allcount += count
    else:
        start2 = fl
        p *= -1
        L.append([start2,count])
        allcount += count

filename = sys.argv[1]
try:
    MOD = sys.argv[2]
except IndexError:
    MOD = "n"

print(">>>统计中...")
t0 = time.time()

file = open(filename)
count = 0
allcount = 0
p = 1
start = ""
start2 = ""
fl = ""
L=[]
maxlen=0

while True:
    try:
        data = file.next().strip()
        if data.startswith(">"):
            if MOD == "n":
                continue
            fl = data.replace(">", "")
            if maxlen<len(fl):
                maxlen=len(fl)
            fPrint(fl, count)
            count = 0
            continue
        elif data=='':
            continue
        elif data[0] in "AGTCNagtcn":
            count += len(data)
    except StopIteration:
        fPrint(fl, count)
        break

s = "%-"+str(maxlen)+"s"
if MOD == "ys":
    L = sorted(L, key=itemgetter(1))  #排序
if MOD != "n":
    for i in range(len(L)):
        # print(i[0],i[1])
        print s%L[i][0],L[i][1]

file.close()
print "总的序列数为：", allcount
print "运行结束，耗时%f秒" % (time.time() - t0)
