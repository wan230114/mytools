# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-22 16:32:01
# @Last Modified by:   JUN
# @Last Modified time: 2019-04-04 12:26:22

import os
import re


def main():
    path = 'out_svg'
    L = os.listdir(path)
    L = [x for x in L if x.endswith('-chr.svg')]
    # print(L)  #  1.muzhisu_Mdom_RAxML_bestTree.4CL.tre.pep.tre.filter.png
    Llines = [x.split('_') for x in L]
    Lbiao = sorted({x[0] for x in Llines})
    # print(Lbiao)
    Dbiao = {x: [] for x in Lbiao}
    # print(Dbiao)
    for Lline in Llines:
        Dbiao[Lline[0]].append(Lline)
    # print(Dbiao)
    fo = open('%s.table-svg-chr.html' % path, 'w')
    fo.write('<html>\n\t<body>\n')
    for biao in Lbiao:
        Llines = Dbiao[biao]
        Lwuzhong = sorted({x[1] for x in Llines})
        Lshuju = sorted({re.findall('bestTree.(.*?).tre.pep.tre.svg-chr.svg', x[3])[0]
                         for x in Llines})
        fo.write('\t\t<br><table border="9">\n')
        for wuzhong in Lwuzhong:
            fo.write('\t\t\t<tr>\n')
            for x in Lshuju:
                file = '_'.join([biao, wuzhong,
                                 'RAxML_bestTree.%s.tre.pep.tre.svg-chr.svg' % x])
                fo.write('\t\t\t\t<td valign="top">\n\t\t\t\t\t<p>%s</p>\n' % file)
                fo.write('\t\t\t\t\t<object data="./%s/%s" type="image/svg+xml"></object>\n\t\t\t\t</td>\n' %
                         (path, file))
            fo.write('\t\t\t</tr>\n')
        fo.write('\t\t</table>\n')
    fo.write('</body>\n</html>\n')


if __name__ == '__main__':
    main()
