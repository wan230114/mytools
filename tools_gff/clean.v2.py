# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  wan230114@qq.com
# @Date:   2018-11-20 15:49:39
# @Last Modified by:   JUN
# @Last Modified time: 2018-11-22 12:06:00

# 此函数用于更改gff文件里CDS的相同序号，输出文件为后缀加.Number
# 输入文件gff中的一个基因后面必须将其所有信息放置于下一个基因前，位置错误可能结果报错

import sys
import re
import time

# if sys.version_info[0] < 3:
#     print("Erro: can not run in python2")
#     sys.exit(0)  # exit programe


class clean:

    def __init__(self, Larvg):
        self.finame = Largv[1]
        self.foname = self.finame + '.clean'
        self.Dtype = {'gene': 1, 'mRNA': 2,  'CDS': 3}
        self.fclean()

    def fclean(self):
        t0 = time.time()
        print('正在处理文件: %s' % self.finame)
        fi = open(self.finame, 'rb')
        fo = open(self.foname, 'wb')
        fo.write(b"##gff-version 3\n")
        S_genetype_raw = {b'mRNA', b'CDS'}
        S_genetype = set()
        Nrow = 0
        while True:
            line = fi.readline()
            Nrow += 1
            if not line:
                break
            elif line.startswith(b'#'):
                continue
            Lline = line.split(b'\t')
            Ltmp = []
            # Dgene_info = {}
            if Lline[2] == b'gene':
                Lline.append(0)  # 为排序做准备
                Ltmp.append(Lline)
                ID_gene = re.findall(b'ID=(.*?);', Lline[8])[0]
                # Dgene_info[Lline[2]] = ID_gene
                S_genetype = set()
                while True:
                    line = fi.readline()
                    Lline = line.split(b'\t')
                    Nrow += 1
                    if not line:
                        if S_genetype != S_genetype_raw:
                            Ltmp = []
                        break
                    elif line.startswith(b'#'):
                        continue
                    elif Lline[2] == b'gene':
                        fi.seek(-len(line), 1)
                        Nrow -= 1
                        if S_genetype != S_genetype_raw:
                            Ltmp = []
                            # print('该基因缺失mRNA或CDS，已过滤该基因，位于行数为 %d 之前的一个基因' % Nrow)
                            # print('%s' % line)
                        break
                    elif Lline[2] == b'mRNA':
                        S_genetype.add(b'mRNA')
                        Parent = re.findall(b'Parent=(.*?);+|\n', Lline[8])[0]
                        ID_mRNA = re.findall(b'ID=(.*?);', Lline[8])[0].decode()
                        if Parent != ID_gene:
                            print('mRNA有误，位于 %d 行' % Nrow)
                            print(line)
                            sys.exit()
                        Lline.append(float(ID_mRNA[-1]))  # !!! 特殊情况，只有当mRNA特别唯一，且最后一位为数字时可以正常运行
                        Ltmp.append(Lline)
                    elif Lline[2] == b'CDS':
                        S_genetype.add(b'CDS')
                        Parent = (re.findall(b'Parent=(.*);*|\s', Lline[8])[0]).decode()
                        Lline.append((int(Parent[-1]) + 0.1))  # !!! 同上
                        Ltmp.append(Lline)
                    else:
                        continue
                        # print('文件中含有非gene、mRNA、CDS的行，行数是: %d' % Nrow)
                        # sys.exit()
            if Ltmp:
                Ltmp = sorted(Ltmp, key=lambda x: (x[9], int(x[3]), -int(x[4])))
                n_CDS = 0
                Lnew = []
                for i,Lline in enumerate(Ltmp):  # 去除无CDS对应的mRNA
                    if Lline[2] == b'mRNA':
                        if Ltmp[i+1][2] == b'CDS':
                            Lnew.append(Lline)
                    elif Lline[2] == b'CDS':
                        Lnew.append(Lline)
                    elif Lline[2] == b'gene':
                        Lnew.append(Lline)
                for Lline in Lnew:
                    if Lline[2] == b'mRNA':
                        n_CDS = 0
                    elif Lline[2] == b'CDS':
                        n_CDS += 1
                        oldID = re.findall(b'ID=(.*?);', Lline[8])[0]
                        tmpCDS = re.findall(b'CDS:|:cds', oldID)[0]
                        newID = oldID.replace(tmpCDS, b'')
                        newID = b'ID='+newID + b':cds' + str(n_CDS).encode()
                        Lline[8] = Lline[8].replace(b'ID=%s'%oldID, newID)
                    fo.write(b'\t'.join(Lline[0:9]))
        fo.close()
        print('处理完毕，耗时%f秒' % (time.time() - t0))

if __name__ == "__main__":
    Largv = sys.argv
    # "Arabidopsis_thaliana.TAIR10.37.gff3"
    # Largv = ['', 't.gff3']
    clean(Largv)
