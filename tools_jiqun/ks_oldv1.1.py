# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-09 00:59:57
# @Last Modified by:   JUN
# @Last Modified time: 2019-06-11 15:51:56

import os
import sys

"""keyword找寻关键字的所有父子进程"""


def fmain(keyword):
    xjf = os.popen('''ps xjf|grep -v mytools/tools_jiqun/ks.py''').read()
    Llines = []
    S_PGID = set()
    for line in xjf.strip().split('\n'):
        Lline = line.strip().split()
        # print(Lline)
        Llines.append([Lline[2], Lline[1], line])
        if keyword in line:
            S_PGID.add(Lline[2])
    Lresult = []
    Lpid = []
    for PGID in S_PGID:
        for PGID2, pid, line in Llines:
            if PGID2 == PGID:
                Lresult.append(line)
                Lpid.append(pid)
    # xjf = os.popen('''tmp="`ps xjf`"; echo -e "$tmp"|grep -v "\\-bash"|grep -v mytools/ks.py|grep %s|awk '{print $3}'|sort|uniq'''%s).read()
    # 'ps xjf|grep -v bash|grep -v mytools/ks.py|grep -v "grep %s"|grep %s' % (keyword, keyword)).read()
    xjf = '\n'.join(Lresult)
    ques = input('%s\n是否删除以上进程(y/n)？' % xjf)
    if ques == 'y':
        print('已使用`kill -s 9 PID`命令杀死以下PID的进程')
        print(Lpid)
        os.system('kill -s 9 ' + ' '.join(Lpid))


def main():
    if len(sys.argv) > 2 or len(sys.argv) == 1:
        print('参数错误，请输入可用`ps xjf`查看第3列keyword')
        sys.exit()
    keyword = sys.argv[1]
    fmain(keyword)

if __name__ == '__main__':
    main()
