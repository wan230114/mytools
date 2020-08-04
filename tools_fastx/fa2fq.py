import sys

fi = sys.argv[1]
fo = sys.argv[2]

with open(fi) as fi, open(fo, 'w') as fo:
    line = fi.readline()
    while line:
        line2 = fi.readline()
        fo.write(line.replace('>', '@'))
        fo.write(line2)
        fo.write('+\n')
        fo.write('F'*len(line2.strip())+'\n')
        line = fi.readline()
