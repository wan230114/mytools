# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-05-01 14:43:33
# @Last Modified by:   JUN
# @Last Modified time: 2019-05-11 09:36:21

import sys
import argparse


def fargv():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''本程序用于格式化输出分行文件文件
使用方法：
python3 itol.py [-c int,int,...]/[-f int,int,...] file ''',
        epilog="""
        # 实例：
        #   # 实例1：转换ceshi.tre为myname.svg输出至"out/"下
        #   python3 itol.py ceshi.tre out/myname
        #   # 实例2：转换ceshi.tre为myname.svg、myname.pdf和myname.png输出至"out/"下，设置参数：选择输出格式，使用圈形，显示支长
        #   python3 itol.py ceshi.tre out/myname --option "--format svg,pdf,png --display_mode 2 --branchlength_display 1"
        """)
    parser.add_argument('file', type=str,
                        help='输入需要处理的文件路径, 如/home/test/test.gff')
    parser.add_argument('--filter', '-f', type=str, default="",
                        help='可选参数，挑选的列，多个以逗号分隔')
    parser.add_argument('--clean', '-c', type=str, default="",
                        help='可选参数，去除的列，多个以逗号分隔')
    parser.add_argument('--sep', '-s', type=str, default="\t",
                        help='可选参数，分隔符，默认"\\t"')
    args = parser.parse_args()
    Targs = (args.file, args.filter, args.clean, args.sep)
    if args.filter and args.clean:
        print('error: -f(--filter) 与 -c(--clean) 不能并存')
        parser.parse_args(['', '--help'])
        sys.exit()
    else:
        for S in [args.filter, args.clean]:
            if len([x for x in S.split(',') if x.isdigit()]) != len([x for x in S.split(',') if x]):
                print([x for x in S.split(',') if x.isdigit()], S.split(','))
                print('error: 分隔符内容必须为数字')
                print('Args:', args)
                parser.parse_args(['', '--help'])
                sys.exit()
    # print("--------------------------")
    # print('Args:', args)
    # # print("输入参数是:\n1、输入路径: %s\n2、输出路径: %s.xxx\n3、可选参数: %s" % Targs)
    # print("--------------------------\n")
    return Targs[0],\
        [x for x in Targs[1].split(',') if x],\
        [x for x in Targs[2].split(',') if x],\
        Targs[3]


def fmain(finame, Lfilter=[], Lclean=[], sep='\t'):
    try:
        with open(finame) as fi:
            for n, line in enumerate(fi):
                line = line.rstrip()
                Lline = line.split(sep)
                try:
                    if Lclean:
                        for num in Lclean:
                            Lline.pop(int(num) - 1)
                        print(sep.join(Lline))
                    elif Lfilter:
                        newLline = []
                        for num in Lfilter:
                            newLline.append(Lline[int(num) - 1])
                        print(sep.join(newLline))
                    else:
                        print(line)
                except IndexError:
                    print(line)
                    # print('%s行num大于所在行列数%s, 已跳过' % (n, len(Lline)))
    except BrokenPipeError:
        pass
    except KeyboardInterrupt:
        pass


def main():
    finame, Lfilter, Lclean, sep = fargv()
    fmain(finame, Lfilter, Lclean, sep)


if __name__ == '__main__':
    main()
