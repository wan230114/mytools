"""
编程思想：
 gene1         gene2        gene3
|-----|       |-----|      |------|
s1   e1       s2    e2      s3    e3

  [L1]    [L2]

1. 二分法查找所有起始位置，定位最后一个上游区块，如L1和L2都定位到s1-e1所在参考
2. 判断是否在参考区域内。终点是否是小于该区域，如L1小于e1。结束判断，注释为gene1基因。但L2结束大于e1，继续下面判断
3. 判断L2开始与上一个区块结束距离，L2结束与下一区块开始距离。谁近则以谁作为临近注释基因。如L2注释到gene2
"""


# %%
import sys
import argparse


def fargv():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=('bed区间搜索，输入bed文件为4列，第4列为基因名\n'
                     '输出为：\n'
                     'chr  start_ref  end_ref  gene_ref  '
                     'start_tar  end_tar  gene_tar  dis'),
        epilog=('注意事项：\n'
                '    None\n'
                ))
    parser.add_argument('inputfile', type=str,
                        help=('输入文件'))
    parser.add_argument('-r', '--ref', type=str, required=True,
                        help=('输入文件'))
    parser.add_argument('-o', '--outfile', type=str, default=False,
                        help=('输出文件，省略参数默认为stdout'))
    parser.add_argument('-s', '--spacing', type=str, default="3000,3000",
                        help=('上下游搜索长度，默认为 “3000,3000”'))
    args = parser.parse_args()
    return args.__dict__


def deal_ref(ref):
    D = {}
    with open(ref) as fi:
        for line in fi:
            line = line.strip()
            if line:
                Lline = line.split("\t")
                D.setdefault(Lline[0], []).append(
                    (int(Lline[1]), int(Lline[2]), Lline[3]))
    return D


def comp(D, CHR, START, END, spacing):
    seed = [0] + [x[0] for x in D[CHR]]
    s, e = 0, len(seed) - 1
    # 1) 查找起始位置
    while True:
        if s == e or seed[s] == START or seed[e] == START:
            break
        if START > seed[s]:
            if START < seed[e]:
                e = int((e - s)/2)
            else:
                s = e
    s -= 1  # 归位，因为前面加了1，此处index归位
    # 2) 判断是否在区间内
    if END < D[CHR][s][1]:
        res = D[CHR][s], 0
    # 3) 判断区间距离
    dis_l = START - D[CHR][s][1]
    dis_r = D[CHR][s+1][0] - END
    if dis_l <= dis_r:
        res = D[CHR][s], dis_l
    else:
        res = D[CHR][s+1], -dis_r
    # 看是否在指定距离内，如果不在，则不进行查找
    # print(CHR, START, END, res[-1])
    if (res[-1] > 0 and res[-1] < spacing[0]) or \
            (res[-1] < 0 and -res[-1] < spacing[1]):
        return res
    else:
        return None


def fmain(inputfile, ref, outfile, spacing):
    try:
        spacing = spacing.split(',')
        spacing = int(spacing[0]), int(spacing[1])
        if spacing[0] <= 0 or spacing[1] <= 0:
            print("Error，上下游数值请输入大于零的数", file=sys.stderr)
            raise
    except:
        print(" -s 输入参数有误", file=sys.stderr)
        raise
    fo = open(outfile, 'w') if outfile else sys.stdout

    D_ref = deal_ref(ref)
    try:
        with open(inputfile) as fi:
            for line in fi:
                line = line.strip()
                if line:
                    x = line.split("\t")
                    CHR, START, END, NAME = x[0], int(x[1]), int(x[2]), x[3]
                    nearinfo = comp(D_ref, CHR, START, END, spacing)
                    if nearinfo:
                        print(CHR, *nearinfo[0], *x,
                              nearinfo[1], sep="\t", file=fo)
    except IndexError:
        print("\n---\nErro, 请检查输入文件格式是否正确", file=sys.stderr)
        raise


def main():
    # sys.argv = '.py -r bedsearch.py--test/ref.bed bedsearch.py--test/in.bed'.split()
    args = fargv()
    # print(*list(args.keys()), sep=", ")
    # print(*list(args.values()), sep=", ")
    fmain(**args)


if __name__ == '__main__':
    main()
