# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-08-24 05:15:45
# @Last Modified by:   JUN
# @Last Modified time: 2019-09-24 15:35:21

import sys
import re
import copy
import argparse
from collections import OrderedDict


def fargv():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=('“sjms” ———— <sjm流程提取器>，用于sjm流程语法文件格式化，可提取指定的job，按流程运行顺序对job“排序”。'
                     ),
        epilog=('[附]：\n'
                '  输入的sjm语法文件需为正确格式，即`sjm xxx.job`能正常运行的文件\n'
                '当前版本：\n'
                '  v1.7 新增功能，可去除指定的节点，添加为-d参数\n'
                '历史版本：\n'
                '  v1.6 修复只使用-a参数会提取全部job的问题\n'
                '  v1.5 加入功能，能去除某一节点之后预执行的job，添加为-b参数\n'
                '  v1.4 加入功能，能提取某一节点之后预执行的所有job，添加为-a参数\n'
                '  v1.3 修复-svk同时使用有时会丢失job的问题\n'
                '  v1.2 修复按流程运行顺序排序概率丢失job的问题\n'
                '  v1.1 加入按流程运行顺序排序的功能，添加为-s参数\n'
                '  v1.0 初始版本，实现提取功能，添加为-k参数\n'
                ))
    parser.add_argument('fipath', type=str,
                        help=('输入需要操作的sjm语法文件'))
    parser.add_argument('-v', '--viewname', action='store_true',
                        default=False,
                        help='是否只打印jobname')
    parser.add_argument('-s', '--sortjob', action='store_true',
                        default=False,
                        help='是否对输出jobs按流程运行顺序进行排序')
    parser.add_argument('-a', '--afters', type=str, default=False,
                        help='输入jobnames(多个用英文逗号分隔)，提取输入的job节点之后预执行的所有job，包含jobnames在内')
    parser.add_argument('-b', '--breaking', type=str, default=False,
                        help='输入jobnames(多个用英文逗号分隔)，去除输入的job节点之后预执行的所有job，不包含jobnames在内')
    parser.add_argument('-k', '--keyword', type=str, default=False,
                        help='输入jobnames(多个用英文逗号分隔), 提取输入的job节点')
    parser.add_argument('-d', '--delword', type=str, default=False,
                        help='输入jobnames(多个用英文逗号分隔), 去除输入的job节点')
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

    return d2


def get_afters_job(iters, D_orders):
    '''处理节点之后分支的函数'''
    iters2 = []
    for x in iters:
        if x in D_orders:
            result = []
            tmp = {x}
            while tmp:
                for xx in tmp.copy():
                    if xx not in result:
                        result.append(xx)
                    tmp.remove(xx)
                    if xx in D_orders:
                        for x in D_orders[xx]:
                            tmp.add(x)
            iters2 += result
    return iters2


def fmain(fipath, keyword, viewname, sortjob, afters, breaking, delword):
    '''主程序'''

    # 1) 处理文件
    # 生成 D_names={name:"job_begin...job_end", name2:...}
    # 生成 D_orders={name:{name1, name2, ...}, name2:{xxx}, ...}
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

    # 2) 处理关键词等信息，生成预打印的iters
    L_keyword, Lcheck, L_delword = [], [], []
    if keyword:
        L_keyword = keyword.split(',')
        Lcheck.append(L_keyword)
    if delword:
        L_delword = delword.split(',')
        Lcheck.append(L_keyword)
    if afters:
        L_afters = afters.split(',')
        L_keyword += L_afters
        Lcheck.append(L_afters)
    if breaking:
        L_breaking = breaking.split(',')
        Lcheck.append(L_breaking)
    # 去重
    L_tmp = []
    for x in L_keyword:
        if x not in L_tmp:
            L_tmp.append(x)
    L_keyword = L_tmp
    # 检查是否是包含关系
    for checks in Lcheck:
        # print(checks)
        if not set(checks) <= set(D_names):
            raise InputError('sorry, your input “-k %s” not in file(%s)\'s job names:%s' % (
                ','.join(list(set(checks) - set(D_names))),
                fipath, ','.join(list(D_names))))
    iters = L_keyword if L_keyword else list(D_names)
    # print(set(D_orders)|{xx for x in D_orders for xx in D_orders[x]})

    # 3) job按执行顺序排序
    # 处理提取某一节点之后还需要执行的所有job
    if afters:
        iters += [x for x in get_afters_job(L_afters, D_orders) if x not in iters]
    if breaking:
        iters_tmp = get_afters_job(L_breaking, D_orders)
        iters_tmp = [x for x in iters_tmp if x not in L_breaking]  # 保留终止的节点
        iters = [x for x in iters if x not in iters_tmp]  # 去除后面的节点
    # 去除待删除的job
    iters = [x for x in iters if x not in L_delword]
    D_orders2 = {x: D_orders[x] for x in (set(D_orders) & set(iters))}  # 去除关键词之外的job
    D_orders3 = sort_iters(D_orders2) if sortjob else {'': D_orders2}  # 设计如此结构以便后期打印
    # 处理分支及排序，得到{'枝头':{'枝头之后的枝1':{name1,name2},name1:{name3}}, '枝头2':{...}}
    if sortjob:
        L_iterms = []
        for x in D_orders3:
            L_iterms.append(x)  # 添加枝头
            for xx in D_orders3[x]:
                if xx not in L_iterms:
                    L_iterms.append(xx)  # 添加内部枝头2
                for xxx in D_orders3[x][xx]:
                    if xxx not in L_iterms:
                        L_iterms.append(xxx)  # 添加每个枝头的结果
        # 过滤结果
        iters_sorted = [x for x in L_iterms if x in iters]
        # 加上一开始去除的枝头，因为D_order是没有把单个job放进去的
        iters = [x for x in iters if x not in iters_sorted] + iters_sorted

    # 4) 打印
    # 打印jobs
    for name in iters:
        if viewname:
            print(name)
        else:
            print(D_names[name])
    # 打印orders和logdir
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
    # sys.argv = ['', './test/sjms/test2.job', '-sv', '-k', 's2,s2.1',  '-a', 's2', '-b', 's4.1']
    # sys.argv = ['', './test/sjms/s2-2.job', '-k', 'pasa2,evm,training_snap,PASA4training,training_glimmHMM']
    # sys.argv = 'test.py ./test/sjms/test2.job -vs -a s2 -b s3,s4.1'.split()
    # sys.argv = 'test.py ./test2.job -s -a s2,p1,pp1 -b s4.1 -d s3'.split()
    # sys.argv = 'test.py ./test2.job -s -a s2,p1,pp1 -b s4.1'.split()
    # sys.argv = ['', '-h']    # print(fargv())
    # print(fargv())

    kwargs = fargv()
    # print(kwargs)
    # print(*list(kwargs.keys()),sep=", ")
    fmain(**kwargs)


if __name__ == '__main__':
    main()
