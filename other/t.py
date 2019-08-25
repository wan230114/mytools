# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-03-22 15:51:00
# @Last Modified by:   JUN
# @Last Modified time: 2019-03-22 16:01:59

import os
import subprocess

cmd = 'du -s ./out'
# s = os.popen(cmd).read()
# print('---')
# print(s.strip().split('\n')[-1])
# print('---')
# print(s)

# s = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
s = subprocess.Popen(cmd).read()
print(s)
print('---')
print(s)
