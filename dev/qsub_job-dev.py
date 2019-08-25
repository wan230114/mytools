# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com 
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-16 10:13:14
# @Last Modified by:   JUN
# @Last Modified time: 2019-01-16 10:13:36

def qsub(fname_sh):
    '''输入脚本名称，投递任务，返回job编号'''
    s = os.popen('qsub -cwd -l vf=0.3g,p=1 ' + fname_sh).read()  # Your job 5468502 ("run1.sh") has been submitted
    return s.split()[2]


def jiankong(L):
    '''传入job号列表，返回运行完的job号'''
    pass