# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-09 00:59:57
# @Last Modified by:   JUN
# @Last Modified time: 2019-03-06 10:23:01

import os
import sys

"""jobID"""


def fmain(jobID):
    xjf = os.popen("vjob|grep %s" % jobID).read()
    # print(xjf.encode())
    Llines = xjf.strip().split('\n')
    Llines = [x.split('.') for x in Llines]
    # print(Llines)
    Lid = [x[0] for x in Llines]
    ques = input('%s\n是否删除以上任务(y/n)？' % xjf)
    if ques == 'y':
        print('已使用`qdel jobID1 jobID2 ...`命令杀死以下jobID的任务')
        print(Lid)
        print('CMD running:', 'qdel', ' '.join(Lid))
        os.system('qdel ' + ' '.join(Lid))


def main():
    jobID = sys.argv[1]
    if len(sys.argv) > 2:
        print('参数错误，请输入可用`vjob`查看任务行中的关键词')
    fmain(jobID)

if __name__ == '__main__':
    main()
