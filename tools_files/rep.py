# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  wan230114@qq.com
# @Date:   2018-02-26
# @Last Modified by:   JUN
# @Last Modified time: 2018-12-12 17:51:29

shelp = '''
功能：
    用自定义的替换列表，替换原文件中某一列的旧名字为新名字（并输出未替换成功的行信息）
使用方法：
    python  rep.py  listfile  oldfile  newfile  Num
    参数说明: 
    listfile 对应替换列表列表，每一行必须为 “ 原名字+\\t+新名字 ”，\\t必须为tab
    oldfile  待替换源文件，源文件需以\\t为列分隔
    newfile  替换的新文件名字
    Num      替换源文件的第几列，以\\t为列分隔的列数，从1开始
快捷设置：
    alias rep="python /ifs/TJPROJ3/Plant/chenjun/mytools/rep.py "

注意事项：
    替换那一列名字的首末端不能出现空格，程序会自动去除首末尾空格

'''
# 旧使用方法：
#     将以下文件放入同一文件夹：
#     运行run.py得到新文件file_new.txt

import os
import sys
import time


def replace_list(Largv):
    try:
        list_name, old_name, new_name, Num = Largv[1:]
    except ValueError:
        print(Largv[1:])
        print(shelp)
        sys.exit()
    t0 = time.time()
    print("( start at time %s )" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    print("列表文件: %s" % list_name)
    print("输入文件: %s" % old_name)
    print("输出文件: %s" % new_name)

    fi_list = open(list_name, 'r')
    fi = open(old_name, 'r')
    Num = int(Num) - 1
    fo = open(new_name, 'w')

    # 1）处理list，生成字典
    print('>>> 建立索引中...')
    Dlist = {}
    for line in fi_list:
        Lline = line.split()
        Lline = [x.strip() for x in Lline]
        Dlist[Lline[0]] = Lline[1]
    print('>>> 已建立索引, 即将开始替换...')
    # 2）替换文件
    key = ''
    cn = 0
    s_WARNING = ''
    neer = 0
    for line in fi:
        cn += 1
        Lline = line.rstrip().split('\t')
        try:
            key = Lline[Num]
            keyValue = Dlist[key]
        except KeyError:
            fo.write('\t'.join(Lline) + '\n')
            neer += 1
            s_WARNING += 'WARNING %s: 跳过第 %s 行替换，列表中值 %s 不存在\n' % (neer, cn, key)
            continue
        Lline[Num] = key.replace(key, keyValue)
        fo.write('\t'.join(Lline) + '\n')
    if s_WARNING:
        print('----------------------\n%s----------------------' % s_WARNING)
    try:
        print('>>> 替换完毕! 最后一次替换是将"%s"替换为"%s"\n进行了%d次替换，请查看新文件: %s' % (key, Dlist[key], cn, new_name))
    except KeyError:
        print('Error :替换失败！请检查list列表文件与待替换列是否有对应关系')
        sys.exit()
    print("运行结束，耗时%s秒" % (time.time() - t0))
    print("( Finish at time %s )\n\n\n\n" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    fi_list.close()
    fi.close()
    fo.close()

if __name__ == '__main__':
    # sys.argv = ['', 'dangshan.list','dangshan.final.annotation.xls','1', 'fo.txt']
    # os.chdir('my_testfile')
    # sys.argv = ['','my_testfile/repLIST.txt','my_testfile/repFILE.txt','my_testfile/repFILE.txt.new','1']
    replace_list(sys.argv)
