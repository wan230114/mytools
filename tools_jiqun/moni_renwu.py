# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2018-12-29 14:19:04
# @Last Modified by:   JUN
# @Last Modified time: 2019-10-11 17:49:08

# import os
import sys
import time
import subprocess


class CmdRunError(Exception):
    pass


def fmain(keyword):
    cmd1 = 'vjob'
    fo = open('moni_renwu.py.log_%s' % (keyword.replace('/', '_')), 'a')
    while True:
        # os.system('''q|grep qw|cut -d ' ' -f 1|sed 's#\.1##'|xargs -i qalter  -q plant.q {}''')
        # s = os.popen(cmd1 % keyword).read().strip()
        p = subprocess.Popen(cmd1, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        p_status = p.wait()
        if p_status:
            raise CmdRunError(
                '\n进程运行状态不为零, stat: %s\n'
                'logs:\n'
                '[out.o]:\n%s\n'
                '[out.e]:\n%s\n' % (p_status, output.decode(), err.decode()))
        out = '\n'.join([line for line in output.decode().split('\n') if keyword in line])
        info = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + \
            '    keyword: ' + keyword
        data = info + '\n' + out + '\n'
        fo.write(data)
        fo.flush()
        if not out:
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
