# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-05-10 14:42:18
# @Last Modified by:   JUN
# @Last Modified time: 2019-07-18 10:37:24


from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import sys


def fgetsort(D):
    def getsort(x):
        return D[x.values[0]]
    return getsort
    # print(x, type(x))
    # a = x
    # print(a, type(a))
    # print(x.values[0])
    # print(type(x.values[0]))
    # sys.exit()
getsort = fgetsort({'a2': 1, 'a3': 2, 'a1': 3})


# def lianjie(D)


data = {"name": ['google', 'baidu', 'yahoo'],
        "marks": [100, 200, 300],
        "price": [1, 2, 3]}
data = [
    ['a1', 'b1', 'c1', 100],
    ['a1', 'b1', 'c1', 100],
    ['a1', 'b2', 'c1', 200],

    ['a2', 'bbbbbbbbbbbbbbbbb1', 'c0', 100],
    ['a2', 'bbbbbbbbbbbbbbbbb1', 'c1', 100],
    ['a2', 'bbbbbbbbbbbbbbbbb1', 'c1', 300],
    ['a2', 'bbbbbbbbbbbbbbbbb1', 'c1', 200],
]
df = DataFrame(data, columns=['a', 'b', 'c',  'num'])
# print(df)
# mapping = {'a': 'path', 'b': 'path', 'c': 'path'}
# print(df.groupby(mapping, axis=1))
# gp_tongji = df.groupby(['a', 'b', 'c']).agg({'a': [getsort], 'num': [len, np.sum]})
# gp_tongji = df.groupby(['a', 'b', 'c'], squeeze=True).agg({'a': [getsort], 'num': [len, np.sum]})
gp_tongji = df.groupby(['a', 'b', 'c'], observed=True).agg({'a': [getsort], 'num': [len, np.sum]})
# gp_tongji = df.groupby(['a', 'b', 'c']).agg({'num': [len, np.sum], 'a': [getsort]})
# gp_tongji = df.groupby(['a', 'b', 'c'])['num', 'a'].agg({'num': [len, np.sum], 'a': [getsort]})
# {'num': len, 'num': np.sum, 'a': getsort})

print(gp_tongji.to_dict())
# print(gp_tongji.__dict__)
print(gp_tongji.to_string())
# print(DataFrame(dict(list(gp_tongji[('a','getsort')]))).to_string())
sys.exit()

# print(gp_tongji.sort_values([('a', 'getsort'),'b','c'], ascending=True))
# print(gp_tongji.sort_values([('a', 'fgetsort(D)'), 'b', 'c', ('num', 'sum')], ascending=False))
print(gp_tongji.sort_values([('a', 'getsort'), 'b', 'c', ('num', 'sum')], ascending=False))
# print(gp_tongji.sort_values(['a', 'b', 'c',('num', 'sum')], ascending=False))


xiangmu = 'b1'
df_tiqu = df[df['b'] == xiangmu]  # 提取某行并求和
print(df_tiqu)

print('\n###项目:', xiangmu)
gp_tongji = df_tiqu.groupby(['a']).agg({'num': [len, np.sum]})
print(gp_tongji.to_dict())
print('文件所属人详情:', gp_tongji.to_dict()[('num', 'sum')])

print('\n###项目', xiangmu, '合计:', df_tiqu['num'].sum())
gp_tongji = df_tiqu.groupby(['a'])['num'].agg([len, np.sum])
print(gp_tongji.to_dict())
print('文件所属人详情:', gp_tongji.to_dict()[('sum')])
# print(type(gp_tongji))
# print(gp_tongji.__dict__)

# print(gp_tongji.to_records())
# print(gp_tongji.iloc[:, 0])  # 等价于data.iloc[:, 0]
# print(gp_tongji.loc[:, 'a'])  # 等价于data.iloc[:, 0]

# print('\n项目信息:', set(df_tiqu.to_dict()['a'].values()))
print('\n项目信息:', ','.join(sorted(set(df_tiqu.to_dict()['a'].values()))))

# gp = df.groupby(['a', 'b'])
# print(gp.sum())


print(df.drop_duplicates('b', keep='first', inplace=False))
print('\n------------------')
print(pd.concat([df, df], ignore_index=True).drop_duplicates(['b'], keep='first', inplace=False))
print('\n------------------')
print(df.drop_duplicates(['b'], keep='first', inplace=False))
with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.colheader_justify', 'light', 'display.width', 2000, 'display.max_colwidth', 500):
    df = df.stack().str.lstrip().unstack()
    print(df)
