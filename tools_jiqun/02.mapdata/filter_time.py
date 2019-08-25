# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-06-24 14:31:15
# @Last Modified by:   JUN
# @Last Modified time: 2019-06-24 15:31:07

import sys
import time
import datetime


def getdate(beforeOfDay):
    today = datetime.datetime.now()
    # print(today)
    # today = datetime.datetime.strptime("2019-06-24", "%Y-%m-%d")
    # 计算偏移量
    offset = datetime.timedelta(days=-beforeOfDay)
    # 获取想要的日期的时间
    re_date = (today + offset).strftime('%Y-%m-%d')
    return re_date


def isbeforetime(tar, new):
    '''判断是否在tar之前'''
    a = time.strptime(tar, "%Y-%m-%d")
    b = time.strptime(new, "%Y-%m-%d")
    return a < b


def fmain(finame, day):
    '''文件，日期'''
    tartime = getdate(int(day))
    with open(finame) as fi:
        for line in fi:
            Lline = line.strip().split('\t')
            if len(Lline) > 2:
                if isbeforetime(Lline[3].split()[0], tartime):
                    print(line, end="")
            else:
                print(line, end="")


def main():
    fmain(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()
