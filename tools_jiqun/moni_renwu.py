# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2018-12-29 14:19:04
# @Last Modified by:   JUN
# @Last Modified time: 2019-03-27 11:26:22

import os
import sys
import time


def fmain(mail, keyword, jg):
    if jg == 'tj':
        cmd1 = '''/home/leiyang/local/bin/vjob|grep %s'''
        cmd2 = 'python /ifs/TJPROJ3/Plant/chenjun/mytools/sendmail.py %s -c 监控任务%%s已跑完' % mail
    else:
        cmd1 = '''/NJPROJ2/Crop/share/software/Perl-5.18.2/bin/perl /NJPROJ2/home/zhangchunliu/bin/vjob|grep %s'''
        cmd2 = 'python /NJPROJ2/Plant/chenjun/mytools/sendmail.py %s -c 监控任务%%s已跑完' % mail
    fo = open('moni_renwu.py.log_%s' % (keyword.replace('/','_')), 'a')
    while True:
        # os.system('''q|grep qw|cut -d ' ' -f 1|sed 's#\.1##'|xargs -i qalter  -q plant.q {}''')
        s = os.popen(cmd1 % keyword).read().strip()
        info = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + \
            '    keyword: ' + keyword
        data = info + '\n' + s + '\n'
        # print(data)
        fo.write(data)
        fo.flush()
        if not s:
            os.system(cmd2 % keyword)
            break
        time.sleep(300)
    fo.close()


def jg():
    if os.system('cd /ifs/TJPROJ3/'):
        s = 'nj'
    else:
        s = 'tj'
    return s


def main():
    if len(sys.argv) == 1:
        print("缺少关键词参数")
        sys.exit()
    mail, keyword = sys.argv[1:3]
    fmain(mail, keyword, jg())


if __name__ == '__main__':
    main()
