# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-02-21 06:35:27
# @Last Modified by:   JUN
# @Last Modified time: 2019-02-21 07:17:27

import os
import sys
import re
sys.path.append('/ifs/TJPROJ3/Plant/chenjun/mytools/tools_tree')
from itol import itol
import imgcut


def quchong(L):
    """给L去重，并保留顺序
    输入L：[index_a, index_b, s]
    """
    if not L:
        return L
    news_ids = []
    for id in L:
        if id not in news_ids:
            news_ids.append(id)
    L = news_ids
    return L


def merge(L):
    """输入L：[index_a, index_b, s]
    """
    if not L:
        return L
    L = quchong(L)
    L = sorted(L, key=lambda x: x[0])
    cankao = L[0]
    newL = [cankao]
    for Ltmp in L[1:]:
        if cankao[0] < Ltmp[0] < cankao[1]:
            continue
        else:
            newL.append(Ltmp)
    return newL


def func(s, L_cankao):
    """
    输入：s，参考的name
    输出：该name所属层级的L: [index_a, index_b, s]

    """
    # print('【1】', L_cankao)
    Lstmp = []
    for stmp in L_cankao:
        # print(s, '\n', stmp)
        index = s.find(stmp)
        if index == 0:
            Lstmp.append([index, index + len(stmp) - 1, stmp])
            continue
        zhibiao = 0
        new_index_l = index
        while zhibiao >= 0:
            new_index_l -= 1
            if s[new_index_l] == '(':
                zhibiao -= 1
            elif s[new_index_l] == ')':
                zhibiao += 1

        zhibiao = 0
        new_index_r = index
        while zhibiao <= 0:
            new_index_r += 1
            if s[new_index_r] == ')':
                zhibiao += 1
            elif s[new_index_r] == '(':
                zhibiao -= 1
        Ltmp = [new_index_l, new_index_r - 1, s[new_index_l:new_index_r + 1]]
        Lstmp.append(Ltmp)
        # print(Ltmp)
    # print('【2】', Lstmp)
    if Lstmp:
        Lstmp = merge(Lstmp)
    # print('【2】', Lstmp)
    return Lstmp


# 路线1：找2级
# L2ji = get2ji(s)
# LALLindex = find(L2ji, L_cankao_index)

# 路线2：找上一级
def filter(LALLindex, name_sample):
    Lfilter = []
    for Ttmp in LALLindex:
        Ltmp = re.findall(r'[(,](\w.*?)\:', Ttmp[2])
        Lresults = [x for x in Ltmp if x.startswith(
            name_sample[0])]  # 【*】文件名开头，此处需更改
        for gene_ID in Lresults:
            Lfilter.append(gene_ID)
    Lfilter = quchong(Lfilter)
    return Lfilter


def fmain(path, name_sample):
    # 读取文本内容
    with open(path) as fi:
        s = fi.read().rstrip()
        # print(s)
        # s = '(((Pbr030875-v2:0.00000122123005994819,Pbr030912-v2flake8:0.00867762713816672311):0.14670012432348594755,(Pbr013551-v2:0.11698983612402558130,(Pbr013557-v2:0.02594433969524034128,Pbr013553-v2:0.02508626817686426466):0.09135238531156551767):0.07875776760315632286):0.29680039344762859654,((AT4G34230_CAD:0.08848725447611539840,(AT3G19450_CAD:0.14881193053584146346,(Eucgr.G01350_CAD2:0.16368356317116763976,((Pbr010589-v2:0.00000122123005994819,Pbr034241-v2:0.00000122123005994819):0.09815337831284791370,(Pbr004968-v2:0.01774463728257631018,Pbr010590-v2:0.03669137422238939739):0.03113971194200373591):0.06041042479546825106):0.05007958796626876818):0.04226391322369490999):0.57208452272229282087,(((Pbr041059-v2:0.08869428570709157744,(Pbr004359-v2:0.16143105606409705044,Pbr002875-v2:0.12286207489582830210):0.01991286673126243731):0.08456954846815462057,Pbr041060-v2:0.19102116969948551573):0.10767285042034635545,((Pbr000129-v2:0.02698554856217153311,Pbr025233-v2:0.05300734224519917243):0.51411086215101675645,(Pbr040762-v2:0.12363224048810127209,(Pbr003166-v2:0.00592939663302982558,Pbr042572-v2:0.01847351396688658512):0.02076941655634096176):0.23224244317268738502):0.07667997892992209352):0.13367976905594583514):0.20216921406369439684,Pbr041632-v2:2.65075526362319502383):0.0;'

    # 2) 计算
    L_all = re.findall(r'[(,](\w.*?)\:', s)
    L_cankao = [x for x in L_all if not x.startswith(
        name_sample[0])]  # 【*】文件名开头，此处需更改
    L_cankao_index = func(s, L_cankao)

    LALLindex = L_cankao_index.copy()
    # print(LALLindex)
    Lfilter = filter(LALLindex, name_sample)
    # print(Lfilter)

    p = 10
    while len(Lfilter) < 1:
        p -= 1
        if not p:
            break
        Lfilter = []
        # print(LALLindex)
        LALLindex = func(s, [x[2] for x in LALLindex])
        # print(LALLindex)
        Lfilter = filter(LALLindex, name_sample)
    # print(Lfilter)
    itol.fmain(path, path)

    # 将svg的参考基因与挑选基因进行上色
    name_svg = path + '.svg'
    data = open(name_svg, 'r').read()
    data = data.replace(' fill="#000000"', '')
    for gene_ID in quchong(L_cankao):
        gene_ID = gene_ID.replace('_', ' ')
        data = data.replace('>%s</text' %
                            gene_ID, ' fill="red" >%s</text' % gene_ID)
    for gene_ID in quchong(Lfilter):
        data = data.replace('>%s</text' %
                            gene_ID, ' fill="green" >%s</text' % gene_ID)
    with open(name_svg, 'w') as fo:
        fo.write(data)
    # 将svg转换为图片
    stat = os.system('convert %s %s.png' %
                     (name_svg, name_svg))
    if stat:
        print(stat, '转换异常')
    print(path + '转换完毕')
    # 去白边
    imgcut.fmain(name_svg + '.png', name_svg + '.png')


def main():
    if sys.argv[1]=='-h' or sys.argv[1] == '--help' :
        print("""    说明：
        本程序组合了之前itol.py, imgcut.py，在它们基础上开发了上色功能，挑选参考基因标注红色，亲缘关系最近的目标基因标注绿色。
    集群路径:
        /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tree/getTree.py
    使用须知:
        参考是按照匹配的基因名字第一个字母来寻找的，设定为非该字母开头的所有基因都为参考基因
    使用方法：
        python3 getTree.py treepath geneName
    必选参数：
        treepath   输入的树文件的路径
        geneName   目标基因的第一个字母
    实例
        # 实例1：将testdir/ceshi.tre于当前文件夹输出标记颜色的svg文件和裁剪的png
        python3 getTree.py testdir/ceshi.tre M
        """)
        sys.exit()
    path, name_sample = sys.argv[1:3]
    fmain(path, name_sample)

if __name__ == '__main__':
    main()
