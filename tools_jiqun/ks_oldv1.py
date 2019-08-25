# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-09 00:59:57
# @Last Modified by:   JUN
# @Last Modified time: 2019-04-16 03:04:36

import os
import sys

"""kPGID"""


def fmain(PGID):
    xjf = os.popen(
        'ps xjf|grep -v bash|grep -v mytools/ks.py|grep -v "grep %s"|grep %s' % (PGID, PGID)).read()
    # print(xjf.encode())
    Llines = xjf.strip().split('\n')
    Llines = [x.split() for x in Llines]
    # print(Llines)
    Lpid = [x[1] for x in Llines]
    ques = input('%s\n是否删除以上进程(y/n)？' % xjf)
    if ques == 'y':
        print('已使用`kill -s 9 PID`命令杀死以下PID的进程')
        print(Lpid)
        os.system('kill -s 9 ' + ' '.join(Lpid))


def main():
    if len(sys.argv) > 2 or len(sys.argv) == 1:
        print('参数错误，请输入可用`ps xjf`查看第3列PGID')
        sys.exit()
    PGID = sys.argv[1]
    fmain(PGID)

if __name__ == '__main__':
    main()
