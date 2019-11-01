# * @Author: ChenJun
# * @Date: 2019-11-01 12:13:51
# * @Last Modified by:   ChenJun
# * @Last Modified time: 2019-11-01 12:13:51

# import sys
import argparse
import re


def fargv():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=('本程序用于markdown文件的标题升级与降级'),
        epilog=('注意事项：\n'
                '    None\n'
                ))
    parser.add_argument('mod', type=str, choices=['u', 'up', 'd', 'down'],
                        help=('输入模式'))
    parser.add_argument('fipath', type=str,
                        help=('输入需要格式化的md文件'))
    parser.add_argument('-l', '--lineRows', type=int, default=1,
                        help=('输入起始行数，默认为1'))
    parser.add_argument('-c', '--coverage', action='store_true',
                        default=False,
                        help='是否使用覆盖模式')
    args = parser.parse_args()
    # print(args.__dict__)
    return args.__dict__


def fmain(mod, fipath, lineRows, coverage):
    Llines = []
    with open(fipath) as fi:
        row = 0
        p = 1
        for line in fi:
            row += 1
            if row >= lineRows:
                line_2 = re.sub('^  ? ?[#`]', '', line)
                if line_2.startswith('```'):
                    p *= -1
                if p > 0 and line_2.startswith('#'):
                    if mod in {'u', 'up'}:
                        if line_2.startswith('##'):
                            line_3 = re.sub('^ ? ? ?(#)', '', line)
                        else:
                            line_3 = line
                    elif mod in {'d', 'down'}:
                        line_3 = re.sub('^ ? ? ?(#)', '##', line)
                    Llines.append(line_3)
                else:
                    Llines.append(line)
    if coverage:
        with open(fipath, 'w') as fo:
            for line in Llines:
                fo.write(line)
    else:
        print(*Llines, sep='', end='')


def main():
    # sys.argv = ['', 'u', 'example.md']
    # sys.argv = ['', '-h']
    args = fargv()
    # print(*list(args.keys()), sep=", ")
    fmain(**args)


if __name__ == '__main__':
    main()
