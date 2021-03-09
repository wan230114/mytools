#!/usr/bin/env python3


"""
Install:

git clone https://github.com/LankyCyril/pyvenn.git
cd pyvenn
python setup.py install
"""

# %%
import sys
import os
from matplotlib import pyplot as plt
from venn import venn
# from matplotlib_venn import venn2
# pip install matplotlib
# pip install matplotlib_venn


def compare2(fi1_name, fi2_name):
    # fi1_name, fi2_name = "merge_H3K27me3_YJ-A549-3-0uM--VS--YJ-A549-NC_filter_DOWN.genelist", "merge_H3K27me3_YJ-3-0--VS--YJ-NC_filter_DOWN.genelist"
    # out1, out2 = fi1_name, fi2_name
    out1 = os.path.splitext(os.path.basename(fi1_name))[0]
    out2 = os.path.splitext(os.path.basename(fi2_name))[0]

    Outname = out1 + '--VS--' + out2

    # %%  write file
    with open(fi1_name) as fi1, open(fi2_name) as fi2:
        s1 = {x.strip().strip('"') for x in fi1.readlines()}
        s2 = {x.strip().strip('"') for x in fi2.readlines()}

    with open(Outname + '__diff1-A' + '.txt', 'w') as fo:
        diff_A = s1 - s2
        fo.write('\n'.join(diff_A)+"\n")

    with open(Outname + '__diff2-B' + '.txt', 'w') as fo:
        diff_B = s2 - s1
        fo.write('\n'.join(diff_B)+"\n")

    with open(Outname + '__diff0-A-B' + '.txt', 'w') as fo:
        diff_A_B = s1.symmetric_difference(s2)
        fo.write('\n'.join(diff_A_B)+"\n")

    with open(Outname + '__comm0-A-B' + '.txt', 'w') as fo:
        com_A_B = s1.intersection(s2)
        fo.write('\n'.join(com_A_B)+"\n")

    with open(Outname + '__union1-A' + '.txt', 'w') as fo:
        union_A = s1
        fo.write('\n'.join(union_A)+"\n")

    with open(Outname + '__union2-B' + '.txt', 'w') as fo:
        union_B = s2
        fo.write('\n'.join(union_B)+"\n")

    with open(Outname + '__union0-A-B' + '.txt', 'w') as fo:
        union_A_B = s1 | s2
        fo.write('\n'.join(union_A_B)+"\n")

    # %%  plot venn
    # help(venn2)
    anno0 = '%s(%s) vs %s(%s)' % ("A", len(s1), "B", len(s2))
    anno = (
        'Union(ALL): %s (100.00%%) \nComm: %s '
        '(C/U: %.2f%%; C/A: %.2f%%; C/B: %.2f%%;) \n' % (
            len(union_A_B), len(com_A_B),
            len(com_A_B)/len(union_A_B)*100,
            len(com_A_B)/len(s1)*100 if len(s1) > 0 else 0,
            len(com_A_B)/len(s2)*100 if len(s2) > 0 else 0
        ) +
        'Diff: %s (D/U: %.2f%%)  (A:%s  B:%s)\n' % (
            len(diff_A_B),
            len(diff_A_B) / len(union_A_B)*100,
            len(diff_A),
            len(diff_B)) +
        'A: %s \nB: %s' % (out1, out2))
    print(anno0 + '\n' + anno, file=open('%s__venn.doc.txt' % Outname, 'w'))
    plt.title(anno0)
    plt.text(0, -1, anno, ha='center', ma='left')
    venn({out1: s1, out2: s2},
         fmt="{percentage:.1f}%\n({size})",
         #  cmap=["g", "b"]
         cmap=["r", "g"]
         )
    # venn2(subsets=[s1, s2], set_labels=("A", "B"), set_colors=('r', 'g'))
    # venn2(subsets=[s1, s2])  #, set_labels=(out1, out2), set_colors=('r', 'g'))

    # %%
    plt.savefig('%s__venn.pdf' % Outname, dpi=200, bbox_inches='tight')
    plt.savefig('%s__venn.png' % Outname, dpi=200, bbox_inches='tight')
    plt.savefig('%s__venn.svg' % Outname, dpi=200, bbox_inches='tight')


if __name__ == "__main__":
    fi1_name, fi2_name = sys.argv[1:3]
    compare2(fi1_name, fi2_name)
