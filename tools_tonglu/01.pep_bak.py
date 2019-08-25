# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2018-12-21 17:41:43
# @Last Modified by:   JUN
# @Last Modified time: 2019-01-21 17:04:12


import os
import sys
import re
import shutil


def f():
    os.chdir('gene.result.xls/tree/pep')
    f_list = os.listdir('.')

    # 开始运行
    for f_sh in f_list:
        if os.path.splitext(f_sh)[1] == '.sh':
            # print(f)  # 获取到sh后缀的文件名
            fname = re.match('runtree(.*)\.tre.pep.sh', f_sh).group(1)
            # print(fname)  # 获取到中间的关键信息
            pep0 = fname + '.tre.pep'
            # print(pep0)  # 获取pep文件名字
            if pep0 + '.bak' not in f_list:
                shutil.copyfile(pep0, pep0 + '.bak')
            else:
                print(pep0 + '.bak 文件已存在，已跳过备份')
    # os.chdir('../../../../')


def main():
    f()

if __name__ == '__main__':
    main()
