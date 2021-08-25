
# %%

# from Bio.Seq import Seq
import pandas as pd
from Bio import SeqIO

onlyLength = True
# StringIO(data)
L_results = []
for seq_record in SeqIO.parse("./fasta_test.fa", "fasta"):
    # for seq_record in SeqIO.parse("/home/chenjun/dataBase/ensembl/hg38.90/fasta/Homo_sapiens.GRCh38.dna.primary_assembly.fa", "fasta"):
    counts_all = len(seq_record)
    if onlyLength:
        print(
            seq_record.id,
            counts_all,
            sep="\t")
    else:
        seqname = ">"+seq_record.description.replace("\t", " ")
        print(seqname)
        SEQ = seq_record.seq.upper()
        counts_A = SEQ.count("A")
        counts_G = SEQ.count("G")
        counts_T = SEQ.count("T")
        counts_C = SEQ.count("C")
        sumATGC = counts_A + counts_G + counts_T + counts_C
        counts_N = SEQ.count("N")
        counts_gap = SEQ.count("-")
        counts_others = counts_all - sumATGC - counts_N - counts_gap
        print(
            # seq_record.id,
            counts_all,
            f'A:{counts_A/counts_all*100:.1f}%,G:{counts_G/counts_all*100:.1f}%,T:{counts_T/counts_all*100:.1f}%,C:{counts_C/counts_all*100:.1f}%,ATGC:{sumATGC/counts_all*100:.1f}%,N:{counts_N/counts_all*100:.1f}%,-:{counts_gap/counts_all*100:.1f}%,others:{counts_others/counts_all*100:.1f}%',
            f'A:{counts_A},G:{counts_G},T:{counts_T},C:{counts_C},ATGC:{sumATGC},N:{counts_N},-:{counts_gap},others:{counts_others}',
            sep="\t"
        )
    L_results.append([seq_record.id, counts_all])

L_results

# %%
df = pd.DataFrame(L_results, columns=["id", "length"])

print(df)
print(df["length"].median())
print(pd.Series([0, 100]).describe([x/100 for x in range(10, 100, 10)]))
# print(df.length.describe([x/100 for x in range(10, 100, 10)]))
# for x in range(10, 100, 10):
#     print(f'N{x}: {(df.length.quantile(x/100))}')
