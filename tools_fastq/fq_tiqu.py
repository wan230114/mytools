# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-09 12:03:10
# @Last Modified by:   JUN
# @Last Modified time: 2019-01-09 14:07:22

import os
import sys
import time
import random
import gzip
from multiprocessing import Pool


def mkdir(mkpath):
    isExists = os.path.exists(mkpath)
    if not isExists:
        os.makedirs(mkpath)


def write_print(fo, s):
    print(s)
    fo.write(s + '\n')
    fo.flush()


def fmain(finame, num):
    mkpath = "reslut_data_tiqu%s/" % num  # 输出文件夹
    mkdir(mkpath)
    fo_log = open('tiqu.log.%s.%s' % (time.strftime("%H-%M-%S", time.localtime()),
                                      str(random.randint(0, 10000))), 'w')
    stime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    write_print(fo_log, stime)
    write_print(fo_log, '正在进行去N操作 ' + finame)

    if finame.endswith('.gz'):
        fi = gzip.open(finame, 'rb')
        fo = gzip.open(mkpath + finame.split('/')[-1], 'wb')
    else:
        fi = open(finame, 'rb')
        fo = open(mkpath + finame.split('/')[-1], 'wb')
    nSeq = 0
    while True:
        if nSeq + 1 > num:
            break
        nSeq += 1
        Lline4 = []
        for i in range(4):
            line = fi.readline()
            if not line:
                if not Lline4:
                    write_print(fo_log, '正常完成')
                else:
                    write_print(fo_log, '请检查最后一条reads')
                break
            Lline4.append(line)
        fo.write(b''.join(Lline4))
        # if not nSeq % 2:
        if not nSeq % 100000:
            write_print(fo_log, '已提取{0:,}行'.format(nSeq))
    fi.close()
    fo.close()
    write_print(fo_log, '提取前%s条reads完毕，已写入 ' % nSeq + mkpath + finame)
    stime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    write_print(fo_log, stime)


def main():
    # sys.argv = ['', 'fq_tiqu.py.fq', '10']
    if len(sys.argv) == 1:
        print('python3 fq_tiqu.py sample.fq num')
        sys.exit()
    finame, num = sys.argv[1:3]
    fmain(finame, int(num))

    # Largv = []
    # with open(sys.argv[1]) as fi:
    #     Largv += fi.read().strip().split('\n')

    # # for finame in Largv:
    #     # fmain(finame)
    # pool = Pool(8)
    # pool.map(fmain, Largv)
    # pool.close()
    # pool.join()


if __name__ == '__main__':
    main()
