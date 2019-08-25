# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-08 17:59:50
# @Last Modified by:   JUN
# @Last Modified time: 2019-02-20 08:58:14

import os
import sys
import argparse
import datetime
from multiprocessing import Pool


class runsh:

    def __init__(self):
        self.folog = 'run_multiProgress.log.%s.%s' % (str(datetime.datetime.now().strftime('%H:%M:%S.%f'))[:-3], os.getpid())
        open(self.folog, 'w+').close()
        self.fargv()

    def fargv(self):
        parser = argparse.ArgumentParser(description='Process some integers.')
        # parser.add_argument('integers', metavar='N', type=int, nargs='+',
        #                     help='an integer for the accumulator')
        # parser.add_argument('--sum', dest='accumulate', action='store_const',
        #                     const=sum, default=max,
        #                     help='sum the integers (default: find the max)')
        # fprint(args.accumulate(args.integers))
        parser.add_argument('file_sh', type=str,
                            help='输入需要运行的sh文件')
        parser.add_argument('-l', '--line', type=int,
                            help='line 每几行做一个运行的分割')
        parser.add_argument('-t', '--thread', type=int,
                            help='thread 用多少线程跑')
        if len(sys.argv) < 5:
            parser.parse_args(['', '--help'])
            sys.exit()
        args = parser.parse_args()
        self.Largs = [args.file_sh, args.line, args.thread]
        fprint(self.folog, "输入参数是:\n  1、文件: %s\n  2、每个进程运行的行数: %s\n  3、进程数: %s" % tuple(self.Largs))

    def fmain(self):
        file_sh, line, thread = self.Largs
        if not file_sh.endswith('.sh'):
            fprint(self.folog, 'WARNING: 输入文件不是sh文件，请注意输入文件是否正确')
        with open(file_sh) as fi:
            Ldatas = []
            Llines = fi.read().strip().split('\n')
            Llines = [x.strip() for x in Llines]
            for i in range(0, len(Llines), line):
                Ldata = []
                for j in range(line):
                    Ldata.append(Llines[i + j])
                Ldatas.append(Ldata)
        # fprint(self.folog,'\n'.join([str(x) for x in Ldatas]))
        fprint(self.folog, 'runstart>>>')
        p = Pool(thread)
        for i in Ldatas:
            # self.sh(i, self.folog,fprint)
            p.apply_async(self.sh, args=(i, self.folog))
        p.close()
        p.join()

    def sh(self, L, folog):
        try:
            # print('hello')
            for line in L:
                fprint(folog, '[CMD runing:] ' + line)
                if os.system(line):
                    fprint(folog, '[CMD命令执行出错 :] %s' % line)
                else:
                    fprint(folog, '[CMD命令执行成功 :] %s' % line)
        except Exception as ex:
            msg = "Error :%s" % ex
            fprint(msg)


def fprint(fo, *t):
    with open(fo, 'a') as fo:
        s = ' '.join([str(x) for x in t])
        fo.write(s + '\n')
        fo.flush()
        print(s)


def main():
    # sys.argv = ['', r'E:\我的云同步\ALLdata\mytools\tools_bed\run\run-workdir\allstep.sh',
    #             '--line', '1', '--thread', '8']
    run = runsh()
    run.fmain()


if __name__ == '__main__':
    main()
