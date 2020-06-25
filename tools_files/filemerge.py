import sys

fo = sys.argv[1]
fis = sys.argv[2:]

D_all = {}  # {k:[0,0,0], k2:[0,0,0]}
for n, fi in enumerate(fis):
    with open(fi) as fi:
        for line in fi:
            k, v = line.strip().split('\t')
            if k in D_all and D_all[k][n] != 0:
                print('warning, key:', k, 'will replace for', D_all[k], v)
            D_all.setdefault(k, len(fis)*[0])[n] = int(v)

with open(fo, 'w') as fo:
    fo.write('\t'.join(['#num'] + fis)+'\n')
    for k in D_all:
        print(k, *D_all[k], sep='\t', file=fo)
