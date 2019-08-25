# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2018-12-27 13:50:49
# @Last Modified by:   JUN
# @Last Modified time: 2019-04-23 11:42:24


import os
import sys
import datetime
import time
import argparse


def fargv():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''本程序用于生成md5和checksize
  使用方法：
  python3 md5q.py [--option OPTION]''',
        epilog="""
设置快捷方式：
  echo alias md5q=\\"/ifs/TJPROJ3/Plant/chenjun/mytools/md5q.sh\\" >>~/.bashrc; source ~/.bashrc
示例：
  python md5q.py
  python md5q.py -m 1170101471@qq.com
  python md5q.py -t 200
  python md5q.py -t 200 -m 1170101471@qq.com
        """)
    parser.add_argument('--thread', '-t', type=int, default=100,
                        help='可选参数，需要使用的进程数，默认投递集群100个任务')
    parser.add_argument('--mail', '-m', type=str, default=None,
                        help='可选参数，邮箱')
    parser.add_argument('--log', '-l', type=str, default=None,
                        help='可选参数，自定义日志名')
    parser.add_argument('--checksize', '-c', action='store_true', default=False,
                        help='可选参数，自定义日志名')
    args = parser.parse_args()
    Targs = (args.thread, args.mail, args.log, args.checksize)
    if not args.log:
        args.log = 'temp_checkdir_%s-%s' % (
            str(datetime.datetime.now().strftime('%H.%M.%S.%f'))[:-3], os.getpid())
    print("--------------------------")
    print("输入参数是:\n1、进程数: %s\n2、提醒邮箱: %s\n3、日志名: %s\n4、只checksize: %s" % Targs)
    print("--------------------------\n")
    return Targs[0], Targs[1], Targs[2], Targs[3]


def jg():
    if os.system('cd /ifs/TJPROJ3/ 2>/dev/null'):
        s = 'nj'
    else:
        s = 'tj'
    return s


def fmain(threadx, mail, log, checksize=False):
    t00 = time.time()
    print('> 正在获取当前文件夹 %s 所有文件路径...' % (os.getcwd()))
    t0 = time.time()
    s_files = os.popen("".join(["find -L ./ -type f|cat|",
                                "awk '!/.\/md5.txt/'|",
                                "awk '!/.\/checkSize.xls/'"])).read()
    Lfiles = s_files.strip().split('\n')
    print('获取结束，耗时%s秒' % (time.time() - t0))
    jq = jg()
    if jq == "tj":
        qsub_sge = "perl /PUBLIC/software/DENOVO/bio/annotation/pipeline_v2.0/scripts/qsub-sge.pl "
        resource = "--resource vf=0.2G:p=1 "
    else:
        qsub_sge = "perl /NJPROJ3/Plant/share/modules/current/commonTools/00.bin/qsub-sge.pl "
        resource = "--resource vf=0.2G,p=1 "
    pwd = os.getcwd()
    if checksize == False:
        print('> 正在以 %s qsub进程 计算所有文件的md5值...' % threadx)
        t0 = time.time()
        os.system('mkdir -p %s/tmp' % log)
        with open(os.path.join(log, 'check.sh'), 'w') as fo:
            for i, fpath in enumerate(Lfiles):
                fo.write('cd %s && md5sum %s >%s/tmp/%s\n' % (pwd, fpath, log, i))
        os.system(''.join(['cd %s && ' % (log),
                           qsub_sge,
                           '--interval 10 ',
                           '--maxjob %s ' % threadx,
                           '--convert no ',
                           resource,
                           'check.sh'
                           ]))
        os.system('cat %s/tmp/* >md5.txt' % log)
        print('计算结束，耗时%s秒' % (time.time() - t0))

    print('> 正在获取文件夹大小...')
    t0 = time.time()
    peer = 0
    with open('checkSize.xls', 'w') as fo:
        if checksize == False:
            fo.write('\t'.join([str(os.path.getsize('./md5.txt')), './md5.txt']) + '\n')
        for path in Lfiles:
            try:
                fo.write('\t'.join([str(os.path.getsize(path)), path]) + '\n')
            except FileNotFoundError:
                print('统计过程中文件%s被删除' % (path))
                peer = 1
    print('获取结束，耗时%s秒' % (time.time() - t0))
    if (os.popen('cat %s/check.sh.*.log' % log).read().strip() != "All jobs finished!") or (peer == 1):
        print('统计过程中有报错，请于当前目录查看日志文件夹: %s/%s' % (pwd, log))
        os.system('echo cat check.sh.*.qsub/work*.sh.e* >view-err.sh')
        os.system('ln -s ~/tmplog/%s %s/' % (log, log))
        os.system('cat %s/%s' % (log, log))
        os.system('echo cat %s/%s >view-log.sh' % (log, log))
    else:
        os.system('rm %s -r' % log)

    print('> 正在对md5.txt、checkSize.xls进行排序...')
    t0 = time.time()
    os.system('sort -k2 md5.txt -o md5.txt')
    os.system('sort -k2 checkSize.xls -o checkSize.xls')
    print('排序结束，耗时%s秒' % (time.time() - t0))

    os.system('sh /ifs/TJPROJ3/Plant/chenjun/mytools/other/getlog.sh')
    print('\n运行结束，已于当前文件夹写入 md5.txt checkSize.xls ，耗时%s秒' % (time.time() - t00))
    if mail:
        os.system(
            'python /ifs/TJPROJ3/Plant/chenjun/mytools/sendmail.py %s -c "[md5, checkSize生成完毕，速速查看]\npath: %s"' % (mail, pwd))


def main():
    # sys.argv = ['','--help']
    threadx, mail, log, checksize = fargv()
    fmain(threadx, mail, log, checksize)


if __name__ == '__main__':
    main()


def GetFileMd5(filename):
    pass
    # Linux下运算时间大约长到1.2倍，该函数被遗弃
    # if not os.path.isfile(filename):
    #     return
    # myhash = hashlib.md5()
    # f = open(filename, 'rb')
    # while True:
    #     # b = f.read(8096)
    #     b = f.read(40960)
    #     if not b:
    #         break
    #     myhash.update(b)
    # f.close()
    # return myhash.hexdigest()
