# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-05-06 23:42:51
# @Last Modified by:   JUN
# @Last Modified time: 2019-05-08 10:08:37


import os
import sys
import re
import readline
workpath = '/ifs/TJPROJ3/Plant/chenjun/mytools'


def jg(info, y=0, n=0, inp=0):
    while True:
        s = input(info)
        if not s:
            continue
        if y == 1:
            if s == 'y':
                return
        if n == 1:
            if s == 'n':
                sys.exit(0)
        if inp == 1:
            return s
        if y and n:
            continue


def fmain():
    print('\n-----------------------------------------------------------------------')
    print('step01: 检查input.list')
    if not os.path.exists('./input.list'):
        path_list = os.path.join(workpath, 'tools_tonglu/Pipe-jianding/input.list')
        os.system('cp %s ./' % (path_list))
        print('已复制模板于当前文件夹，请参照 ./input.list 格式修改，注意顺序是prjname,fa,gff,cds,pep')
        sys.exit(0)
    else:
        L = [x.strip() for x in open('./input.list').readlines()]
        Lgroups = [L[n:n + 5] for n in range(0, len(L), 5)]
        print('请预览(以确认输入文件无误)：')
        for i_Lgroup, Lgroup in enumerate(Lgroups):
            i_Lgroup += 1
            print('*** prjname%2d: %s ***' % (i_Lgroup, Lgroup[0]))
            for i_x, x in enumerate(['fa ', 'gff', 'cds', 'pep']):
                i_x += 1
                print('%s: %s' % (x, Lgroup[i_x]))
        jg('[确认list文件无误？(输入"y"确认，输入"n"退出pipe程序)]:', y=1, n=1)

        print('\n-----------------------------------------------------------------------')
        print('step02: 检查需要鉴定的gene列表文件夹（一个文件对每个样品单独构一个树）')
        if os.path.isdir('gene'):
            Lfile = os.listdir('gene')
            if not Lfile:
                print('请检查gene文件夹是否有文件')
                sys.exit()
            print('请预览(输入的基因文件是):')
            for i_file, file in enumerate(Lfile):
                s_gene = os.popen(
                    "grep \\> gene/%s|head -5|sed 's#>##'|sed ':label;N;s/\\n/ /;b label'|sed -e 's/[[:space:]][[:space:]]*/  /g'" % file).read().strip()
                Lfile[i_file] += ':  %s  ...' % s_gene
            print('\n'.join(Lfile))
        else:
            os.system('mkdir gene 2>/dev/null')
            os.system('ln -s %s gene-ref' % (os.path.join(workpath, 'tools_tonglu/Pipe-jianding/test/gene')))
            print('运行需要准备需要鉴定的基因pep文件于gene文件夹内，请将待鉴定基因放入其中并以.fa为后缀名。已为您创建gene文件夹，并软链接gene-ref，可参照格式修改。')
            sys.exit()
        jg('[确认gene文件无误？(输入"y"确认，输入"n"退出pipe程序)]:', y=1, n=1)

        print('\n-----------------------------------------------------------------------')
        print('step03: 检查程序运行的项目名称，默认为test')
        if not os.path.exists('./all-run.sh'):
            path_all_run_sh = os.path.join(workpath, 'tools_tonglu/Pipe-jianding/all-run.sh')
            print(path_all_run_sh)
            os.system('cp %s ./' % (path_all_run_sh))
        print('请预览prjname：')
        stemp = os.popen('cat all-run.sh |grep prjname=').read()
        print(stemp)
        oldprjname = re.findall('prjname="(.*?)"', stemp)[0]
        newprjname = jg(
            '[是否使用该prjname？(输入y确认，输入"n"退出pipe程序，输入其他字母/数字以更新prjname)]:', y=1, n=1, inp=1)
        if newprjname:
            print('已更新prjname: %s --> %s' % (oldprjname, newprjname))
            os.system("""sed -i 's#%s#prjname="%s"#' all-run.sh""" % (stemp.strip(), newprjname))
            prjname = newprjname
        else:
            prjname = oldprjname

        os.system('mkdir list 2>/dev/null')
        print('\n./list/*列表生成中...')
        for Lgroup in Lgroups:
            os.system("python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_gff/getGeneID.py %s list/%s_list.txt %s" %
                      (Lgroup[2], Lgroup[0], prjname))

        print('\n-----------------------------------------------------------------------')
        print('step03: 投递任务')
        mail = jg('[是否需要运行完邮箱提醒？(输入邮箱，输入"n"跳过)]:', inp=1)
        while True:
            if mail == 'n':
                break
            if not re.findall('.*?@.*?\..*?', mail):
                mail = jg('[请输入正确的邮箱地址？(输入邮箱，输入"n"跳过)]:')
            else:
                break
        jg('[是否投递任务？(输入"y"确认，输入"n"退出pipe程序)]:', y=1, n=1)
        if mail != 'n':
            os.system('nohup sh all-run.sh &>all-run.sh.log && python /ifs/TJPROJ3/Plant/chenjun/mytools/sendmail.py %s -c "基因鉴定项目：%s跑完了" &' %
                      (mail, prjname))
        else:
            os.system('nohup sh all-run.sh &>all-run.sh.log &')


def main():
    try:
        fmain()
    except KeyboardInterrupt:
        print()

if __name__ == '__main__':
    main()
