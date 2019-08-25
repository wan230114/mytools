# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2018-12-21 17:41:43
# @Last Modified by:   JUN
# @Last Modified time: 2019-05-06 23:59:22


import os
import sys


class Pipe:
    """Pipe帮助:

    运行方法：
        python getPipe.py list.txt
    """

    def __init__(self, fi_list, fi_softpath, genename):
        self.Llist = []
        self.Dpath = {}
        self.Dpath['genename'] = genename
        self.Dpath['runpwd'] = os.getcwd()
        self.getinfo(fi_list, fi_softpath)

    def getinfo(self, fi_list, fi_softpath):
        with open(fi_list) as fi:
            Llines = fi.read().strip().split('\n')
            Llines = [x.strip() for x in Llines]
            for i in range(0, len(Llines), 5):
                self.Llist.append(Llines[i: i + 5])

        with open(fi_softpath) as fi:
            for line in fi:
                Lline = line.strip().split('=')
                Lline = [x.strip() for x in Lline]
                self.Dpath[Lline[0]] = Lline[1]

    def fmain(self):
        # 创建运行目录并切换至运行目录
        self.__mkdir__('run-workdir')
        os.chdir('run-workdir')

        open('allstep.sh', 'w+').close()
        f_runall = open('allstep.sh', 'a')
        with open('runAllstart.sh', 'w') as fo:
            fo.write('python3 %(path_mytools)s/multiProgress.py allstep.sh --line 1 --thread 10 ' %
                     self.Dpath)
        # with open('../../mod_run.sh') as fi:   # 测试专用
        # with open('%s/mod_run.sh' % self.Dpath['path_bedtools']) as fi:
        #     data = fi.read()
        with open('wuzhong.list', 'w') as fo:
            fo.write('\n'.join(sorted([x[0] for x in self.Llist])))
        with open('%(path_tool)s/mod-run.sh' % self.Dpath, 'rb') as fi:
            data = fi.read().decode()

        for Lline in self.Llist:
            self.Pipe(Lline, data, f_runall)

    def Pipe(self, Lline, data, f_runall):
        prjname = Lline[0]

        self.__mkdir__(prjname)
        os.chdir(prjname)
        self.__mkdir__('input')

        pwd = os.getcwd()
        os.system('ln -s %s/gene' % self.Dpath['runpwd'])
        for i in Lline[1:]:
            os.system('ln -s %s input/' % i)

        fa, gff, cds,  pep = [pwd + '/input/' + x.split('/')[-1] for x in Lline[1:]]

        # 创建每个需要运行的脚本
        newdata = data % (pep, cds, fa, gff)
        with open('run.sh', 'w') as fo:
            fo.write(newdata)
        with open('runtree.sh', 'w') as fo:
            fo.write('python3 %(path_tool)s/01.pep_bak.py\n' % self.Dpath)
            fo.write('python3 %(path_tool)s/02.run-tree.py\n' % self.Dpath)

        all_step00 = 'run-allstart.sh'
        do_step00 = 'run_start.00.do.sh'
        sh_step00 = 'run_start.00.sh'
        do_step01 = 'run_start.01.do.sh'
        sh_step01 = 'run_start.01.sh'

        # 01) 创建外部运行投递的程序
        line1 = 'cd %s && sh %s &>%s.log\n' % (pwd, all_step00, all_step00)
        f_runall.write(line1)

        # 02) 创建主运行脚本
        with open(all_step00, 'w') as fo:
            fo.write('### 运行构树00\nsh run_start.00.do.sh\n\n')
            fo.write('### 运行构树01\nsh run_start.01.do.sh\n\n')

        # 03) 创建内部投递程序
        s = "%(path_perl)s/perl %(path_qsub)s/qsub-sge.pl --interval 30 --maxjob 1 --convert no --reqsub " % self.Dpath
        with open(do_step00, 'w') as fo:
            snew = s + "--line 1 --resource vf=2G:p=1 "
            fo.write("%s %s\n" % (snew, sh_step00))
        with open(sh_step00, 'w') as fo:
            fo.write("cd %s && sh run.sh\n" % pwd)

        with open(do_step01, 'w') as fo:
            snew = s + "--line 1 --resource vf=2G:p=10 "
            fo.write("%s %s\n" % (snew, sh_step01))
        with open(sh_step01, 'w') as fo:
            fo.write("cd %s && sh runtree.sh\n" % pwd)

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
    fi_list, genename = sys.argv[1:3]
    fi_softpath = "/ifs/TJPROJ3/Plant/chenjun/mytools/tools_tonglu/softpath.txt"
    p = Pipe(fi_list, fi_softpath, genename)
    p.fmain()


if __name__ == '__main__':
    main()
