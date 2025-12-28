#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# @ Author: Chen Jun
# @ Author Email: 1170101471@qq.com
# @ Created Date: 2020-12-24, 15:10:57
# @ Modified By: Chen Jun
# @ Last Modified: 2021-12-23, 00:26:13
# @ Updated to be compatible with modern pdf2png.py
#############################################

import os
import sys
from multiprocessing import Pool
from pdf2png import process_file

def process_pdf_file(file_path):
    """处理单个PDF文件，适配pdf2png.py中的process_file函数"""
    process_file(file_path)

if __name__ == "__main__":
    L_res = []
    for p, ds, fs in os.walk("."):
        # print(p, ds, fs)
        for f in fs:
            if f.endswith(".pdf"):
                L_res.append(os.path.join(p, f))

    L_res.sort()
    print(f"找到 {len(L_res)} 个PDF文件")

    # 创建进程池处理所有PDF文件
    p = Pool(5)
    for i, file in enumerate(L_res, start=1):
        print(f"提交任务 {i}/{len(L_res)}: {file}")
        p.apply_async(process_pdf_file, args=(file,))
    p.close()
    p.join()
    print("所有PDF文件处理完成")
