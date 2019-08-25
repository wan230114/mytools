# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2018-12-27 13:50:49
# @Last Modified by:   JUN
# @Last Modified time: 2018-12-28 00:16:06

shelp = """md5 --help
用于获取当前文件夹下所有的md5值和大小信息，并输出到新文件

命令：
    python md5.py [x]
    选项:
    [x]  使用几个进程来运行，缺省默认2个进程

示例：
    python md5.py
    python md5.py 6
    python md5.py 8
"""
import os
import sys
import hashlib
import datetime
import time
from multiprocessing import Pool


def fmain(filepath):
    os.system('md5sum "%s" >>md5.txt' % filepath)


def main():
    t00 = time.time()
    if len(sys.argv) == 1:
        x = 2
    elif len(sys.argv) == 2:
        if sys.argv[1] == '--help':
            print(shelp)
            sys.exit()
        else:
            x = int(sys.argv[1])

    print('> 正在获取当前文件夹所有文件路径...')
    t0 = time.time()
    # s_files = os.popen("""find -L ./ -type f |cat|awk '!/.\/md5.txt/'|sort""").read()
    s_files = os.popen("""find -L ./ -type f|cat|awk '!/.\/md5.txt/'|awk '!/.\/checkSize.xls/'""").read()
    os.system('>md5.txt')
    Lfiles = s_files.strip().split('\n')
    print('获取结束，耗时%s秒' % (time.time() - t0))

    print('> 正在以 %s 进程 计算所有文件的md5值...' % x)
    t0 = time.time()
    p = Pool(x)
    for path in Lfiles:
        # fmain(path)
        p.apply_async(fmain, args=(path,))
    p.close()
    p.join()
    print('计算结束，耗时%s秒' % (time.time() - t0))

    print('> 正在获取文件夹大小...')
    t0 = time.time()
    with open('checkSize.xls', 'w') as fo:
        fo.write('\t'.join([str(os.path.getsize('./md5.txt')), './md5.txt']) + '\n')
        for path in Lfiles:
            fo.write('\t'.join([str(os.path.getsize(path)), path]) + '\n')
    print('获取结束，耗时%s秒' % (time.time() - t0))

    print('> 正在对md5.txt、checkSize.xls进行排序...')
    t0 = time.time()
    os.system('sort -k2 md5.txt -o md5.txt')
    os.system('sort -k2 checkSize.xls -o checkSize.xls')
    print('排序结束，耗时%s秒' % (time.time() - t0))

    print('\n运行结束，已于当前文件夹写入 md5.txt checkSize.xls ，耗时%s秒' % (time.time() - t00))


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
