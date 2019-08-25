# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-22 16:32:01
# @Last Modified by:   JUN
# @Last Modified time: 2019-03-21 13:15:25

import os
import re


def main():
    path = 'out_svg'
    folist = open('%s.table-png.html.xls' % path, 'w')
    L = os.listdir(path)
    L = [x for x in L if x.endswith('.svg.png')]
    # print(L)  #  1.muzhisu_Mdom_RAxML_bestTree.4CL.tre.pep.tre.filter.png
    Llines = [x.split('_') for x in L]
    Lbiao = sorted({x[0] for x in Llines})
    # print(Lbiao)
    Dbiao = {x: [] for x in Lbiao}
    # print(Dbiao)
    for Lline in Llines:
        Dbiao[Lline[0]].append(Lline)
    # print(Dbiao)
    fo = open('%s.table-png.html' % path, 'w')
    fo.write('<html>\n\t<body>\n')
    for biao in Lbiao:
        Llines = Dbiao[biao]
        # [print(x) for x in Llines]
        Lwuzhong = sorted({x[1] for x in Llines})
        Lshuju = sorted({re.findall('bestTree.(.*?).tre.pep.tre.svg.png', x[3])[0]
                         for x in Llines})
        # print(Lshuju)
        fo.write('\t\t<br><table border="9">\n')
        folist.write('\t'.join(['#wuzhong'] + Lshuju) + '\n')
        for wuzhong in Lwuzhong:
            fo.write('\t\t\t<tr>\n')
            Lline_folist = [wuzhong]
            for x in Lshuju:
                file = '_'.join([biao, wuzhong,
                                 'RAxML_bestTree.%s.tre.pep.tre.svg.png' % x])
                # print(file)
                fo.write('\t\t\t\t<td valign="top">\n\t\t\t\t\t<p>%s</p>\n' % file)
                fo.write('\t\t\t\t\t<img src="./%s/%s" /></p>\n\t\t\t\t</td>\n' %
                         (path, file))
                if os.path.exists('./%s/%s' % (path, file)):
                    Lline_folist.append('Y')
                else:
                    Lline_folist.append('N')
            fo.write('\t\t\t</tr>\n')
            folist.write('\t'.join(Lline_folist) + '\n')
        fo.write('\t\t</table>\n')
    fo.write('</body>\n</html>\n')


if __name__ == '__main__':
    main()
