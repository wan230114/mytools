# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-08-24 05:15:45
# @Last Modified by:   11701
# @Last Modified time: 2019-08-24 15:25:31

import sys
import re
import argparse
from collections import OrderedDict


def fargv():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=('本程序用于处理sjm语法文件'
                     '版本简介：\n'
                     '    v1.0 初始版本'),
        epilog=('注意事项：\n'
                '    None'
                ))
    parser.add_argument('fipath', type=str,
                        help=('输入需要操作的sjm语法文件'))
    parser.add_argument('-k', '--keyword', type=str, default=False,
                        help=('输入想要提取的关键词，如：... '))
    parser.add_argument('-v', '--viewname', action='store_true',
                        default=False,
                        help='是否只打印jobname')
    args = parser.parse_args()
    # print(args)
    return args.__dict__


class InputError(Exception):
    pass


def clean(L_keyword, D_raw):
    D_new = OrderedDict()
    for x in L_keyword:
        D_new[x] = D_raw[x]
    return D_new


def fmain(fipath, keyword, viewname):

    D_names = OrderedDict()
    D_orders = OrderedDict()
    with open(fipath) as fi:
        s_all = fi.read()
        # print(s)
        L_jobs = re.compile(r'job_begin.*?job_end', re.DOTALL).findall(s_all)
        for i, x in enumerate(L_jobs):
            # print(x)
            name = re.findall(r'name(.*)', x)[0].strip()
            D_names[name] = x
        L_orders = re.findall(r'order\s+(.*?)\s+after\s+(.*?)\s', s_all)
        for x1, x2 in L_orders:
            # print(x1, x2)
            D_orders.setdefault(x2, {x1}).add(x1)
        Llogdir = re.findall(r'log_dir.*', s_all)
        if Llogdir:
            logdir = Llogdir[0]
        else:
            logdir = ''
    L_keyword = []
    if keyword:
        L_keyword = keyword.split(',')
        # print(L_keyword)
        # print(set(L_keyword) <= set(D_names))
        # sys.exit()
        if not set(L_keyword) <= set(D_names):
            raise InputError('sorry, your input “-k %s” not in file(%s)\'s names:%s' % (
                ','.join(list(set(L_keyword) - set(D_names))),
                fipath, ','.join(list(D_names))))

    iters = L_keyword if keyword else D_names
    for name in iters:
        if viewname:
            print(name)
        else:
            print(D_names[name])
    if not viewname:
        for x2 in set(D_orders) & set(iters):
            for x1 in D_orders[x2]:
                if x1 in iters:
                    print('order', x1, 'after', x2)
        print(logdir)


def main():
    # sys.argv = ['', '-h']    # print(fargv())
    # sys.argv = ['', './s2-2.job']
    # print(fargv())

    kwargs = fargv()
    # print(*list(kwargs.keys()),sep=", ")
    fmain(**kwargs)


if __name__ == '__main__':
    main()
