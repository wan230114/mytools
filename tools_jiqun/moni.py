# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  wan230114@qq.com
# @Date:   2018-11-09 20:41:10
# @Last Modified by:   JUN
# @Last Modified time: 2018-11-14 22:12:42

import time
import os

mkpath = 'tmp'  # 输出文件夹
isExists = os.path.exists(mkpath)
if not isExists:
    os.makedirs(mkpath)

S_list = set(["[tjbnode01]","[tjbnode03]","[tjbnode07]","[tjbnode11]","[tjbnode12]","[tjbnode14]","<tjnode26>","<tjnode27>","<tjnode28>","<tjnode29>","<tjnode30>","<tjnode93>","<tjnode94>","<tjnode176>","<tjnode177>","<tjnode178>","<tjnode179>","<tjnode180>","<tjnode181>","<tjnode185>","<tjnode186>","<tjnode187>","<tjnode287>","<tjnode288>","<tjnode289>","<tjnode290>","<tjnode291>","<tjnode292>","<tjnode293>","<tjnode294>","<tjnode295>","<tjnode296>","<tjnode297>","<tjnode298>","<tjnode299>","<tjnode300>","<tjnode301>","<tjnode341>","<tjnode352>","<tjnode364>","<tjnode370>","<tjnode371>","<tjnode372>","<tjnode373>","<tjnode374>","<tjnode375>","<tjnode376>","<tjnode377>","<tjnode378>","<tjnode379>","<tjnode380>","<tjnode386>","<tjnode401>","<tjnode402>","<tjnode403>","<tjnode404>","<tjnode405>","<tjnode406>"])

S_list2 = set([
    '[tjbnode01]',
    '[tjbnode03]',
    '[tjbnode07]',
    '[tjbnode11]',
    '[tjbnode12]',
    '[tjbnode14]'])

# 总时间
day = 3
minis_day = day * 24 * 60
# 间隔分钟数
minis = 10
secs = minis * 60

while True:
    minis_day -= minis
    if minis_day < 0:
        break
    os.system('/home/leiyang/local/bin/cx >tmp/cxtmp')
    fi = open('tmp/cxtmp')
    fo = open('tmp/cxtmp.log', 'a')
    freedata = ''
    for line in fi:
        Lline = line.split()
        if Lline[0] in S_list:
            cpu = int(Lline[1])
            vf = float(Lline[4])
            sdate = time.strftime('%Y-%m-%d %H:%M:%S',
                                  time.localtime(time.time()))
            fo.write('%s\t%s\t%d\t%.1f\n' % (sdate, Lline[0], cpu, vf))
            if cpu > 20 and vf > 20:
                freedata += '\n节点为%s，cpu为%d，内存为%.1f' % (Lline[0], cpu, vf)
    if freedata:
        os.system(
            'python /ifs/TJPROJ3/Plant/chenjun/mytools/sendmail.py 1170101471@qq.com "嗨，节点空闲啦，当前情况：%s"' % freedata)
        #os.system(
        #    'python /ifs/TJPROJ3/Plant/chenjun/mytools/sendmail.py 1050502282@qq.com "嗨，节点空闲啦，当前情况：%s"' % freedata)
    fi.close()
    fo.close()
    time.sleep(secs)
