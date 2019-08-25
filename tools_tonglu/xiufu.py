# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-02-18 14:33:19
# @Last Modified by:   JUN
# @Last Modified time: 2019-02-18 14:40:23

import os

for wuzhong in ['Mdom', 'Pcui', 'Pdan', 'Pdul', 'Phai', 'Phei', 'Pkue', 'Pnan', 'Ptia', 'Pzao']:
    os.system('cd /ifs/TJPROJ3/Plant/chenjun/prj/prj01-nannongli/01.tonglu-new/ALL_results/2.yixi/%s/gene.result.xls/tree/pep;\
        mkdir xiufu;cd xiufu;\
        ls ..|grep -e pep$|xargs -i ln -s ../{};sh ~/run.sh' % wuzhong)
