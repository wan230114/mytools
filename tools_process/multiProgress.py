# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-08 17:59:50
# @Last Modified by:   JUN
# @Last Modified time: 2019-02-20 08:58:14

"""
待改进的问题：
- 每一个命令的 .o 和 .e 单独分离开来
- 当line参数大于1时，考虑是否让报错就终止向下运行。

- 最后对所有的运行结果进行一个数据统计，如果成功，打印所有执行成功的信息
  - 如何统计？
  - 方案1：可以日志分为2个文件：一个执行成功的，一个执行失败的。
         最后运行完直接统计文件行数（不够健壮）
  - 方案2：使用共享内存进行计数，使用subprocess来执行shell进程管理。
"""

import os
import sys
import argparse
import datetime
from multiprocessing import Pool


class RunSh(object):

    def __init__(self):
        self.folog = 'log.%s.%s' % (
            str(datetime.datetime.now().strftime('%m-%d_%H-%M-%S')), os.getpid())
        self.__dict__.update(self.fargv())
        if not self.logdir:
            self.logdir = self.file_sh + '.log'
        # open(self.folog, 'w+').close()

    def fargv(self):
        parser = argparse.ArgumentParser(description='Process some integers.')
        parser.add_argument('file_sh', type=str,
                            help='输入需要运行的sh文件')
        parser.add_argument('-l', '--lineNUM', type=int, default=1,
                            help='line 每几行做一个运行的分割，默认1')
        parser.add_argument('-t', '--thread', type=int, default=4,
                            help='thread 用多少线程跑，默认4')
        parser.add_argument('-o', '--logdir', type=str, default="",
                            help='输出日志文件夹的后缀, 默认为 脚本+.log')
        if len(sys.argv) == 1:
            parser.parse_args(['', '--help'])
            sys.exit()
        args = parser.parse_args()
        print("输入参数是:\n"
              "  1、文件: %(file_sh)s\n"
              "  2、每个进程运行的行数: %(lineNUM)s\n"
              "  3、进程数: %(thread)s\n"
              "  4、日志文件夹: %(logdir)s" %
              args.__dict__, flush=True)
        return args.__dict__

    def fmain(self):
        if not os.path.exists(self.logdir):
            os.mkdir(self.logdir)
        if not self.file_sh.endswith('.sh'):
            print('WARNING: 输入文件不是sh文件，请注意输入文件是否正确', flush=True)
        with open(self.file_sh) as fi:
            Ldatas = []
            Llines = fi.read().strip().split('\n')
            Llines = [x.strip() for x in Llines]
            for i in range(0, len(Llines), self.lineNUM):
                Ldata = []
                for j in range(self.lineNUM):
                    Ldata.append(Llines[i + j])
                Ldatas.append(Ldata)
        # fprint(self.folog,'\n'.join([str(x) for x in Ldatas]))
        print('runstart>>>', flush=True)
        Ldatas_len = '%%0%dd' % len(str(int(len(Ldatas))))
        p = Pool(self.thread)
        for i, L_cmd in enumerate(Ldatas, start=1):
            # print(i, L_cmd)
            # self.sh(i, L_cmd, Ldatas_len, self.folog)
            p.apply_async(self.sh, args=(
                L_cmd, Ldatas_len % i,
                self.logdir+os.sep+self.file_sh+Ldatas_len % i+'.'+self.folog))
        p.close()
        p.join()

    def sh(self, L_cmd, lineNUM, folog):
        try:
            # print('hello')
            for line in L_cmd:
                fprint(folog,     '> [CMD Start Run. %s] %s' % (lineNUM, line))
                if os.system(line):
                    fprint(folog, '[CMD Run Failed.  %s] %s' %
                           (lineNUM, line))
                else:
                    fprint(folog, '[CMD Run Success. %s] %s' %
                           (lineNUM, line))
        except Exception as ex:
            msg = "Error :%s" % ex
            fprint(folog, msg)


def fprint(fo, *t):
    with open(fo, 'a') as fo:
        s = ' '.join([str(x) for x in t])
        fo.write(s + '\n')
        fo.flush()
        print(s, flush=True)


def main():
    # sys.argv = ['', r'E:\我的云同步\ALLdata\mytools\tools_bed\run\run-workdir\allstep.sh',
    #             '--line', '1', '--thread', '8']
    run = RunSh()
    run.fmain()


if __name__ == '__main__':
    main()
