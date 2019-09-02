# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-08-24 15:27:38
# @Last Modified by:   11701
# @Last Modified time: 2019-08-24 17:28:55

import sys
import copy
from pprint import pprint
from collections import OrderedDict


def get_Ele():
    '''

    '''
    d2 = {9: {9: {8, 7}}, 1:{1: {2}}}
    s = {4, 5, 6, 7, 8, 9}
    d = {4: {5}, 6: {5}, 7: {6, 4}, 8: {5}}
    while d:
        for fz in d2:
            # print(x)
            for x in d2[fz].copy():
                # d2[x] = d.pop(x)
                print(d2[fz][x])
                for xx in d2[fz][x]:
                    if xx in d:
                        d2[fz][xx] = d.pop(xx)
                print(d2)
                print(d)

def sort_iters(d):

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


def main():
    d = {4: {5}, 9: {8, 7}, 6: {5}, 7: {6, 4}, 8: {5},
         2: {1, 0}, 1: {0.01},
         'a': {'b', 'c'}, 'c': {'d'}}

    print(sort_iters(d))


if __name__ == '__main__':
    main()
    # get_Ele()
