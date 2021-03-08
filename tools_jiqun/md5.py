# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2018-12-27 13:50:49
# @Last Modified by:   JUN
# @Last Modified time: 2018-12-28 00:16:06

import os
import time
from multiprocessing import Pool
import argparse
# import sys
# import hashlib
# import datetime


def fargv():
    parser = argparse.ArgumentParser(
        description='用于获取当前文件夹下所有的md5值和大小信息，并输出到新文件')
    parser.add_argument('-x', type=int, default=1,
                        help='md5计算的进程数, 默认1')
    parser.add_argument('-c', '--checksize', action='store_true',
                        help='是否只开启 checksize 模式')
    args = parser.parse_args()
    return args.__dict__


def md5_do(filepath):
    os.system('md5sum "%s" >>md5.txt' % filepath)


def do(x, checksize=False):
    t00 = time.time()

    print('> \n正在获取当前文件夹所有文件路径...')
    t0 = time.time()
    # s_files = os.popen("""find -L ./ -type f |cat|awk '!/.\/md5.txt/'|sort""").read()
    s_files = os.popen(
        """find -L ./ -type f|cat|awk '!/.\/md5.txt/'|awk '!/.\/checkSize.xls/'""").read()
    Lfiles = s_files.strip().split('\n')
    print('获取结束，耗时%s秒' % (time.time() - t0))

    print('> \n正在获取文件夹大小...')
    t0 = time.time()
    with open('checkSize.xls', 'w') as fo:
        # fo.write(
        #     '\t'.join([str(os.path.getsize('./md5.txt')), './md5.txt']) + '\n')
        for path in Lfiles:
            fo.write('\t'.join([str(os.path.getsize(path)), path]) + '\n')
    print('获取结束，耗时%s秒' % (time.time() - t0))
    os.system('sort -k2 checkSize.xls -o checkSize.xls')
    print('排序结束，耗时%s秒' % (time.time() - t0))
    print('运行结束，已于当前文件夹写入 checkSize.xls ，耗时%s秒' % (time.time() - t00))

    if not checksize:
        print('> \n正在以 %s 进程 计算所有文件的md5值...' % x)
        os.system('>md5.txt')
        t0 = time.time()
        p = Pool(x)
        for path in Lfiles:
            # md5_do(path)
            p.apply_async(md5_do, args=(path,))
        p.close()
        p.join()
        print('计算结束，耗时%s秒' % (time.time() - t0))

        print('> \n正在对md5.txt、checkSize.xls进行排序...')
        t0 = time.time()
        os.system('sort -k2 md5.txt -o md5.txt')
        print('排序结束，耗时%s秒' % (time.time() - t0))
        print('运行结束，已于当前文件夹写入 md5.txt ，耗时%s秒' % (time.time() - t00))


def main():
    kwargs = fargv()
    # print(kwargs)
    # print(*list(kwargs.keys()),sep=", ")
    do(**kwargs)


if __name__ == '__main__':
    main()


# def GetFileMd5(filename):
#     pass
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
