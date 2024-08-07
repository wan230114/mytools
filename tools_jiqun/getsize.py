#!/usr/bin/env python3
import sys
import argparse


def fargv():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='本程序用于格式化存储单位某一行的大小文件',
        epilog=('注意事项：\n'
                '    无'))
    parser.add_argument('-i', '--inputpath', type=str, default=False,
                        help=('输入需要统计的扫盘结果文件或文件夹，不给文件时将默认从管道读取。 其中包含的文件，'
                              '每一行四列，如：“lixiangkong <\\t> 22617126 <\\t> /TJNAS01/PAG/Plant/Data_20170920/170508_ST-E00126_0410_BHKVCJALXX/GBS00714/GBS00714_L3_1.adapter.list.gz <\\t> 2017-09-21”'))
    parser.add_argument('-n', '--num', type=int, default=1,
                        help='输入想统计的第几列')
    parser.add_argument('-s', '--sep', type=str, default='',
                        help='输入列之间的分隔符，默认为一切空字符，与awk默认类似')
    parser.add_argument('--rep', action='store_true',
                        default=False,
                        help='是否使用替换模式？对指定列不在后面一列增加一列，而直接替换当前列')
    args = parser.parse_args()
    # print(args.__dict__)
    return args.__dict__


def getsize(size):
    D = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    try:
        for x in D:
            if int(size) < 1024**(x + 1):
                hsize = str('%.3f' % (int(size) / 1024**x)) + D[x]
                return hsize
    except ValueError:
        # print(size, 'have eero')
        return size


def do(line, num, rep, sep):
    try:
        line = line.decode('utf8')
    except UnicodeDecodeError:
        line = line.decode('gbk')
    sep = sep if sep else None
    Lline = line.strip().split(sep)
    if rep:
        Lline[num] = getsize(Lline[num])
    else:
        Lline.insert(num + 1, getsize(Lline[num]))
    # print(Lline)
    print('\t'.join(Lline))


def fmain(inputpath, num, rep, sep):
    num = int(num) - 1
    if not inputpath:
        while True:
            line = sys.stdin.buffer.readline()
            if not line:
                break
            do(line, num, rep, sep)
    else:
        with open(inputpath, 'rb') as fi:
            for line in fi:
                if not line.strip():
                    continue
                do(line, num, rep, sep)


def main():
    # sys.argv = ['', '-h']
    # sys.argv = ['', 'deal-result-saopan/result/TJNAS_Plant_10M', '2', '--rep']
    # sys.argv = ['', 'deal-result-saopan/result/TJNAS_Plant_10M', '2']
    # sys.argv = ['', '-i', 'deal-result-saopan/result/TJNAS_Plant_10M', '-n', '2', '--rep']
    args = fargv()
    # print(*list(args.keys()), sep=", ")
    fmain(**args)


if __name__ == '__main__':
    main()
