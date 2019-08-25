# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-08-24 05:15:45
# @Last Modified by:   11701
# @Last Modified time: 2019-08-24 18:54:56

import sys
import re
import copy
import argparse
from collections import OrderedDict


def fargv():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=('本程序用于处理sjm语法文件'
                     '版本简介：\n'
                     '    v1.1 加入按流程运行顺序排序的功能'),
        epilog=('注意事项：\n'
                '    None'
                ))
    parser.add_argument('fipath', type=str,
                        help=('输入需要操作的sjm语法文件'))
    parser.add_argument('-k', '--keyword', type=str, default=False,
                        help=('输入想要提取的关键词，如：-k pasa2,evm,training_snap,PASA4training '))
    parser.add_argument('-s', '--sortjob', action='store_true',
                        default=False,
                        help='是否对job按流程运行顺序进行排序')
    parser.add_argument('-v', '--viewname', action='store_true',
                        default=False,
                        help='是否只打印jobname')
    args = parser.parse_args()
    # print(args)
    return args.__dict__


class InputError(Exception):
    pass


def sort_iters(d):
    d = copy.deepcopy(d)
    # 第一步：分支，每支单独的流程
    d2 = OrderedDict()
    s = set()
    for x in d.values():
        for xx in x:
            s.add(xx)
    for name in d.copy():
        if name not in s:
            d2[name] = {name: d.pop(name)}
    while d:
        for fz in d2:
            # print(x)
            for x in d2[fz].copy():
                # d2[x] = d.pop(x)
                # print(d2[fz][x])
                for xx in d2[fz][x]:
                    if xx in d:
                        d2[fz][xx] = d.pop(xx)
                # print(d2)
                # print(d)
    # sys.exit()

    # 第二步：对每一支内部进行排序
    for fz in d2:
        d = d2[fz]
        d_tmp = OrderedDict()
        while d:
            s = set()
            for x in d.values():
                for xx in x:
                    s.add(xx)
            for name in d.copy():
                if name not in s:
                    d_tmp[name] = d.pop(name)
        d2[fz] = d_tmp

    # 第三步：合并分支(去掉，保留一下)
    # print(d2)
    return d2


def clean(L_keyword, D_raw):
    D_new = OrderedDict()
    for x in L_keyword:
        D_new[x] = D_raw[x]
    return D_new


def fmain(fipath, keyword, viewname, sortjob):

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
    D_orders2 = {x: D_orders[x] for x in (set(D_orders) & set(iters))}
    D_orders3 = sort_iters(D_orders2) if sortjob else {'': D_orders2}
    iters = [xx for x in D_orders3 for xx in D_orders3[x]] if sortjob else iters
    for name in iters:
        if viewname:
            print(name)
        else:
            print(D_names[name])
    if not viewname:
        print()
        for fz in D_orders3:
            p = 0
            for x2 in D_orders3[fz]:
                for x1 in D_orders[x2]:
                    # print(x1, '--------->',iters)
                    if x1 in iters:
                        print('order', x1, 'after', x2)
                        p = 1
            if p:
                print()
        print(logdir)


def main():
    # sys.argv = ['', './s2-2.job', '-k', 'pasa2,evm,training_snap,PASA4training,training_glimmHMM', '-s']
    # sys.argv = ['', './s2-2.job', '-k', 'pasa2,evm,training_snap,PASA4training,training_glimmHMM']
    # sys.argv = ['', '-h']    # print(fargv())
    # print(fargv())

    kwargs = fargv()
    # print(*list(kwargs.keys()),sep=", ")
    fmain(**kwargs)


if __name__ == '__main__':
    main()
