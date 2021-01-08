# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  wan230114@qq.com
# @Date:   2018-11-02 12:58:15
# @Last Modified by:   JUN
# @Last Modified time: 2019-03-20 15:04:15

# 2018-11-07 14:48:51 本次修改内容为修复只能统计当前操作文件夹的BUG
# 2018-11-09 16:17:45 将查错功能单独列出来为一选项，加快程序运行速度
# 2018-11-10 01:05:39 全面修改升级架构，改用类实现
# 2018-11-21 16:52:18 修改错误碱基输出算法，优化整体统计速度
# （正在开发，统计每一条序列的gap数及含量，错误碱基及含量）
#
#

import os
import sys
import time
import numpy
from operator import itemgetter
from prettytable import PrettyTable
# python3开发，考虑兼容解决python2里面的编码问题
if sys.version[0] == '2':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')


def printM(file, *args, **kwargs):
    print(*args, **kwargs)
    print(*args, **kwargs, file=file)


class fas():
    '''--help：
    fas功能：
        1.统计每条序列长度及总长
        2.按序列大小或名称排序
        3.序列查错，统计序列中非ATCGN的碱基
        4.统计gap数，统计序列中N的起止位置
        5.统计平均长度和N50

    fas命令：
        python fas.py fastaname [argv]
        选项：
            fastaname  (必选)待统计的fasta文件
            [argv]:
            无       默认缺省参数，不排序打印序列总长和各条序列长度的统计结果
            -l / -n  (可选，二选一)按序列长度排序 / 按名称排序
            -r       (可选)逆序排序
            -y       (可选)打印所有的统计细节
            -o       (可选)将长度信息和gap统计信息写入原文件名加后缀名为.length和.gap的文件于当前操作文件夹
        查看帮助文档:
            python fas.py [--help]

    快捷设置:
        alias fas='python /.../mytools/fas.py'

    注意事项:
        1.-y详情模式统计较久，若基因组过大，请投递运行
        2.-l和-n模式只能二选一
        3.选项可以拆分书写，如fas mygene.fasta -y -lro，不能有选项之外的字母

    示例:
        # 统计序列数和碱基总数，打印每条序列长度
        fas mygene.fasta
        # 统计序列数和碱基总数，按长度逆序排序，打印每条序列长度
        fas mygene.fasta -lr
        # 统计序列数和碱基总数，按长度逆序排序，打印每条序列长度，同时将长度信息写入到新文件new.length
        fas mygene.fasta -lro new.length
        # 统计序列数和碱基总数，打印每条序列长度（并打印细节，包括gap含量和错误含量）
        fas mygene.fasta -y
        # 统计序列数和碱基总数，按长度逆序排序，打印每条序列长度（并打印细节，包括gap含量和错误含量）
        fas mygene.fasta -ylro
    (若您有好的建议或其他需求敬请联系: chenjun4663@novogene.com)'''

    def __init__(self, Lsysargv):
        self.fname = ''  # 输入的fasta名字
        # 定义变量
        # 存储详细统计数据，格式为[['ch1',11123,...],['ch2',12313,...],...]
        self.LCOUNT = []  # 存储统计数据，格式为[['ch1',11123],['ch2',12313],...]
        self.Ncount = 0
        self.Ncorrect = 0
        self.Ngap = 0
        self.Lgap = []  # 存储[[gene,start,end],[gene,start,end],...]
        self.Nerr = 0
        self.L_err = []
        # 初始化选项
        self.S_MOD = set()  # 存储选项
        self.argv(Lsysargv)

    def fmain(self):
        print('>>>统计中...')
        print('统计的文件是: %s' % self.fname)
        self.t0 = time.time()
        if not self.S_MOD:
            self.fcount()  # 统计主程序
        elif 'y' not in self.S_MOD:
            self.fcount()  # 统计数量的主程序
            self.sort()
        else:
            self.fcount2()  # 统计数量的主程序
            self.sort()
        # 根据需求是否输出文件
        if 'o' in self.S_MOD:
            with open(self.fname_length, "w") as fo:
                for Ldata in self.LCOUNT:
                    fo.write('%s\t%d\n' % (Ldata[0], Ldata[1]))
            print('已写入文件:  %s' % self.fname_length)
            if self.Lgap:
                with open(self.fname.split(os.sep)[-1] + '.gap', "w") as fo:
                    for Ldata in self.Lgap:
                        fo.write('%s\t%d\t%d\n' % (Ldata[0], Ldata[1], Ldata[2]))
                print('已写入文件:  %s' % self.fname_length)
        self.fasprint()
        return [x[:2] for x in self.LCOUNT]

    def argv(self, Lsysargv):
        '''用于输入格式标准化，如-y -l -r 会自动合并为-ylr'''
        try:
            self.fname = Lsysargv[1]
            if self.fname == '--help':
                print(self.__doc__)
                sys.exit()
            open(self.fname, 'rb')  # 文件不存在时处理异常IOError
            # 合并参数
            MOD = ''
            if len(Lsysargv) > 2:
                for x in Lsysargv[2:]:
                    if x[0] == '-':
                        self.S_MOD.update(set(x[1:]))
                if not bool(self.S_MOD) & ({'y', 'l', 'n', 'r', 'o', 'c'} >= self.S_MOD):
                    print('输入参数有误，只能输入规定内参数')
                    sys.exit()
                if {'l', 'n'} <= self.S_MOD:
                    print('输入参数有误，选项l和n排序只能二选一')
                    raise IndexError
                MOD = ''.join(self.S_MOD)
            Largv = ['', self.fname, MOD]  # 标准格式化
            # Largv += [x for x in Lsysargv[2:] if x[0] != '-']  # 统计和输出更多文件时可用
            # 定义新文件名
            if len(Largv) > 4:
                print('输入的新文件名有误\n\n%s' % self.__doc__)
            try:
                self.fname_length = Largv[3]
            except IndexError:
                self.fname_length = self.fname.split('/')[-1] + '.length'
        except IOError:
            print('文件[%s]未找到\n查看帮助: fas -h' % self.fname)
            sys.exit()
        except IndexError:
            print('您输入的参数为: ' + ' '.join(Lsysargv[1:]))
            print('您输入的参数为: ' + ' '.join(Lsysargv[1:]))
            print(self.__doc__)

    # 执行模式1，按行读取，好处是统计速度快，但不能统计gap数和查出错误的碱基
    def fcount(self):
        fi = open(self.fname, 'rb')
        while True:
            line = fi.readline()
            if not line:
                break
            # 【1】读取到基因行，进入
            if line.startswith(b'>'):
                geneName = line.decode().rstrip().split(' ', 1)[0].replace('>', '')
                Ncount = 0
                # 【2】读取每一行碱基计算
                while True:
                    line = fi.readline()
                    if not line:
                        break
                    if line.startswith(b'>'):
                        fi.seek(-len(line), 1)
                        break
                    Ncount += len(line.rstrip())
                # 【3】读取完碱基，统计
                self.Ncount += Ncount
                # 读取下一个序列前，计算总数并添加到结果
                self.LCOUNT.append([geneName, Ncount])
                Ncount = 0
    # 执行模式2，按单个字符读取，统计速度较慢，但能统计每条序列的gap数和错误碱基

    def fcount2(self):
        # 初始变量
        Ncount = 0
        perr = 0  # 指标，用于判断是否有非ATGCN的错误存在
        Nrow = 0  # 记录行数
        geneBase = {'A', 'G', 'T', 'C'}
        geneGap = "N"
        fi = open(self.fname, 'rb')
        while True:
            line = fi.readline()
            Nrow += 1
            if not line:  # 判断是否到文件末尾
                break
            if line.startswith(b'>'):
                geneName = line.decode().rstrip().split(' ', 1)[0].replace('>', '')
                Ncount = 0
                Ngap = 0
                Nerr = 0
                Pold = 1  # 当为正常ATGC时==1
                Pgap = 0
                while True:
                    line = fi.readline()
                    Nrow += 1
                    if not line:  # 考虑是否读取到最后一行
                        break
                    if line.startswith(b'>'):  # 是基因则进入下一次判断
                        fi.seek(-len(line), 1)
                        Nrow -= 1
                        break
                    # 【】逐个字符读取，文件查错，计算gap，
                    Lerr = []  # 记录行数Nrow,第几个碱基Ntemp，是什么字符i
                    perr = 0  # 是否有错
                    Ncount_tmp = 0  # 记录该行第几个碱基
                    NgapBEGIN = 0
                    NgapEND = 0
                    line_decode = line.rstrip().decode().upper()  # 统一转换大写，减少遍历时间
                    for i in line_decode:
                        Ncount_tmp += 1
                        if i not in geneBase:   # {'A', 'G', 'T', 'C'} #如此设计可以减少一个遍历N的计算量
                            if i == geneGap:
                                NgapTMP = 1
                                Ngap += 1
                                if Pold:  # 记住开始的地方
                                    NgapBEGIN = Ncount + Ncount_tmp
                                Pold = 0
                                Pgap = 1
                            else:
                                Nerr += 1
                                perr = 1
                                Lerr.append([str(Ncount + Ncount_tmp) + '|' + str(Ncount_tmp), i])
                            continue
                        if Pgap == 1:
                            NgapEND = Ncount + Ncount_tmp - 1
                            self.Lgap.append([geneName, NgapBEGIN, NgapEND])
                        Pold = 1
                        Pgap = 0
                    Ncount += len(line.rstrip())
                    if perr == 1:
                        perr = 0
                        serr = ''
                        for err in Lerr:
                            serr = serr + ':'.join(err) + '\n'
                        self.L_err.append([str(Nrow), serr])
                Ncorrect = Ncount - Ngap - Nerr
                self.Ncount += Ncount
                self.Ncorrect += Ncorrect
                self.Ngap += Ngap
                self.Nerr += Nerr
                # python2不够智能，需要100.0放在最前面转换浮点数才能计算，考虑与python3的兼容
                precenNcorrect = 100.0 * Ncorrect / Ncount
                precenNgap = 100.0 * Ngap / Ncount
                precenNerr = 100.0 * Nerr / Ncount
                self.LCOUNT.append([geneName, Ncount, Ncorrect, '%.2f%%' % precenNcorrect,
                                    Ngap, '%.2f%%' % precenNgap, Nerr, '%.2f%%' % precenNerr])
                Ncount = 0
            elif line.startswith(b'#'):  # 放到这里，是因为一般不会执行到，如果放到前面可能会多n次的运行判断
                print('WARNING : 跳过第 %d 行注释行统计' % Nrow)
                continue
            else:
                print('WARNING : 跳过第 %d 行，内容为: %s' % (Nrow, line.strip().decode()))
                continue
        fi.close()

    def sort(self):
        if 'l' in self.S_MOD:
            if 'r' in self.S_MOD:
                self.LCOUNT = sorted(
                    self.LCOUNT, key=itemgetter(1), reverse=True)  # 排序
            else:
                self.LCOUNT = sorted(self.LCOUNT, key=itemgetter(1))  # 排序
        elif 'n' in self.S_MOD:
            if 'r' in self.S_MOD:
                self.LCOUNT = sorted(
                    self.LCOUNT, key=itemgetter(0), reverse=True)  # 排序
            else:
                self.LCOUNT = sorted(self.LCOUNT, key=itemgetter(0))  # 排序

    def fasprint(self):
        print('统计完毕，耗时%f秒' % (time.time() - self.t0))
        print("-------------------------------------------------------------")
        print('总共序列数为:           ' + str(len(self.LCOUNT)))
        print('总共碱基数为:           {0: <10,}  '.format(self.Ncount))
        Lnums = [x[1] for x in self.LCOUNT]
        Lnums.sort(reverse=True)
        len50 = sum(Lnums) / 2.0
        numN50 = 0
        sumN50 = 0
        for i in Lnums:
            sumN50 += i
            if sumN50 > len50:
                numN50 = i
                break
        len90 = sum(Lnums) * 0.9
        numN90 = 0
        sumN90 = 0
        for i in Lnums:
            sumN90 += i
            if sumN90 > len90:
                numN90 = i
                break
        print('该文件序列的平均长度为：%.3f' % numpy.mean(Lnums))
        print('该文件序列的N50为:      %d' % numN50)
        print('该文件序列的N90为:      %d' % numN90)
        print("-------------------------------------------------------------")
        if 'y' in self.S_MOD:
            totol = self.Ncount + self.Ngap + self.Nerr
            print('其中正确碱基个数为:     {0: <10,}  '.format(self.Ncorrect) +
                  '%.4f%%' % (self.Ncount / float(totol) * 100))
            print('其中为N的碱基个数为:    {0: <10,}  '.format(self.Ngap) +
                  '%.4f%%' % (self.Ngap / float(totol) * 100))
            print('可能错误的碱基个数为:   {0: <10,}  '.format(self.Nerr) + '%.4f%%' %
                  (self.Nerr / float(totol) * 100))
        self.print_info()
        print('(本工具包目前功能涵盖统计每条序列，按长度或序列名排序，-y模式还增加碱基错误、gap统计功能，具体使用方法请查看详情：python fas.py --help)')

    def print_info(self):
        LCOUNT = self.LCOUNT
        print("\n\n每条序列长度信息如下：\n-------------------------------------------------------------")
        for Ldata in LCOUNT:
            Ldata = [str(x) for x in Ldata]
            print('%s' % '\t'.join(Ldata))
        print("-------------------------------------------------------------")
        if 'y' in self.S_MOD:
            print("\n\n每条序列长度信息如下：")
            print('gene       ——序列的名字')
            print('count      ——该条序列的长度')
            print('Ncorrect   ——该条序列中为ATGC的长度')
            print('Ngap       ——该条序列中gap的长度')
            print('Nerr       ——该条序列中非ATGCN的长度')
            allx = PrettyTable(['gene', 'count', 'Ncorrect', 'Ncorrect%',
                                'Ngap', 'Ngap%', 'Nerr', 'Nerr%'])
            allx.align["gene"] = "l"  # Left align city names
            for i in LCOUNT:
                allx.add_row(i)
            print(allx)
        if self.L_err:
            print("\n\n文件错误信息汇总：")
            print('Nrow       ——行数: 位于文件第几行')
            print('Erro info  ——错误信息，格式为: 该序列第几个碱基|该行第几个碱基:错误碱基')
            Column1 = 'Nrow'
            Column2 = 'Erro info'
            objErr = PrettyTable([Column1, Column2])
            objErr.align[Column1] = "l"
            objErr.align[Column2] = "l"
            # print(self.L_err)
            for i in self.L_err:
                objErr.add_row(i)
            print(objErr)

        if self.Lgap:
            print("\n\n文件gap信息汇总：")
            print('gene       ——gene的名字')
            print('start      ——gap的起始位置')
            print('end        ——gap的终止位置')
            print("-----------------------------")
            print('gene\tstart\tend')
            for Li in self.Lgap:
                print('\t'.join([str(x) for x in Li]))
            print("-----------------------------")


if __name__ == '__main__':
    if (len(sys.argv) == 1):
        # sys.argv = ['', 'fas.test.fa']
        sys.argv = ['', 'fas.test.fa', '-ylr']
        # sys.argv = ['', 'fas.test.fa', '-ylo']
        # sys.argv = ['', 'fas.test2.fa', 'yl']
    fas = fas(sys.argv)
    Llength = fas.fmain()
    # print(Llength)
