with open('GCA_000001405.15_GRCh38_no_alt_analysis_set--bak') as fi,\
        open('GCA_000001405.15_GRCh38_no_alt_analysis_set', 'w') as fo:
    seq = set('agtcnAGTCN')
    n = 0
    for line in fi:
        n += 1
        if line.startswith('>'):
            fo.write(line)
        else:
            seqline = set(line.strip())
            if seqline <= seq:
                fo.write(line)
            else:
                newline = line
                for x in (seqline - seq):
                    newline = newline.replace(x, 'N')
                fo.write(newline)
                print('----', n)
                print(line, '-->')
                print(newline)
