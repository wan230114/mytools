#!/usr/bin/env python3
# %%
import sys
import os
from matplotlib import pyplot as plt
from matplotlib_venn import venn2
# pip install matplotlib
# pip install matplotlib_venn

# fi1_name, fi2_name = "merge_H3K27me3_YJ-A549-3-0uM__vs__YJ-A549-NC_filter_DOWN.genelist", "merge_H3K27me3_YJ-3-0__vs__YJ-NC_filter_DOWN.genelist"
fi1_name, fi2_name = sys.argv[1:3]
out1 = os.path.splitext(os.path.basename(fi1_name))[0]
out2 = os.path.splitext(os.path.basename(fi2_name))[0]

# %%  write file
with open(fi1_name) as fi1, open(fi2_name) as fi2:
    s1 = {x.strip().strip('"') for x in fi1.readlines()}
    s2 = {x.strip().strip('"') for x in fi2.readlines()}

with open('diff_1_' + out1 + '.txt', 'w') as fo:
    diff_A = s1 - s2
    fo.write('\n'.join(diff_A))

with open('diff_2_' + out2 + '.txt', 'w') as fo:
    diff_B = s2-s1
    fo.write('\n'.join(diff_B))

with open('diff_all_' +
          out1 + '_' +
          out2 + '.txt', 'w') as fo:
    diff_A_B = s1.symmetric_difference(s2)
    fo.write('\n'.join(diff_A_B))
with open('com_all_' +
          out1 + '_' +
          out2 + '.txt', 'w') as fo:
    com_A_B = s1.intersection(s2)
    fo.write('\n'.join(com_A_B))

with open('union_all_' +
          out1 + '_' +
          out2 + '.txt', 'w') as fo:
    union_A_B = s1 | s2
    fo.write('\n'.join(union_A_B))

# %%  plot venn
# help(venn2)
anno0 = '%s(%s) vs %s(%s)' % ("A", len(s1), "B", len(s2))
anno = (
    'Union: %s (100.00%%) \nComm: %s '
    '(C/U: %.2f%%; C/A: %.2f%%; C/B: %.2f%%;) \n' % (
        len(union_A_B), len(com_A_B),
        len(com_A_B)/len(union_A_B)*100,
        len(com_A_B)/len(s1)*100,
        len(com_A_B)/len(s2)*100
    ) +
    'Diff: %s (D/U: %.2f%%)  (A:%s  B:%s)\n' % (
        len(diff_A_B), len(diff_A_B) / len(union_A_B)*100,
        len(diff_A),
        len(diff_B)) +
    'A: %s \nB: %s' % (out1, out2))
print(anno0 + '\n' + anno, file=open('venn_%s__vs__%s.stat' % (out1, out2), 'w'))
plt.title(anno0)
plt.text(0, -1, anno, ha='center', ma='left')
venn2(subsets=[s1, s2], set_labels=("A", "B"), set_colors=('r', 'g'))
# venn2(subsets=[s1, s2])  #, set_labels=(out1, out2), set_colors=('r', 'g'))

# %%
plt.savefig('venn_%s__vs__%s.pdf' % (out1, out2), dpi=200, bbox_inches='tight')
plt.savefig('venn_%s__vs__%s.png' % (out1, out2), dpi=200, bbox_inches='tight')
