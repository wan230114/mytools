# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2018-12-25 17:56:50
# @Last Modified by:   JUN
# @Last Modified time: 2019-01-21 17:00:32

import os
import re
from multiprocessing import Pool


def f():
    # print("已进入" + prjname + '/gene.result.xls/tree/pep')
    os.chdir('gene.result.xls/tree/pep')
    f_list = os.listdir('.')

    # 用来输出日志准备
    pstat = 0
    pstat_max = 0
    os.system('rm *.log *.new *.tre *.muscle')

    # 开始运行
    p = Pool(2)
    for f_sh in f_list:
        if os.path.splitext(f_sh)[1] == '.sh':
            pstat_max += 1
            # print(f)  # 获取到sh后缀的文件名
            fname = re.match('runtree(.*)\.tre.pep.sh', f_sh).group(1)
            # print(fname)  # 获取到中间的关键信息
            pep0 = fname + '.tre.pep'
            # print(pep0)  # 获取pep文件名字

            # 重新写入新的sh文件
            with open(f_sh, 'rb') as fi:
                data = fi.read()
            with open(f_sh + '.new', 'wb') as fo:
                s = ("muscle -in  %s" % pep0).encode()
                s = data
                # s = data.replace(s, s + b'.new')
                s = b'export PATH=/PUBLIC/software/DENOVO/bio/software/muscle3.8.31/:$PATH\n' + s
                fo.write(s)

            # 构建pep文件列表准备写入pep
            with open('../../%s.fa.result_aa.fasta' % fname) as fi2:
                Ldata = fi2.read().split()
                # print(Ldata)
                # print(Ldata)
                Lnewdata = []
                i = 0
                i_max = len(Ldata) - 1
                linetmp = ''
                Lnewdata.append(Ldata[i])
                while True:
                    i += 1
                    if i > i_max:
                        break
                    if Ldata[i].startswith('>'):
                        linetmp = linetmp[:-1]
                        Lnewdata.append(linetmp)
                        Lnewdata.append(Ldata[i])
                        linetmp = ''
                    else:
                        linetmp += Ldata[i]
                linetmp = linetmp[:-1]
                Lnewdata.append(linetmp)
                len_Lnewdata = len([x for x in Lnewdata if x.startswith('>')])

            # 读取前面的行准备重新写入pep文件
            with open(pep0 + '.bak') as fi:
                Ldatas = fi.read().split()
                # print(Ldatas)
                Ldata = []
                i = -1
                while True:
                    i += 1
                    try:
                        if Ldatas[i + 1].startswith('>'):
                            break
                        else:
                            Ldata.append(Ldatas[i])
                            Ldata.append(Ldatas[i + 1])
                            i += 1
                    except IndexError:
                        break
                len_Ldata = len([x for x in Ldata if x.startswith('>')])
                # print(len_Ldata)
                Ldata = [x.replace(':', '_') for x in Ldata]
                Ldata = [x.replace('|', '_') for x in Ldata]
                Ldata = [x.replace('*', '') for x in Ldata]
            # print(Ldata + Lnewdata)
            with open(pep0, 'w') as fo:
                fo.write('\n'.join(Ldata + Lnewdata))
            p.apply_async(run, args=(f_sh, fname, len_Ldata, len_Lnewdata))
    p.close()
    p.join()
    os.chdir('../../../')


def run(*s):
    f_sh, fname, len_Ldata, len_Lnewdata = s
    try:
        stat = os.system('sh %s.new &>%s.new.log' % (f_sh, f_sh))
        if not stat:
            os.system('echo "%s |  正常完成  | %s | %s | %s">>run.log' %
                      (fname, len_Ldata, len_Lnewdata, len_Ldata + len_Lnewdata))
        else:
            os.system('echo "%s | 未正常完成 | %s | %s | %s">>run.log' %
                      (fname, len_Ldata, len_Lnewdata, len_Ldata + len_Lnewdata))
    except Exception as ex:
        msg = "Error :%s" % ex
        print(msg)


def main():
    # L = []
    # with open('list.txt') as fi:
    #     Llines = fi.readlines()
    #     Llines = [x.strip() for x in Llines]
    #     for i in range(0, len(Llines), 5):
    #         prjname = Llines[i]
    #         L.append(prjname)
    # L = ["Pcui", "Pdan", "Pdul", "Phai", "Phei", "Pkue", "Pnan", "Ptia", "Pzao"]
    f()

if __name__ == '__main__':
    main()
