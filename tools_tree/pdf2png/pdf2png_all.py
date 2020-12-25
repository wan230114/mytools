#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# @ Author: Chen Jun
# @ Author Email: 1170101471@qq.com
# @ Created Date: 2020-12-24, 15:10:57
# @ Modified By: Chen Jun
# @ Last Modified: 2020-12-24, 15:13:22
#############################################

from pdf2png import *

files = os.popen('find ./ -type f -name "*pdf"').read()
for file in files.strip().split("\n"):
    main(file)
