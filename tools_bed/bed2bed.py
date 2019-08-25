# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-08 15:12:26
# @Last Modified by:   JUN
# @Last Modified time: 2019-01-17 13:06:02

import os
import sys


class Pipe:
    """Pipe帮助:

    运行方法：
        python getPipe.py 01.softpath.txt 02.list.xls
    """

    def __init__(self, fi_list, fi_softpath):
        self.Llist = []
        self.Dpath = {}
        self.getinfo(fi_list, fi_softpath)

    def getinfo(self, fi_list, fi_softpath):
        with open(fi_list) as fi:
            for line in fi:
                Lline = line.split()
                self.Llist.append(Lline)
        with open(fi_softpath) as fi:
            for line in fi:
                Lline = line.strip().split('=')
                Lline = [x.strip() for x in Lline]
                self.Dpath[Lline[0]] = Lline[1]
        print(self.Llist)
        print(self.Dpath)

    def fmain(self):
        # 创建运行目录并切换至运行目录
        self.__mkdir__('run-workdir')
        os.chdir('run-workdir')

        open('allstep.sh', 'w+').close()
        f_runall = open('allstep.sh', 'a')
        with open('runAllstart.sh', 'w') as fo:
            fo.write('python3 %s/multiProgress.py allstep.sh --line 1 --thread 8 ' %
                     self.Dpath['path_mytools'])

        # with open('../../mod_run.sh') as fi:   # 测试专用
        with open('%s/mod_run.sh' % self.Dpath['path_bedtools']) as fi:
            data = fi.read()

        for Lline in self.Llist:
            self.Pipe(Lline, data, f_runall)

    def Pipe(self, Lline, data, f_runall):
        prjname, reffa, datapath = Lline
        pwd = os.getcwd()
        self.__mkdir__(prjname)
        os.chdir(prjname)

        do_step00 = 'run_start.00.do.sh'
        sh_step00 = 'run_start.01.sh'
        all_step00 = 'allstep.00.sh'

        # 01) 创建外部运行投递的程序
        line1 = 'cd %s/%s && sh %s &>%s.log\n' % (pwd, prjname, do_step00, do_step00)
        f_runall.write(line1)

        # 02) 创建内部投递程序
        s = "%s/perl %s/qsub-sge.pl --interval 30 --maxjob 1 --convert no --reqsub " % (
            self.Dpath['path_perl'], self.Dpath['path_qsub'])
        with open(do_step00, 'w') as fo:
            # snew = s + "--line 2 --resource vf=4G:p=18 "
            snew = s + "--line 2 --resource vf=1G:p=1 "
            fo.write("%s %s\n" % (snew, sh_step00))
        with open(sh_step00, 'w') as fo:
            fo.write("cd %s/%s \nsh %s\n" % (pwd, prjname, all_step00))

        # 03) 创建主运行脚本
        with open('%s' % all_step00, 'w') as fo:
            sh = data % (prjname, reffa, datapath, self.Dpath[
                         'path_bedtools'], self.Dpath['path_blast'])
            fo.write(sh)

        os.chdir('..')

    def __mkdir__(self, mkpath):
        isExists = os.path.exists(mkpath)
        if not isExists:
            os.makedirs(mkpath)
            print('创建文件夹%s成功' % mkpath)
        else:
            print('Error: 文件夹%s已存在, 未能成功创建' % mkpath)
            # sys.exit(0)


def main():
    # sys.argv = ['', '01.list.txt', '02.softpath.txt']
    fi_list, fi_softpath = sys.argv[1:3]
    p = Pipe(fi_list, fi_softpath)
    p.fmain()

if __name__ == '__main__':
    main()
