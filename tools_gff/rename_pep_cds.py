# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-04-08 14:10:46
# @Last Modified by:   JUN
# @Last Modified time: 2019-04-22 17:27:22

import sys
import collections


def fmain(qianzui, finame_pep, finame_cds):
    num = 0
    qianzui_old = qianzui
    if qianzui[-1] in '0123456789':
        qianzui += '-'
    D = collections.OrderedDict()
    with open(finame_pep) as fi, open(finame_pep + '.new', 'w') as fo:
        for line in fi:
            if line.startswith('>'):
                num += 1
                # oldname = line.strip().split()[0].strip('>').split('_cds_')[-1]
                oldname = line.strip().split()[0].lstrip('>')
                newname = '%s%05d' % (qianzui, num)
                D[oldname] = newname
                line = '>%s\n' % newname
            fo.write(line)
    print('pep替换完成', finame_pep, '-->', finame_pep + '.new')
    with open(finame_cds) as fi, open(finame_cds + '.new', 'w') as fo:
        for line in fi:
            if line.startswith('>'):
                oldname = line.strip().split()[0].lstrip('>')
                # oldname = line.strip().split()[0].strip('>').split('_prot_')[-1]
                if oldname not in D:
                    if oldname + '.p' not in D:
                        if oldname.replace('_cds_', '_prot_') not in D:
                            newname = oldname
                            print(oldname, '未替换成功')
                        else:
                            newname = D[oldname.replace('_cds_', '_prot_')]
                    else:
                        newname = D[oldname + '.p']
                line = '>%s\n' % oldname.replace(oldname, newname)
            fo.write(line)
    print('cds替换完成', finame_cds, '-->', finame_cds + '.new')
    with open(qianzui_old + '_ID.list', 'w') as fo:
        for oldname in D:
            fo.write('%s\t%s\n' % (oldname, D[oldname]))
    print('list写入完毕', '-->', qianzui_old + '_ID.list')


def main():
    qianzui, finame_pep, finame_cds = sys.argv[1:]
    fmain(qianzui, finame_pep, finame_cds)


if __name__ == '__main__':
    main()
