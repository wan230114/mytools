# * @Author: ChenJun
# * @Date: 2019-11-01 12:13:51
# * @Last Modified by:   ChenJun
# * @Last Modified time: 2019-11-01 12:13:51

import sys
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
    def get_Llines():
        with open(fipath, 'rb') as fi:
            row = 0
            p = 1
            for line in fi:
                row += 1
                if row >= lineRows:
                    line_2 = re.sub(b'^  ? ?[#`]', b'', line)
                    if line_2.startswith(b'```'):
                        p *= -1
                        if line_2.strip().replace(b'```', b'', 1).endswith(b'```'):
                            p *= -1
                    if p > 0 and line_2.startswith(b'#'):
                        if mod in {'u', 'up'}:
                            if line_2.startswith(b'##'):
                                line_3 = re.sub(b'^ ? ? ?(#)', b'', line)
                            else:
                                line_3 = line
                        elif mod in {'d', 'down'}:
                            line_3 = re.sub(b'^ ? ? ?(#)', b'##', line)
                        yield line_3
                    else:
                        yield line
    if coverage:
        print(*[x.decode() for x in get_Llines()],
              sep='', end='', file=open(fipath, 'w'))
    else:
        print(*(x.decode() for x in get_Llines()), sep='', end='',)


def main():
    # sys.argv = ['', 'u', 'example.md']
    # sys.argv = ['', '-h']
    args = fargv()
    # print(*list(args.keys()), sep=", ")
    fmain(**args)


if __name__ == '__main__':
    main()
