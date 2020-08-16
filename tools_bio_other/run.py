import sys

fi, FC = sys.argv[1], float(sys.argv[2])

with open("WGY-target.bam__vs__HCT116.bam.diff") as fi:
    for line in fi:
        if line.startswith('#'):
            continue
        Lline = line.strip().split()
        if abs(float(Lline[2])) >= FC:
            print(line, end="")
