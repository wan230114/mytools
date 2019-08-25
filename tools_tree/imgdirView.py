# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-22 16:32:01
# @Last Modified by:   JUN
# @Last Modified time: 2019-05-16 01:13:17

import os
import sys
import argparse


def fargv():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''  本程序用于生成html可视化文件夹中的png、pdf、svg文件
    使用方法：
      python3 imgdirView.py fidir houzui
    快捷设置:
      alias view='python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tree/imgdirView.py'
    ''')
    parser.add_argument('fidir', type=str,
                        help='输入需要可视化的文件夹名，当前文件夹')
    parser.add_argument('houzui', type=str,
                        help='输入后缀名，末尾只能以png,pdf,svg结束，可以包含多个字符如 tre.png , option.tre.pdf , ')
    parser.add_argument('-v', '--reverse', type=str, default=[], nargs='*',
                        help='排除不想要的文件名，可依次增加多个条件，类似于grep -v用法')
    args = parser.parse_args()
    if args.houzui[-3:] not in ["png", "pdf", "svg"]:
        print('请检查输入文件后缀名')
        parser.parse_args(['', '--help'])
        sys.exit()
    Targs = (args.fidir, args.houzui, ', '.join(args.reverse))
    print("--------------------------")
    print("输入参数是:\n1、输入文件夹: %s\n2、过滤文件后缀名: %s\n3、排除的文件名：%s" % Targs)
    print("--------------------------\n")
    return Targs[0], Targs[1], args.reverse


def fmain(fidirraw, houzui, reverse=[]):
    softpath = os.path.split(os.path.realpath(__file__))[0]
    if not os.path.isdir(fidirraw):
        print('%s 文件夹不存在' % fidirraw)
        sys.exit()
    fidir = fidirraw.rstrip(os.sep).split(os.sep)[-1]
    # L = os.listdir(fidir)
    L = []
    for p, d, f in os.walk(fidir):
        for ff in f:
            L.append(os.path.join('.', p, ff))
    if reverse:
        L = [x for x in L if x.endswith(houzui)]
        S = set()
        for x in L:
            if x.endswith(houzui):
                p = 0
                for xx in reverse:
                    # print(xx not in x, xx, x)
                    if xx in x:
                        p = 1
                        break
                if p == 0:
                    S.add(x)
        L = sorted(S)
    else:
        L = sorted([x for x in L if x.endswith(houzui)])
    [print(x) for x in L]
    print('过滤到%s个文件' % len(L))
    Dfile = {'pdf': 'mod-pdf.html',
             'png': 'mod-png.html',
             'svg': 'mod-svg.html',
             }
    foname = '%s-%s.html' % (fidir, houzui)
    with open(foname, 'w') as fo:
        with open(os.path.join(softpath, 'mod', Dfile[houzui.split('.')[-1]])) as fi:
            s = fi.read()
        fo.write(s % (str(L).strip('[]')))
    print('\nSuccess. write to: ' + foname)
    # else:
    #     fo.write('<html>\n\t<body>\n')
    #     fo.write('\t\t<br><table border="5">\n')
    #     for file in L:
    #         if file.endswith('png'):
    #             lineview = '<img src="%s" /></p>' % file
    #         if file.endswith('svg'):
    #             lineview = '<object data="%s" type="image/svg+xml"></object>' % file
    #         fo.write('\t\t\t<tr>\n')
    #         fo.write('\t\t\t\t<td valign="top">\n\t\t\t\t\t<p>%s</p>\n' % file)
    #         fo.write('\t\t\t\t\t%s\n\t\t\t\t</td>\n' % lineview)
    #         fo.write('\t\t\t</tr>\n')
    #     fo.write('\t\t</table>\n')
    #     fo.write('</body>\n</html>\n')
    sinput = ''.join(['\n请选择压缩模式\n'
                      '--> 将文件夹保持文件相对位置，压缩并下载至本地查看\n',
                      '    模式1：只压缩需要查看文件：\n',
                      '        zip %s.zip $FilterFiles* ...\n' % fidir,
                      '    模式2：压缩整个文件夹：\n',
                      '        find -L %s -type f -name "*"|xargs zip %s.zip %s\n' % (
                          fidir, fidir, foname),
                      '    模式3：压缩整个文件夹(不含软链接)：\n',
                      '        find %s -type f -name "*"|xargs zip %s.zip %s\n' % (
                          fidir, fidir, foname),
                      '    模式其他：预自定义操作，请按Enter或输入其他任意字符退出\n\n请输入数字进行模式选择(1/2/3): '])
    try:
        mond = input(sinput).strip()
    except Exception:
        mond = ''
    if mond == "1":
        os.system('zip %s.zip %s %s' % (fidir, foname, ' '.join(L)))
    if mond == "2":
        os.system('find -L %s -type f -name "*"|xargs zip %s.zip %s' %
                  (fidir, foname, foname))
    if mond == "3":
        os.system('find %s -type f -name "*"|xargs zip %s.zip %s' %
                  (fidir, foname, foname))
    print('\n请下载文件于本地查看: %s.zip' % fidir)
    print('\nThank you for using imgdirView.py.')


def main():
    # sys.argv = ['', '1', 'pdf']
    # fidir, houzui = sys.argv[1:3]
    fidir, houzui, reverse = fargv()
    fmain(fidir, houzui, reverse)


if __name__ == '__main__':
    main()
