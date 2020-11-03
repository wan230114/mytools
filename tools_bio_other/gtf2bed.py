import sys

finame = sys.argv[1]

with open(finame) as fi:
    for line in fi:
        if line.startswith('#'):
            continue
        Lline = line.strip().split('\t')
        if Lline[2] != "gene":
            continue
        D8 = {}
        for x in Lline[8][0:-1].split(';'):
            xx = x.strip().split()
            D8[xx[0]] = xx[1].strip('"')
        print(
            *[Lline[i-1] for i in [1, 4, 5]],
            D8['gene_name'],
            *[Lline[i-1] for i in [6, 7]],
            sep="\t")
