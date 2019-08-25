# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-02-21 06:35:27
# @Last Modified by:   JUN
# @Last Modified time: 2019-05-06 23:37:45

import os
import sys
import re
sys.path.append('/ifs/TJPROJ3/Plant/chenjun/mytools/tools_tree')
from itol import itol
import imgcut
import argparse


def fargv():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''本程序用于可视化tree文件
使用方法：
python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tree/getTree_fromFile.py treepath [-mod zc/zm/f info]''',
        epilog="""
    说明：
        本程序组合了之前itol.py, imgcut.py，在它们基础上开发了上色功能，挑选参考基因标注红色，亲缘关系最近的目标基因标注绿色。
    集群路径:
        /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tree/getTree_fromFile.py
    三种模式zc/zm/f助记：
        z--字母，m--目标基因，c--参考基因，f--file参考基因文件，三种模式就是它们组合而来
    实例
        # 实例1：选取以t为开头的基因为参考基因，转换树标记颜色
        python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tree/getTree_fromFile.py ceshi.tre -mod zc t
        # 实例2：选取以M为开头的基因为目标基因，除去目标基因为外的基因为参考基因，转换树标记颜色
        python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tree/getTree_fromFile.py ceshi.tre -mod zm M
        # 实例3：选取以文件file中的列表基因为参考基因，转换树标记颜色
        python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tree/getTree_fromFile.py ceshi.tre -mod f cankao.list
    """)
    parser.add_argument('treepath', type=str,
                        help='treepath    输入需要转换的树文件路径, 如/home/test/test.tre')
    parser.add_argument('-mod', type=str, nargs=2,
                        help='-mod zc A / -mod zm A / -mod f file.list (参考基因的第一个字母 / 目标基因对应的第一个字母 / 给定的参考基因list)')
    args = parser.parse_args()
    mod, info = args.mod
    if mod not in {'zc', 'zm', 'f'}:
        print(args)
        print('error: mod模式输入错误，请在zc/zm/f中三选一\n')
        # parser.parse_args(['', '--help'])
        sys.exit(1)
    Targs = (args.treepath, mod, info)
    print("--------------------------")
    print("输入参数是:\n1、treepath: %s\n2、mod：%s\n3、info：%s" % Targs)
    print("--------------------------\n")
    return Targs[0], Targs[1], Targs[2]


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
def filter(LALLindex, L_cankao):
    Lfilter = []
    for Ttmp in LALLindex:
        Ltmp = re.findall(r'[(,](\w.*?)\:', Ttmp[2])
        Lresults = set(Ltmp) - set(L_cankao)
        for gene_ID in Lresults:
            Lfilter.append(gene_ID)
    Lfilter = quchong(Lfilter)
    return Lfilter


def fmain(treepath, mod, info):
    # 读取文本内容
    print('[--> getTree args:', treepath, mod, ']')
    with open(treepath) as fi:
        Llines = [line.strip() for line in fi.readlines()]
        s = ''.join(Llines)
        # print(s)
        # s = '(((Pbr030875-v2:0.00000122123005994819,Pbr030912-v2flake8:0.00867762713816672311):0.14670012432348594755,(Pbr013551-v2:0.11698983612402558130,(Pbr013557-v2:0.02594433969524034128,Pbr013553-v2:0.02508626817686426466):0.09135238531156551767):0.07875776760315632286):0.29680039344762859654,((AT4G34230_CAD:0.08848725447611539840,(AT3G19450_CAD:0.14881193053584146346,(Eucgr.G01350_CAD2:0.16368356317116763976,((Pbr010589-v2:0.00000122123005994819,Pbr034241-v2:0.00000122123005994819):0.09815337831284791370,(Pbr004968-v2:0.01774463728257631018,Pbr010590-v2:0.03669137422238939739):0.03113971194200373591):0.06041042479546825106):0.05007958796626876818):0.04226391322369490999):0.57208452272229282087,(((Pbr041059-v2:0.08869428570709157744,(Pbr004359-v2:0.16143105606409705044,Pbr002875-v2:0.12286207489582830210):0.01991286673126243731):0.08456954846815462057,Pbr041060-v2:0.19102116969948551573):0.10767285042034635545,((Pbr000129-v2:0.02698554856217153311,Pbr025233-v2:0.05300734224519917243):0.51411086215101675645,(Pbr040762-v2:0.12363224048810127209,(Pbr003166-v2:0.00592939663302982558,Pbr042572-v2:0.01847351396688658512):0.02076941655634096176):0.23224244317268738502):0.07667997892992209352):0.13367976905594583514):0.20216921406369439684,Pbr041632-v2:2.65075526362319502383):0.0;'

    # 2) 计算
    L_all = re.findall(r'[(,](\w.*?)\:', s)
    # print(L_all)
    # [print(x) for x in L_all]
    if mod == 'zc':
        L_cankao = [x for x in L_all if x.startswith(info[0])]
    if mod == 'zm':
        L_cankao = [x for x in L_all if not x.startswith(info[0])]
    elif mod == 'f':
        L_cankao = [x for x in info if x in L_all]
    L_cankao_index = func(s, L_cankao)
    LALLindex = L_cankao_index.copy()
    Lfilter = filter(LALLindex, L_cankao)
    # print(LALLindex)
    # print(L_cankao)
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
        Lfilter = filter(LALLindex, L_cankao)
    # print(Lfilter)
    itol.fmain(treepath, treepath, {"display_mode":2})

    # 将svg的参考基因与挑选基因进行上色
    name_svg = treepath + '.svg'
    data = open(name_svg, 'r').read()
    data = data.replace(' fill="#000000"', '')
    for gene_ID in quchong(L_cankao):
        gene_ID = gene_ID.replace('_', ' ')
        data = data.replace('>%s</text' %
                            gene_ID, ' fill="red" >%s</text' % gene_ID)
    for gene_ID in quchong(Lfilter):
        gene_ID = gene_ID.replace('_', ' ')
        data = data.replace('>%s</text' %
                            gene_ID, ' fill="green" >%s</text' % gene_ID)
    with open(name_svg, 'w') as fo:
        fo.write(data)
    # 将svg转换为图片
    stat = os.system('convert %s %s.png' %
                     (name_svg, name_svg))
    if stat:
        print('[WARNING: 转换异常', stat, treepath, ']')
    print('[转换完毕:', treepath, ']')
    # 去白边
    imgcut.fmain(name_svg + '.png', name_svg + '.png')
    return L_all, L_cankao, Lfilter


def main():
    # sys.argv = ['', 'test.tre', '-z', 'M', '-c', 'fi']
    treepath, mod, info = fargv()
    # treepath, name_sample = sys.argv[1:3]
    if mod == 'f':
        with open(info) as fi:
            info = [line.strip() for line in fi if line.strip()]
    fmain(treepath, mod, info)


if __name__ == '__main__':
    main()
