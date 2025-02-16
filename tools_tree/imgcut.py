#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-31 01:04:34
# @Last Modified by:   JUN
# @Last Modified time: 2021-03-09 00:12:04


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
    parser.add_argument('fipath', type=str, nargs="+",
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


def isCrust(L_tmp, Len):
    """计算L_tmp中的值是否存在不为白色

    Args:
        L_tmp (np.array): [[x,y,z],[x,y,z],...]

    Returns:
        bool: True/False, 有杂色返回TRUE，都为白色时，返回FALSE
    """
    # return sum(pix) < 25
    # print(pix)
    # Lall = []
    # for Li in L_tmp:
    #     Lall.extend(Li)
    # print(len(L_tmp))
    return L_tmp.sum() < (765 * Len - 3)


def filter(img):
    L = numpy.array(img)
    w, h = img.size
    left, top, right, bottom = 0, 0, 0, 0
    if not isCrust(L, L.size/3):
        return None
    else:
        step = 3
        kepp_black = 10
        for x in range(0, w, step):
            Ly = L[:, x, :]
            if isCrust(Ly, Ly.size/3):
                left = x - kepp_black
                break
        for x in range(w - 1, -1, -step):
            Ly = L[:, x, :]
            if isCrust(Ly, Ly.size/3):
                right = x + kepp_black
                break
        for y in range(0, h, step):
            Lx = L[y]
            if isCrust(Lx, Lx.size/3):
                top = y - kepp_black
                break
        for y in range(h - 1, -1, -step):
            Lx = L[y]
            if isCrust(Lx, Lx.size/3):
                bottom = y + kepp_black
                break
        if bottom > h:
            bottom = h
        if right > w:
            right = w
    rect = (left, top, right, bottom)
    Lrect = []
    for x in rect:
        if x < 0:
            x = 0
        Lrect.append(x)
    rect = tuple(Lrect)
    return rect


def fmain(finame, foname, i=1, i_all=1):
    str_num = ('%%0%dd' % len(str(i_all))) % i + \
        ('-%s' % (i_all))
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
        if rect:
            region = img.crop(rect)
            info = ''
            try:
                region.save(foname)
            except SystemError:
                info = '\n   Warning: 图片全白'
        else:
            info = '\n   Warning: 图片全白'
        print(str_num, '[裁剪完毕: ', finame, '-->', foname, ']',
              '\n   裁剪坐标是：', (0, 0) + img.size, '-->', rect,
              info)
    except Exception:
        traceback.print_exc()


def main():
    # sys.argv = ['', 'testdir']
    # sys.argv = ['', 'testdir', '-f', 'bmp']
    # sys.argv = ['', '--help']
    fipaths, houzui, isbak = fargv()
    if not houzui:
        houzui = ""
    for fipath in fipaths:
        if os.path.isdir(fipath):
            # Lfiles = os.listdir(fipath)
            Lfiles = ['%s/%s' % (a, file)
                    for a, b, c in os.walk(fipath)
                    for file in c
                    if file.endswith('%s' % houzui)]
            # print(Lfiles)
            Lfiles = [x for x in Lfiles if x.endswith('%s' % houzui)]
            # print(Lfiles)
            p = Pool(5)
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
                a, b = os.path.splitext(fipath)
                fopath = a + '.cut' + b
            else:
                fopath = fipath
            fmain(fipath, fopath)


if __name__ == '__main__':
    main()
    # fmain("baidu.png", "baidu.cut.png")
