# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-05-28 15:56:39
# @Last Modified by:   JUN
# @Last Modified time: 2019-05-28 17:16:02

# 输入list，注意，每个文库必须是单lan

import os
import sys


def fmain(finame):
    with open(finame) as fi, \
            open('merge.sh', 'w') as fo, \
            open('merge2.sh', 'w') as fo2:
        cwd = os.getcwd()
        for line in fi:
            sample_wenku, path1, path2 = line.strip().split('\t')
            name_wenku = path1.split('/')[-1]
            L1 = sorted(os.listdir(path1))
            L2 = sorted(os.listdir(path2))
            if len(L1) == len(L2):
                os.system('mkdir -p result/%s 2>/dev/null' % name_wenku)
                f1_L1 = [x for x in L1 if x.endswith('_1.fq.gz')]
                f1_L2 = [x for x in L2 if x.endswith('_1.fq.gz')]
                f2_L1 = [x for x in L1 if x.endswith('_2.fq.gz')]
                f2_L2 = [x for x in L2 if x.endswith('_2.fq.gz')]
                if len(f1_L1) == 1 and len(f2_L1) == 1:
                    fo.write('cd %s && zcat %s/%s %s/%s|gzip >result/%s/%s\n' %
                             (cwd, path1, f1_L1[0], path2, f1_L2[0], name_wenku, f1_L1[0]))
                    fo.write('cd %s && zcat %s/%s %s/%s|gzip >result/%s/%s\n' %
                             (cwd, path1, f2_L1[0], path2, f2_L2[0], name_wenku, f2_L1[0]))
                    print('%s\t%s' % (f1_L1[0], f1_L2[0]))
                    print('%s\t%s' % (f2_L1[0], f2_L2[0]))
                    f1_L1 = [x for x in L1 if x.endswith('_1.adapter.list.gz')]
                    f1_L2 = [x for x in L2 if x.endswith('_1.adapter.list.gz')]
                    f2_L1 = [x for x in L1 if x.endswith('_2.adapter.list.gz')]
                    f2_L2 = [x for x in L2 if x.endswith('_2.adapter.list.gz')]
                    if len(f1_L1) == 1 and len(f2_L1) == 1:
                        fo2.write('''cd %s && zcat %s/%s %s/%s|awk '{if(NR==1)print $0}!/^#/{print$0}'|gzip >result/%s/%s\n''' %
                                  (cwd, path1, f1_L1[0], path2, f1_L2[0], name_wenku, f1_L1[0]))
                        fo2.write('''cd %s && zcat %s/%s %s/%s|awk '{if(NR==1)print $0}!/^#/{print$0}'|gzip >result/%s/%s\n''' %
                                  (cwd, path1, f2_L1[0], path2, f2_L2[0], name_wenku, f2_L1[0]))
                        print('%s\t%s' % (f1_L1[0], f1_L2[0]))
                        print('%s\t%s' % (f2_L1[0], f2_L2[0]))
                        print("%s ----- ok!!\n" % name_wenku)
            else:
                print('WARNING, f1:', L1)
                print('WARNING, f2:', L2)
    # os.system('chmod a+x merge.sh merge2.sh')


def main():
    finame = sys.argv[1]
    fmain(finame)


if __name__ == '__main__':
    main()
