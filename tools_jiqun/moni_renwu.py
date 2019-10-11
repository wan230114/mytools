# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2018-12-29 14:19:04
# @Last Modified by:   JUN
# @Last Modified time: 2019-10-11 15:32:31

import os
import sys
import time


def fmain(keyword):
    cmd1 = '''vjob|grep %s'''
    fo = open('moni_renwu.py.log_%s' % (keyword.replace('/','_')), 'a')
    while True:
        # os.system('''q|grep qw|cut -d ' ' -f 1|sed 's#\.1##'|xargs -i qalter  -q plant.q {}''')
        s = os.popen(cmd1 % keyword).read().strip()
        info = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + \
            '    keyword: ' + keyword
        data = info + '\n' + s + '\n'
        fo.write(data)
        fo.flush()
        if not s:
            break
        time.sleep(300)
    fo.close()


def main():
    if len(sys.argv) == 1:
        print("缺少关键词参数")
        sys.exit()
    keyword = sys.argv[1]
    fmain(keyword)


if __name__ == '__main__':
    main()
