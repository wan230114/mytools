# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2018-12-29 14:22:52
# @Last Modified by:   JUN
# @Last Modified time: 2019-04-16 04:02:43


import os
import sys
import time


def jg():
    if os.system('cd /ifs/TJPROJ3/ &>/dev/null'):
        s = 'nj'
    else:
        s = 'tj'
    return s


def fmain(keyword, mod, lll, jg):
    L = os.popen('/home/leiyang/local/bin/cx').read().split('\n')
    jiedian = set([x.split('\t')[-1] for x in L])

    filelog = 'moni_qalter.py.log.%s.%s' % (keyword, mod)
    fo = open(filelog.replace('/', '-'), 'a')

    if jg == 'tj':
        path_perl = '/PUBLIC/software/public/System/Perl-5.18.2/bin'
        path_vjob = '''/home/leiyang/local/bin'''
    else:
        path_perl = '/NJPROJ2/Crop/share/software/Perl-5.18.2/bin'
        path_vjob = '''/NJPROJ2/home/zhangchunliu/bin'''
    global stop_single
    stop_single = 0

    def f(path_perl, path_vjob, keyword, lll):
        def do(qqq):
            s = os.popen('''%s/perl %s/vjob |grep %s|grep qw|cut -d ' ' -f 1|sed 's#\\.1##'|xargs -i qalter %s %s {}''' % (
                path_perl, path_vjob, keyword, lll, qqq)).read()
            fo.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                     '   %s   %s   %s\n' % (keyword, qqq, lll))
            fo.write(s.strip() + '\n')
            fo.flush()
            global stop_single
            if s:
                stop_single = 0
            else:
                stop_single += 1
            time.sleep(120)
        return do
    do = f(path_perl, path_vjob, keyword, lll)
    while True:
        if mod == '1':
            for line in ['plant.q', 'plant1.q', 'plant2.q', 'pub.q',  'novo.q', 'all.q']:
                if line in jiedian:
                    do(' -q ' + line)
            if stop_single > 720:
                break
        elif mod == '2':
            do(' -q tjsmp01_1024.q -P smp1024 ')
            do(' -q tjsmp03_1024.q -P smp1024 ')
            do(' -q tjsmp14_512.q -P smp512')
            do(' -q tjsmp07_1024.q -P smp1024 ')
            do(' -q tjsmp11_1024.q -P smp1024 ')
            do(' -q tjsmp14_512.q -P smp512')
            if stop_single > 720:
                break
        elif mod == '3':
            for line in ['plant.q', 'plant1.q', 'plant2.q', 'pub.q',  'novo.q', 'all.q']:
                if line in jiedian:
                    do(' -q ' + line)
            do('-q joyce.q -P joyce')
            do(' -q tjsmp01_1024.q -P smp1024 ')
            do(' -q tjsmp03_1024.q -P smp1024 ')
            do(' -q tjsmp07_1024.q -P smp1024 ')
            do(' -q tjsmp11_1024.q -P smp1024 ')
            do(' -q tjsmp14_512.q -P smp512 ')
            if stop_single > 720:
                break
    fo.close()


def printhelp():
    print("[help:]",
          "usage: moni_qalter.py keyword mod [lll]",
          "keyword: vjob能grep的关键词",
          "mod: 1/2/3 (小节点/大节点/所有节点)", sep='\n')
    sys.exit()


def main():
    if len(sys.argv) <= 2:
        print("缺少关键词参数\n")
        printhelp()
    keyword, mod = sys.argv[1:3]
    try:
        lll = sys.argv[3]
    except Exception:
        lll = ""
    if mod not in {'1', '2', '3'}:
        print('mod有误')
        printhelp()
    fmain(keyword, mod, lll, jg())

if __name__ == '__main__':
    main()
