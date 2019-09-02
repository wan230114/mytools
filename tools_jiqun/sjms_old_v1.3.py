# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-08-24 05:15:45
# @Last Modified by:   JUN
# @Last Modified time: 2019-08-26 10:42:32

import sys
import re
import copy
import argparse
from collections import OrderedDict


def fargv():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=('本程序用于格式化处理sjm语法文件，可提取指定job，还可按运行顺序对job排序\n'
                     '    当前版本：\n'
                     '      v1.3 修复-svk同时使用有时会丢失job的问题\n'
                     '    历史版本：\n'
                     '      v1.2 修复按流程运行顺序排序概率丢失job的问题\n'
                     '      v1.1 加入按流程运行顺序排序的功能\n'
                     '      v1.0 初始版本，实现提取功能\n'
                     ),
        epilog=('注意事项：\n'
                '    输入的sjm语法文件需为正确格式，即`sjm xxx.job`能正常运行的文件'
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
    s = {xx for x in d.values() for xx in x}
    # s = set()
    # for x in d.values():
    #     for xx in x:
    #         s.add(xx)
    for name in d.copy():
        if name not in s:
            d2[name] = {name: d.pop(name)}
    while d:
        for fz in d2:
            for x in d2[fz].copy():
                for xx in d2[fz][x]:
                    if xx in d:
                        d2[fz][xx] = d.pop(xx)

    # 第二步：对每一支内部进行排序
    for fz in d2:
        d = d2[fz]
        d_tmp = OrderedDict()
        while d:
            s = {xx for x in d.values() for xx in x}
            for name in d.copy():
                if name not in s:
                    d_tmp[name] = d.pop(name)
        d2[fz] = d_tmp

    # 第三步：合并分支(去掉，保留一下)
    # print(sorted([[x, list(d2[xx][x])] for xx in d2 for x in d2[xx]]))
    # sys.exit()
    return d2


def fmain(fipath, keyword, viewname, sortjob):
    '''主程序'''
    # 处理文件
    with open(fipath) as fi:
        D_names = OrderedDict()
        D_orders = OrderedDict()
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
    # 处理关键词及顺序
    L_keyword = []
    if keyword:
        L_keyword = keyword.split(',')
        L_tmp = []
        for x in L_keyword:
            if x not in L_tmp:
                L_tmp.append(x)
        L_keyword = L_tmp
        if not set(L_keyword) <= set(D_names):
            raise InputError('sorry, your input “-k %s” not in file(%s)\'s names:%s' % (
                ','.join(list(set(L_keyword) - set(D_names))),
                fipath, ','.join(list(D_names))))
    iters = L_keyword if keyword else list(D_names)
    # print(iters)
    # print(D_orders)
    # print(set(D_orders)|{xx for x in D_orders for xx in D_orders[x]})
    D_orders2 = {x: D_orders[x] for x in (set(D_orders) & set(iters))}
    D_orders3 = sort_iters(D_orders2) if sortjob else {'': D_orders2}
    # print(D_orders3)
    L_iterms = []
    if sortjob:
        for x in D_orders3:
            L_iterms.append(x)
            for xx in D_orders3[x]:
                if xx not in L_iterms:
                    L_iterms.append(xx)
                for xxx in D_orders3[x][xx]:
                    if xxx not in L_iterms:
                        L_iterms.append(xxx)
        iters2 = [x for x in L_iterms if x in iters]
        iters = [x for x in iters if x not in iters2] + iters2
    # 打印
    # print(iters)
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
                for x1 in D_orders3[fz][x2]:
                    if x1 in iters:
                        print('order', x1, 'after', x2)
                        p = 1
            if p:
                print()
            #         print('order', x1, 'after', x2)
            # print()
        print(logdir)


def main():
    # sys.argv = ['', './s2-2.job', '-k', 'pasa2,evm,training_snap,PASA4training,training_glimmHMM', '-s']
    # sys.argv = ['', './test/sjms/s2-2.job', '-k', 'pasa2,evm,training_snap,PASA4training,training_glimmHMM','-s']
    # sys.argv = ['', './test/sjms/s2-2.job', '-k', 'pasa2,evm,training_snap,PASA4training,training_glimmHMM']
    # sys.argv = ['', '-h']    # print(fargv())
    # print(fargv())

    kwargs = fargv()
    # print(*list(kwargs.keys()),sep=", ")
    fmain(**kwargs)


if __name__ == '__main__':
    main()
