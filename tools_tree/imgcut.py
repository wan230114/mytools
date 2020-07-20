# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-31 01:04:34
# @Last Modified by:   JUN
# @Last Modified time: 2019-03-08 10:57:04


from PIL import Image
import os
import sys
import numpy
import re
import traceback
from multiprocessing import Pool
import argparse


def fargv():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''本程序用于图像白边裁剪
注意事项：
  对于裁剪的图像会直接覆盖原文件，请做好备份，若要保留原文件，请使用--bak选项
使用方法：
  python3 imgcut.py fipath [--filter FILTER] [--bak]''',
        epilog="""应用实例：
      # 实例1：裁剪文件test.png
      python3 imgcut.py test.png
      # 实例2：裁剪文件夹中testdir后缀名为.png的文件
      python3 imgcut.py testdir
      # 实例3：裁剪文件夹中testdir后缀名为.bmp的文件
      python3 imgcut.py testdir -f .bmp
      # 实例4：裁剪文件夹中testdir后缀名为.filter.jpg的文件，并保留原文件
      python3 imgcut.py testdir -f .filter.jpg --bak
      python3 imgcut.py testdir -f .filter.jpg -b
        """)
    parser.add_argument('fipath', type=str,
                        help='输入需要裁剪的文件路径或文件夹路径')
    parser.add_argument('--filter', '-f', type=str, default=None,
                        help='若输入文件(必选参数1)为文件夹路径，则此参数用于文件夹中过滤的后缀名, 可以为任意字符串如“resultbak.png”')
    parser.add_argument('--bak', '-b', action='store_true', default=False,
                        help='是否使用复制模式，保留原文件，默认为False')
    args = parser.parse_args()
    Targs = (args.fipath, args.filter, args.bak)
    print("\n--------------------------")
    print("输入参数是:\n1、输入路径: %s\n2、待过滤后缀名: %s\n3、是否保留原文件: %s" % Targs)
    print("--------------------------\n")
    return Targs


def isCrust(Lx):
    # return sum(pix) < 25
    # print(pix)
    Lall = []
    for Li in Lx:
        Lall.extend(Li)
    # print(len(Lx))
    return sum(Lall) < 765 * len(Lx) - 3


def filter(img):
    L = numpy.array(img)
    # print(len(L))
    # print(len(L[0]))
    a, b = img.size
    left, top, right, bottom = 0, 0, 0, 0
    for x in range(0, a, 1):
        Ly = [xx[x] for xx in L]
        if isCrust(Ly):
            left = x - 10
            break
    for x in range(a - 1, -1, -1):
        Ly = [xx[x] for xx in L]
        if isCrust(Ly):
            # print(Ly)
            right = x + 10
            break
    for y in range(0, b, 1):
        Lx = L[y]
        if isCrust(Lx):
            top = y - 10
            break
    for y in range(b - 1, -1, -1):
        Lx = L[y]
        if isCrust(Lx):
            bottom = y + 10
            break
    if bottom > b:
        bottom = b
    if right > a:
        right = a
    rect = (left, top, right, bottom)
    Lrect = []
    for x in rect:
        if x < 0:
            x = 0
        Lrect.append(x)
    rect = tuple(Lrect)
    return rect


def fmain(finame, foname, i, i_all):
    str_num = ('%%0%dd' % len(str(i_all))) % i + \
        ('-%s(%0.3f%%)' % (i_all, i/i_all*100))
    try:
        try:
            img = Image.open(finame)
        except OSError:
            print('WARNING: 输入文件', finame, '有误，已跳过裁剪')
            return
        if img.mode != "RGB":
            img = img.convert("RGB")
        print(str_num, '[裁剪开始: ', finame, "] 图片宽度和高度分别是{}".format(img.size))
        rect = filter(img)
        print(str_num, '[裁剪完毕: ', finame, '-->', foname, '] 裁剪坐标是：',
              (0, 0) + img.size, '-->', rect)
        region = img.crop(rect)
        region.save(foname)
    except Exception:
        traceback.print_exc()


def main():
    # sys.argv = ['', 'testdir']
    # sys.argv = ['', 'testdir', '-f', 'bmp']
    # sys.argv = ['', '--help']
    fipath, houzui, isbak = fargv()
    if not houzui:
        houzui = ""
    if os.path.isdir(fipath):
        # Lfiles = os.listdir(fipath)
        Lfiles = ['%s/%s' % (a, file)
                  for a, b, c in os.walk(fipath)
                  for file in c
                  if file.endswith('%s' % houzui)]
        # print(Lfiles)
        Lfiles = [x for x in Lfiles if x.endswith('%s' % houzui)]
        # print(Lfiles)
        p = Pool(20)
        for i, fi in enumerate(Lfiles, start=1):
            if isbak:
                fo = fi + '.cut' + re.findall('\.[A-Za-z]*?$', fi)[0]
            else:
                fo = fi
            p.apply_async(fmain, args=(fi, fo, i, len(Lfiles)))
            # fmain(fipath + os.sep + fi, fipath + os.sep + fo)
        p.close()
        p.join()
    else:
        if isbak:
            fopath = fipath + '.cut' + re.findall('\.[A-Za-z]*?$', fipath)[0]
        else:
            fopath = fipath
        fmain(fipath, fopath)


if __name__ == '__main__':
    main()
