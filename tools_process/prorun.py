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
import time
from datetime import datetime
from multiprocessing import Pool, Array


class RunSh(object):

    def __init__(self):
        self.folog = 'log.%s.%s' % (
            datetime.now().strftime('%Y-%m-%d_%H-%M-%S'), os.getpid())
        self.__dict__.update(self.fargv())
        self.logdir = os.path.basename(self.file_sh) + '.' + self.folog
        # self._shm = Array('i', [0, 0])
        # self._shm = [0, 0]
        print("  4、日志文件夹: %s" % self.logdir)
        # open(self.folog, 'w+').close()

    def fargv(self):
        parser = argparse.ArgumentParser(description='Process some integers.')
        parser.add_argument('file_sh', type=str,
                            help='输入需要运行的sh文件')
        parser.add_argument('-l', '--lineNUM', type=int, default=1,
                            help='line 每几行做一个运行的分割，默认1')
        parser.add_argument('-t', '--thread', type=int, default=1,
                            help='thread 用多少线程跑，默认1')
        parser.add_argument('-r', '--retry', type=int, default=0,
                            help='出错时重试的次数，默认0')
        parser.add_argument('-rt', '--interval_time', type=float, default=0,
                            help='出错时重试的间隔时间(秒)，默认0')
        # parser.add_argument('-o', '--logdir', type=str, default="",
        # help='输出日志文件夹的后缀, 默认为 脚本+.log')
        if len(sys.argv) == 1:
            parser.parse_args(['', '--help'])
            sys.exit()
        args = parser.parse_args()
        print("输入参数是:\n"
              "  1、文件: %(file_sh)s\n"
              "  2、每个进程运行的行数: %(lineNUM)s\n"
              "  3、进程数: %(thread)s"
              % args.__dict__, flush=True)
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
                Ldata = Llines[i:i+self.lineNUM]
                Ldatas.append(Ldata)
        # fprint(self.folog,'\n'.join([str(x) for x in Ldatas]))
        print('runstart>>>', flush=True)
        Ldatas_len = '%%0%dd' % len(str(int(len(Ldatas))))
        p = Pool(self.thread)
        for i, L_cmd in enumerate(Ldatas, start=1):
            # print(i, L_cmd)
            # self.sh(i, L_cmd, Ldatas_len, self.folog)
            args = (
                L_cmd,
                lineNUM,
                folog_pre,
                retry,
                interval_time) = (
                L_cmd,
                '(%s/%s)' % (Ldatas_len % i, len(Ldatas)),
                self.logdir+os.sep +
                    os.path.basename(self.file_sh)+Ldatas_len % i,
                self.retry,
                self.interval_time)
            with open(folog_pre, 'w') as fo:
                fo.write('\n'.join(L_cmd))
            p.apply_async(self.sh, args=args)
        p.close()
        p.join()
        # print(self._shm)
        # print(
        #     f'\n[CMD complete stat: '
        #     f'{self._shm[0]}/{self._shm[1]+self._shm[0]} '
        #     f'{self._shm[0]/self._shm[1]+self._shm[0]}')
        # if self._shm[1]:
        #     print('\033[1;5;37;41m[ALL CMD not complete.\033[0m\n')
        # else:
        #     print('\033[1;37;42m[ALL CMD complete.\033[0m')

    def sh(self, L_cmd, lineNUM, folog_pre, retry, interval_time=0):
        try:
            # print('hello')
            folog = folog_pre + '.' + self.folog
            num_len_line = len(str(len(L_cmd)))
            retry_raw = retry
            for num_line, line in enumerate(L_cmd, start=1):
                stat = 1
                retry = retry_raw
                while stat and retry >= 0:
                    isretry = ('\nRetrying time(%d/%d)\n' % (
                        retry_raw - retry, retry_raw)
                        if retry < retry_raw else '')
                    retry -= 1
                    t1 = datetime.now()
                    fprint(folog, isretry + '>>>[CMD Start Run. %s-%s  %s]   %s' %
                           (lineNUM, ('%%0%dd' % num_len_line) % num_line,
                            t1.strftime('%Y-%m-%d_%H:%M:%S'), line))
                    stat = os.system(line)
                    t2 = datetime.now()
                    # print("self._shm:", self._shm)
                    if stat:
                        # self._shm[0] += 1
                        fprint(folog, '\n\033[1;5;37;41m[CMD Run Failed.   %s-%s  %s (Time: %s)]  CMD: %s\033[0m\n' %
                               (lineNUM, ('%%0%dd' % num_len_line) % num_line,
                                t2.strftime('%Y-%m-%d_%H:%M:%S'),
                                t2-t1, line))
                        time.sleep(interval_time)
                    else:
                        # self._shm[1] += 1
                        fprint(folog, '\033[1;37;42m[CMD Run Success.  %s-%s  %s (Time: %s)]  CMD: %s\033[0m' %
                               (lineNUM, ('%%0%dd' % num_len_line) % num_line,
                                t2.strftime('%Y-%m-%d_%H:%M:%S'),
                                t2-t1, line))
        except Exception as ex:
            msg = "Error :%s" % ex
            fprint(folog, msg)


def fprint(fo, *t):
    with open(fo, 'a') as fo:
        s = ' '.join([str(x) for x in t])
        fo.write(s + '\n')
        fo.flush()
        print(s + '\n', flush=True, end='')


def main():
    # sys.argv = ['', r'E:\我的云同步\ALLdata\mytools\tools_bed\run\run-workdir\allstep.sh',
    #             '--line', '1', '--thread', '8']
    run = RunSh()
    run.fmain()


if __name__ == '__main__':
    main()
