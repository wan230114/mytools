#!/usr/bin/env python3
# %%
import sys
import os
from matplotlib import pyplot as plt
from matplotlib_venn import venn3
# pip install matplotlib
# pip install matplotlib_venn

# fi1_name, fi2_name = "merge_H3K27me3_YJ-A549-3-0uM--VS--YJ-A549-NC_filter_DOWN.genelist", "merge_H3K27me3_YJ-3-0--VS--YJ-NC_filter_DOWN.genelist"
fi1_name, fi2_name, fi3_name = sys.argv[1:4]
# fi1_name, fi2_name, fi3_name = ['A', 'B', 'C']
# out1, out2, out3 = fi1_name, fi2_name, fi3_name
out1 = os.path.splitext(os.path.basename(fi1_name))[0]
out2 = os.path.splitext(os.path.basename(fi2_name))[0]
out3 = os.path.splitext(os.path.basename(fi3_name))[0]

Outname = out1 + '--VS--' + out2 + '--VS--' + out3

# %%  write file
with open(fi1_name) as fi1, open(fi2_name) as fi2, open(fi3_name) as fi3:
    s1 = {x.strip().strip('"') for x in fi1.readlines()}
    s2 = {x.strip().strip('"') for x in fi2.readlines()}
    s3 = {x.strip().strip('"') for x in fi3.readlines()}

with open(Outname + '__union1-A' +'.txt', 'w') as fo:
    union_A = s1
    fo.write('\n'.join(sorted(union_A))+"\n")
with open(Outname + '__union2-B' +'.txt', 'w') as fo:
    union_B = s2
    fo.write('\n'.join(sorted(union_B))+"\n")
with open(Outname + '__union3-C' +'.txt', 'w') as fo:
    union_C = s3
    fo.write('\n'.join(sorted(union_C))+"\n")
with open(Outname + '__union0-A-B-C' +'.txt', 'w') as fo:
    union_A_B_C = s1 | s2 | s3
    fo.write('\n'.join(sorted(union_A_B_C))+"\n")

# %%
with open(Outname + '__diff1-A' + '.txt', 'w') as fo:
    diff_A = s1 - s2 - s3
    fo.write('\n'.join(sorted(diff_A))+"\n")
with open(Outname + '__diff2-B' + '.txt', 'w') as fo:
    diff_B = s2 - s1 - s3
    fo.write('\n'.join(sorted(diff_B))+"\n")
with open(Outname + '__diff3-C' + '.txt', 'w') as fo:
    diff_C = s3 - s1 - s2
    fo.write('\n'.join(sorted(diff_C))+"\n")
with open(Outname + '__diff0-A-B-C' + '.txt', 'w') as fo:
    diff_A_B_C = diff_A | diff_B | diff_C
    fo.write('\n'.join(sorted(diff_A_B_C))+"\n")

with open(Outname + '__comm1-A-B' + '.txt', 'w') as fo:
    comm_A_B = s1 & s2
    fo.write('\n'.join(sorted(comm_A_B))+"\n")
with open(Outname + '__comm2-A-C' + '.txt', 'w') as fo:
    comm_A_C = s1 & s3
    fo.write('\n'.join(sorted(comm_A_C))+"\n")
with open(Outname + '__comm3-B-C' + '.txt', 'w') as fo:
    comm_B_C = s2 & s3
    fo.write('\n'.join(sorted(comm_B_C))+"\n")
with open(Outname + '__comm0-A-B-C' + '.txt', 'w') as fo:
    comm_A_B_C = s1 & s2 & s3
    fo.write('\n'.join(sorted(comm_A_B_C))+"\n")

# print(sorted(union_A_B_C))
# print(sorted(comm_A_B_C))
# print(sorted(diff_A))
# print(sorted(diff_B))
# print(sorted(diff_C))

# %%  plot venn
# help(venn2)
anno0 = '%s(%s) vs %s(%s) vs %s(%s)' % (
    "A", len(s1), "B", len(s2), "C", len(s3))

# 'Comm/A: %.2f%%; Comm/B: %.2f%%; Comm/C: %.2f%%; \n'
# len(comm_A_B_C)/len(s1)*100 if len(s1) > 0 else 0,
# len(comm_A_B_C)/len(s2)*100 if len(s2) > 0 else 0,
# len(comm_A_B_C)/len(s3)*100 if len(s2) > 0 else 0
anno = (
    'Union(ALL): %s\n' % (len(union_A_B_C)) +
    'Comm: %s (Comm/Union: %.2f%%) (A_B: %s  B_C: %s  A_C: %s)\n' % (
        len(comm_A_B_C),
        len(comm_A_B_C)/len(union_A_B_C)*100,
        len(comm_A_B),
        len(comm_B_C),
        len(comm_A_C),
    ) +
    'Diff: %s (A:%s B:%s C:%s) (Diff/Union: %.2f%%);\n' % (
        len(diff_A_B_C),
        len(diff_A),
        len(diff_B),
        len(diff_C),
        len(diff_A_B_C)/len(union_A_B_C)*100,
    ) +
    'A: %s \nB: %s \nC: %s' % (out1, out2, out3))
print(anno0 + '\n' + anno, file=open('%s__venn.doc.txt' % Outname, 'w'))
plt.title(anno0)
plt.text(0, -1.1, anno, ha='center', ma='left')
venn3(subsets=[s1, s2, s3], set_labels=(
    "A", "B", "C"), set_colors=('r', 'b', 'g'))
# venn2(subsets=[s1, s2])  #, set_labels=(out1, out2), set_colors=('r', 'g'))

# %%
plt.savefig('%s__venn.pdf' % Outname, dpi=200, bbox_inches='tight')
plt.savefig('%s__venn.png' % Outname, dpi=200, bbox_inches='tight')
plt.savefig('%s__venn.svg' % Outname, dpi=200, bbox_inches='tight')
