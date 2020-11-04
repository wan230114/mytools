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


class InputFileERRO(BaseException):
    pass


def fargv():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=('bed区间搜索，输入bed文件为4列，第4列为基因名\n'
                     '输出为：\n'
                     'chr  start_ref  end_ref  gene_ref  '
                     'start_tar  end_tar  gene_tar  dis  type\n'),
        epilog=('注意事项：\n'
                '    None\n'
                ))
    parser.add_argument('inputfile', type=str,
                        help=('输入文件，要求和ref输入文件的区间最多一个重叠'))
    parser.add_argument('-r', '--ref', type=str, required=True,
                        help=('输入文件'))
    parser.add_argument('-o', '--outfile', type=str, default=False,
                        help=('输出文件，省略参数默认为stdout'))
    parser.add_argument('-s', '--spacing', type=str, default="3000,3000",
                        help=('上下游搜索长度，默认为 “3000,3000”'))
    parser.add_argument('-pa', '--print_all', action='store_true',
                        help='是否打印全部inbed内容，未查找到的，用 “.” 补齐')
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
    SEED = [0] + [x[0] for x in D[CHR]]
    LEN_SEED = len(SEED) - 1
    s, e = 0, LEN_SEED
    while True:
        # 1) 二分
        n = int((e - s)/2)
        n = 1 if not n else n
        # 2) 重新分配坐标
        if START < SEED[s+n]:
            e = e - n
        else:
            s = s + n
        # 3）判断退出条件
        if s == e or SEED[s] == START or SEED[e] == START:
            break
    s = 0 if s == 0 else s - 1  # 归位，因为前面加了1，此处index归位
    dis = 0
    # 处理第一个
    if s == 0 and START < D[CHR][s][0]:
        if END < D[CHR][s][0]:
            dis = D[CHR][s][0] - END
            res = D[CHR][s], (dis, "Right")
        else:
            res = D[CHR][s], (dis, "Intersect_right")
            # if END <= D[CHR][s][1]:
            #     raise(InputFileERRO("相交区间跨越多个参考系，请检查输入文件的合理性，出错行：\n"
            #                     "%s\t%s\t%s" % (CHR, START, END)))
    # 处理位于最后一块区间右边
    elif s == len(D[CHR]) - 1:
        if START > D[CHR][s][1]:
            dis = D[CHR][s][1] - START
            res = D[CHR][s], (dis, "Left")
        elif START >= D[CHR][s][0]:
            res = D[CHR][s], (dis, "Intersect_left")
    # 2) 判断区间
    elif START <= D[CHR][s][1]:
        if END <= D[CHR][s][1]:
            res = D[CHR][s], (dis, "Intersect")
        else:
            res = D[CHR][s], (dis, "Intersect_left")
            # if END <= D[CHR][s+1][0]:
            #     raise(InputFileERRO("相交区间跨越多个参考系，请检查输入文件的合理性，出错行：\n"
            #                         "%s\t%s\t%s" % (CHR, START, END)))
    elif START > D[CHR][s][1]:
        if END < D[CHR][s+1][0]:
            # 右侧区间
            # 3) 判断区间距离
            dis_l = START - D[CHR][s][1]
            dis_r = D[CHR][s+1][0] - END
            if dis_l < dis_r:
                dis = -dis_l
                res = D[CHR][s], (dis, "Left")
            elif dis_l > dis_r:
                dis = dis_r
                res = D[CHR][s+1], (dis, "Right")
            else:
                dis = dis_l
                res = (('%s,%s' % (D[CHR][s][0], D[CHR][s+1][0]),
                        '%s,%s' % (D[CHR][s][1], D[CHR][s+1][1]),
                        '%s,%s' % (D[CHR][s][2], D[CHR][s+1][2]),
                        ), ('%s,%s' % (-dis, dis), "Left,Right")
                       )
        else:
            res = D[CHR][s+1], (dis, "Intersect_right")
            # if END <= D[CHR][s+1][1]:
            #     raise(InputFileERRO("相交区间跨越多个参考系，请检查输入文件的合理性，出错行：\n"
            #                         "%s\t%s\t%s" % (CHR, START, END)))
    # print(START, END)
    # from pprint import pprint
    # pprint(D[CHR][s-1:s+10])
    # print(s, e, res)
    # sys.exit()
    # 看是否在指定距离内，如果不在，则不进行查找
    if dis == 0 or \
        (dis > 0 and dis < spacing[0]) or \
            (dis < 0 and -dis < spacing[1]):
        return res
    else:
        return None


def fmain(inputfile, ref, outfile, spacing, print_all):
    try:
        spacing = spacing.split(',')
        spacing = int(spacing[0]), int(spacing[1])
        if spacing[0] <= 0 or spacing[1] <= 0:
            raise(InputFileERRO("Error，上下游数值请输入大于零的数"))
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
                    x = line.split("\t")[0:4]
                    CHR, START, END, NAME = x[0], int(x[1]), int(x[2]), x[3]
                    nearinfo = comp(D_ref, CHR, START, END, spacing)
                    if nearinfo:
                        print(*x,
                              CHR, *nearinfo[0],
                              *nearinfo[1],
                              sep="\t", file=fo)
                    elif print_all:
                        print(*x, ('\t.'*5)[1:])
    except IndexError:
        raise(InputFileERRO("\n---\nErro, 请检查输入文件格式是否正确"))


def main():
    # sys.argv = '.py -pa -s 100000,100000 -r bedsearch.py--test/ref.bed bedsearch.py--test/in.bed'.split()
    # sys.argv = ('.py -s 100000,100000 '
    #             '-r protein_coding.v32.position.bed'
    #             ' in2.bed').split()
    args = fargv()
    # print(*list(args.keys()), sep=", ")
    # print(*list(args.values()), sep=", ")
    fmain(**args)


if __name__ == '__main__':
    main()
