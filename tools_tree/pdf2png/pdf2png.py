#!/usr/bin/env python3

# ref: https://zhuanlan.zhihu.com/p/102742847
# pip install fitz
# pip install PyMuPDF

"""
# 将PDF转化为图片
pdfPath pdf文件的路径
imgPath 图像要保存的文件夹
zoom_x x方向的缩放系数
zoom_y y方向的缩放系数
rotation_angle 旋转角度
"""


import fitz
import sys
import os
# import argparse


# def args():
#     if len(sys.argv) == 1:
#         sys.argv = ["", "-h"]
#     parser = argparse.ArgumentParser(description=('TargetScan7.0注释（human）'))
#     group = parser.add_mutually_exclusive_group()
#     group.add_argument('-i', '--inputfile', type=str, default=None,
#                        help=('输入文件'))
#     group.add_argument('-ID', '--mirID', type=str, default=None,
#                        help=('输入文件'))
#     args = parser.parse_args()
#     return args


def pdf_image(pdfPath, imgPath, zoom_x, zoom_y, rotation_angle):
    # 打开PDF文件
    pdf = fitz.open(pdfPath)
    # 逐页读取PDF
    mod = "%%0%dd" % len(str(pdf.pageCount))
    for pg in range(0, pdf.pageCount):
        page = pdf[pg]
        # 设置缩放和旋转系数
        trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotation_angle)
        pm = page.getPixmap(matrix=trans, alpha=False)
        # 开始写图像
        pgnum = mod % pg if pdf.pageCount > 1 else ""
        pm.writePNG(imgPath+pgnum+".png")
    pdf.close()


def main(file):
    outpre = os.path.splitext(file)[0]
    print(f'in : {file}\nout: {outpre}*.png')
    pdf_image(file, outpre, 5, 5, 0)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        if os.path.isfile(path):
            main(os.path.abspath(path))
        elif os.path.isdir(path):
            for x in [os.path.join(root, file)
                      for root, dirs, files in os.walk(path)
                      for file in files if file.endswith("pdf")]:
                main(os.path.abspath(x))
