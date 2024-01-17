#!/usr/bin/env python3

# %%

import pandas as pd
import sys

class filebase(object):
    """docstring for filebase."""

    def __init__(self, file):
        # super(filebase, self).__init__()
        self.file = file


f1 = filebase("/output/test-combine-3/1653275727038/67855-9710-CNVseqPLUS-filtered_10k_first.txt")
f2 = filebase("/output/test-combine-3/1653275727038/67855-9710-CNVseqPLUS-CNV_Combined_10k_First.tsv")
#%%
f1 = filebase(sys.argv[1])
f2 = filebase(sys.argv[2])
#%%


def pd_read_table_str(infile, dtype={}, **kwargs):
    # ! 二次读取的解决方案：先读第一行，将所有列指定为str，根据需求手动改类型，二次读取。
    colnames = pd.read_table(
        infile, nrows=1, keep_default_na=False, **kwargs).columns
    dtypes = {x: "str" for x in colnames}
    dtypes.update(dtype)
    # dtype.update({"c1": "int"})  # 根据需要更改
    df = pd.read_table(infile, dtype=dtypes, keep_default_na=False, **kwargs)
    # 如需将NA也识别为字符串，需指定参数，keep_default_na=False
    return df


f1.df = pd.DataFrame(pd_read_table_str(f1.file))
f2.df = pd.DataFrame(pd_read_table_str(f2.file))

# %%
f1.special_col = list(set(f1.df.columns) - set(f2.df.columns))
f2.special_col = list(set(f2.df.columns) - set(f1.df.columns))

# f1.df == f2.df

common = []
diff = []
for col in set(f1.df.columns) & set(f2.df.columns):
    if (f1.df.loc[:, col] == f2.df.loc[:,col]).all():
        common.append(col)
    else:
        diff.append(col)

# f1.df[common]
# 停滞，设计有难度，需要思考如何展示。用相同列做合并，不同列分列展示吗？

print(f"common: {common}")
print(f"f1.special_col: {f1.special_col}")
print(f"f2.special_col: {f2.special_col}")
print(f"diff: {diff}")

pd.concat([f1.df.loc[:, diff], f2.df.loc[:, diff]], axis=1)
