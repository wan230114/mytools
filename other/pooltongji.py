# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-03-22 14:29:51
# @Last Modified by:   JUN
# @Last Modified time: 2019-03-22 17:14:38

import os
import sys
from multiprocessing import Pool
import traceback


def getnewname(Ldatas):
    L = []
    for i, Ldata in enumerate(Ldatas):
        foname = Ldatas[i][2]
        if foname not in L:
            L.append(foname)
        else:
            foname_new = foname
            ii = 0
            while True:
                if ii != 0:
                    foname_new = '%s.%s' % (foname, ii)
                if foname_new in L:
                    ii += 1
                else:
                    break
            Ldatas[i][2] = foname_new
            L.append(foname_new)


def fmain(outdir, prjname, path, foname):
    try:
        s = os.popen('du -s %s' % path).read()
        if not s:
            with open(outdir + os.sep + foname, 'w') as fo:
                fo.write('%s\t%s\t%s\t%s\n' % (prjname, '.', '.', path))
            raise IndexError('\nWARNING: ' + path + '无法统计')
        size = s.split()[0]
        if int(size) <= 1024**2:
            hsize = '%.3f' % (int(size) / 1024**1) + 'K'
        elif 1024**2 < int(size) <= 1024**3:
            hsize = '%.3f' % (int(size) / 1024**2) + 'M'
        elif 1024**3 < int(size) <= 1024**4:
            hsize = '%.3f' % (int(size) / 1024**3) + 'G'
        else:
            hsize = '%.3f' % (int(size) / 1024**4) + 'T'
        with open(outdir + os.sep + foname, 'w') as fo:
            fo.write('%s\t%s\t%s\t%s\n' % (prjname, size, hsize, path))
    except Exception:
        traceback.print_exc()


def main():
    flist, outdir = sys.argv[1:3]
    try:
        os.mkdir(outdir)
    except Exception:
        print(outdir, '文件夹已存在')
    with open(flist) as fi:
        Llines = [line.strip() for line in fi.readlines()]
        Ldatas = []
        for line in Llines:
            prjname, path = line.split(',')
            Ldatas.append([prjname, path, '%s--%s' % (prjname, path.split(os.sep)[-1])])
        getnewname(Ldatas)
        # [print(x) for x in Ldatas]

    p = Pool(80)
    for prjname, path, foname in Ldatas:
        p.apply_async(fmain, args=(outdir, prjname, path, foname))
    p.close()
    p.join()
    print('[ok] 统计完毕')


if __name__ == '__main__':
    main()
