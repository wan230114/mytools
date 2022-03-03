# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-08 17:59:50
# @Last Modified by:   JUN
# @Last Modified time: 2019-02-20 08:58:14

"""
version: 2.0, 完成对任务的执行状态统计。

待改进的问题：
- 每一个命令的 .o 和 .e 考虑需要单独分离开来？不必
- 块内报错即停止, 考虑是否让报错就终止向下运行。 不考虑，强制终止

- 最后对所有的运行结果进行一个数据统计, 如果成功, 打印所有执行成功的信息
  - 如何统计？
  - 方案1：可以日志分为2个文件：一个执行成功的, 一个执行失败的。
         最后运行完直接统计文件行数（不够健壮）
  - 方案2：使用共享内存进行计数, 使用subprocess来执行shell进程管理。
          程序编写有一定难关需要攻克。
  - 方案3：按返回值进行判断 [当前采用]
"""

import os
import sys
import argparse
import time
from datetime import datetime
from multiprocessing import Pool


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
                            help='line 每几行做一个运行的分割, 默认1')
        parser.add_argument('-t', '--thread', type=int, default=1,
                            help='thread 用多少线程跑, 默认1')
        parser.add_argument('-s', '--split_env', action="store_true",
                            help='每一个分割命令的块内, 是否需要独立当前环境运行')
        parser.add_argument('-r', '--retry', type=int, default=0,
                            help='出错时重试的次数, 默认0')
        parser.add_argument('-rt', '--interval_time', type=float, default=0,
                            help='出错时重试的间隔时间(秒), 默认0')
        parser.add_argument('-b', '--breakpoint_run', type=float, default=0,
                            help='(准备开发) 断点续跑功能，初步设想日志文件或者json记录')
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
            print('WARNING: 输入文件不是sh文件, 请注意输入文件是否正确', flush=True)
        with open(self.file_sh) as fi:
            L_CMDs = []
            Llines = fi.read().strip().split('\n')
            Llines = [x.strip() for x in Llines]
            for i in range(0, len(Llines), self.lineNUM):
                L_CMD = Llines[i:i+self.lineNUM]
                L_CMDs.append(L_CMD)
        # fprint(self.folog,'\n'.join([str(x) for x in L_CMDs]))
        print('runstart>>>', flush=True)
        L_CMDs_len = '%%0%dd' % len(str(int(len(L_CMDs))))
        p = Pool(self.thread)
        L_p = []
        for i, L_CMD in enumerate(L_CMDs, start=1):
            # print(i, L_CMD)
            # self.sh(i, L_CMD, L_CMDs_len, self.folog)
            L_CMD = L_CMD
            lineNUM = f'{len(L_CMDs)}-{L_CMDs_len % i}'
            folog_pre = os.path.join(
                self.logdir,
                os.path.basename(os.path.splitext(self.file_sh)[0]) +
                "." + (L_CMDs_len % i) + ".sh")
            retry = self.retry
            interval_time = self.interval_time
            split_env = self.split_env
            args = (
                L_CMD,
                lineNUM,
                folog_pre,
                retry,
                interval_time,
                split_env)
            with open(folog_pre, 'w') as fo:
                fo.write('\n'.join(L_CMD))
            L_p.append(p.apply_async(self.sh, args=args))
        stat_res = [x.get() for x in L_p]
        # from pprint import pprint
        # pprint(stat_res)
        stat_res_fail = []
        print("\033[1mJobs run stat:\033[0m")
        for chunks in stat_res:
            for chunk in chunks:
                if chunk[0] > 0:
                    stat_res_fail.append(chunk)
                    print(f"\033[31;5m {chunk[1]} Run Failed.\033[0m")
        print(f"\033[1m %.3f%% (%s/%s)\033[0m" % (
            len(stat_res_fail)/len(stat_res)*100,
            len(stat_res)-len(stat_res_fail),
            len(stat_res)
        ))
        if stat_res_fail:
            print("\033[1mSome jobs fail.\033[0m")
            out_fail_sh = os.path.basename(
                os.path.splitext(self.file_sh)[0])
            with open(out_fail_sh+".prorun-Failed-cmd.sh", "w") as fo1, \
                    open(out_fail_sh+".prorun-Failed.sh", "w") as fo2:
                for chunk in stat_res_fail:
                    # print(chunk)
                    print(chunk[3], file=fo1)
                    print("bash -evx", chunk[3], file=fo2)
        else:
            print("\033[1mAll job has Done.\033[0m")
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

    def sh(self, L_CMD, lineNUM, folog_pre, retry, interval_time=0, split_env=False):
        try:
            # print('hello')
            folog = folog_pre + '.stat.txt'
            num_len_line = len(str(len(L_CMD)))
            retry_raw = retry
            L_CMD = L_CMD if split_env else ['\n'.join(L_CMD)]
            stats = []
            for num_line, line in enumerate(L_CMD, start=1):
                stat = 1
                retry = retry_raw
                while stat and retry >= 0:
                    isretry = ('\nRetrying time(%d/%d)\n' % (
                        retry_raw - retry, retry_raw)
                        if retry < retry_raw else '')
                    retry -= 1
                    t1 = datetime.now()
                    run_number = "%s-%s" % (
                        lineNUM, ('%%0%dd' % num_len_line) % num_line)
                    fprint(folog, isretry + '>>>[CMD Start Run. %s  %s]   %s' %
                           (run_number,
                            t1.strftime('%Y-%m-%d_%H:%M:%S'), line))
                    with open(f"{folog_pre}.{run_number}.sh", "w") as fo:
                        print(line, file=fo)
                    stat = os.system(
                        f"bash -exv {folog_pre}.{run_number}.sh "
                        f">{folog_pre}.{run_number}.sh.log 2>&1")
                    t2 = datetime.now()
                    # print("self._shm:", self._shm)
                    if stat:
                        # self._shm[0] += 1
                        fprint(folog, '\n\033[1;5;37;41m[CMD Run Failed.   %s  %s (Time: %s)]  CMD: %s \033[0m\n' %
                               (run_number,
                                t2.strftime('%Y-%m-%d_%H:%M:%S'),
                                t2-t1, line))
                        time.sleep(interval_time)
                    else:
                        # self._shm[1] += 1
                        fprint(folog, '\033[1;37;42m[CMD Run Success.  %s  %s (Time: %s)]  CMD: %s \033[0m' %
                               (run_number,
                                t2.strftime('%Y-%m-%d_%H:%M:%S'),
                                t2-t1, line))
                else:
                    stats.append([stat, folog_pre, folog, line])
            return stats
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
    # sys.argv = ['', r'E:\我的云同步\ALL_CMD\mytools\tools_bed\run\run-workdir\allstep.sh',
    #             '--line', '1', '--thread', '8']
    run = RunSh()
    run.fmain()


if __name__ == '__main__':
    main()
