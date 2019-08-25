# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-07-05 11:35:15
# @Last Modified by:   JUN
# @Last Modified time: 2019-07-11 11:15:45

import sys
import argparse
import json


def fargv():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''本程序用于格式化输出分列文件文件
使用方法：
python3 xxx.py [-c int,int,...]/[-f int,int,...] file ''',
        epilog="""
        # 实例：
        #   # 实例1：
        #   python3
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
    return args

def filtL(L):
    for x in L:
        if 



def fmain(finame, Lfilter=[], Lclean=[], sep='\t'):
    try:
        Lfinal = []

        with open(finame) as fi:
            for n, line in enumerate(fi):
                line = line.rstrip()
                Lline = line.split(sep)
                try:
                    if Lclean:
                        for num in Lclean:
                            if int(num) > 0:
                                Lline.pop(int(num) - 1)
                            else:
                                Lline.pop(int(num))
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
    sys.argv = ['', '-f', '[(1,-4),-2]', '-c', '[-3]', 'list']
    print(sys.argv)
    args = fargv()
    print(args)
    fmain(args.file, json.loads(args.filter), json.loads(args.clean), args.sep)
    # a = '[%s]' % args.filter
    # print(a)
    # print(json.loads('[]'))
    # print(json.loads(a))


if __name__ == '__main__':
    main()
