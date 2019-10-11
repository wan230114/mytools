# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2018-12-29 14:19:04
# @Last Modified by:   JUN
# @Last Modified time: 2019-10-11 17:04:08

# import os
import sys
import time
import subprocess


class CmdRunError(Exception):
    pass


def fmain(keyword):
    cmd1 = '''vjob|grep %s'''
    fo = open('moni_renwu.py.log_%s' % (keyword.replace('/', '_')), 'a')
    while True:
        # os.system('''q|grep qw|cut -d ' ' -f 1|sed 's#\.1##'|xargs -i qalter  -q plant.q {}''')
        # s = os.popen(cmd1 % keyword).read().strip()
        p = subprocess.Popen(cmd1 % keyword, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        p_status = p.wait()
        if p_status:
            print('进程运行状态不为零，stat:', p_status)
            raise CmdRunError('logs:\n[out.e]:\n%s\n[out.o]:\n%s\n' % (output, err))
        info = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + \
            '    keyword: ' + keyword
        data = info + '\n' + output.strip() + '\n'
        fo.write(data)
        fo.flush()
        if not output:
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
