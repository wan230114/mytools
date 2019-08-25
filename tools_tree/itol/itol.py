# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-01-30 15:57:56
# @Last Modified by:   JUN
# @Last Modified time: 2019-05-06 17:54:19

import os
import sys
import shutil
from itolapi import Itol, ItolExport
import argparse


def fargv():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''本程序用于可视化tree文件
使用方法：
python3 itol.py fipath fopath [--option OPTION]''',
        epilog="""可选参数--option <str>：
        str部分需用引号引起来
          --format   转换格式（默认svg，可多选中间用逗号隔开，可选：svg, eps, pdf, png, newick, nexus, phyloxml）
          --display_mode   显示模式，1 =正常，2 =圆形，3 =无根（1，2，3）
          --tree_x   水平移动像素距离（int）
          --tree_y   垂直移动像素距离（int）
          --branchlength_label_size   分支长度标签的字体大小，像素为单位（int）
          --branchlength_display   是否显示支长（0, 1）
          --bootstrap_display  是否显示元数据值（0, 1）
          ...
          更多参数请参考官网: https://itol.embl.de/help.cgi#bExOpt

        实例：
          # 实例1：转换ceshi.tre为myname.svg输出至"out/"下
          python3 itol.py ceshi.tre out/myname
          # 实例2：转换ceshi.tre为myname.svg、myname.pdf和myname.png输出至"out/"下，设置参数：选择输出格式，使用圈形，显示支长
          python3 itol.py ceshi.tre out/myname --option "--format svg,pdf,png --display_mode 2 --branchlength_display 1"
        """)
    parser.add_argument('fipath', type=str,
                        help='输入需要转换的树文件路径, 如/home/test/test.tre')
    parser.add_argument('fopath', type=str,
                        help='输入转换的树文件路径(无需后缀), 如out/Mdom会在目录out下生成Mdom.svg或其他指定格式')
    parser.add_argument('--option', type=str, default=None,
                        help='可选参数，参数部分为字符串，需要引号引起来')
    args = parser.parse_args()
    Doption = dict()
    if args.option:
        args.option = args.option.replace('\n', ' ').replace('--', '\n--')
        Ldic = [x.split() for x in args.option.strip().split('\n')]
        Ldic = [[x[0].lstrip('--'), x[1]] for x in Ldic]
        Doption = dict(Ldic)
        # print(Doption)
    Targs = (args.fipath, args.fopath, args.option)
    print("--------------------------")
    print("输入参数是:\n1、输入路径: %s\n2、输出路径: %s.xxx\n3、可选参数: %s" % Targs)
    print("--------------------------\n")
    return Targs[0], Targs[1], Doption


def upload(finame):
    itol_upload = Itol()
    itol_upload.add_file(finame)
    # itol_upload.params['treeName'] = finame
    # # 查看字典参数
    # itol_upload.print_variables()
    try:
        status = itol_upload.upload()  # SUCCESS: 1234567890
    except Exception:
        status = 0
    if not status:
        print('---> Upload failed.', itol_upload.comm.upload_output.strip())
        return False, 0
    return True, itol_upload.comm.tree_id
    # 查看对象信息
    # print(type(itol_upload.comm.tree_id))
    # # 1234567890
    # print(itol_upload.get_webpage())
    # # http://itol.embl.de/external.cgi?tree=1234567890&restore_saved=1
    # print(itol_upload.get_itol_export())
    # # <ItolEx


def export(fopath, Doption):
    # print('Exporting to %s' % form)
    exp = ItolExport()
    # exp = itol_upload.get_itol_export()  # 从上传处获取信息
    # exp.set_export_param_value('format', 'svg')
    # exp.set_export_param_value('display_mode', 2)
    # exp.set_export_param_value('datasetList', 'dataset1')
    exp.set_export_param_value('align_labels', 0)  # 是否居右，否则靠拢支
    exp.set_export_param_value('tree_y', 12)  # 向下移动10像素
    # exp.set_export_param_value('ignore_branch_length', 1)  # 对齐右侧
    # exp.set_export_param_value('branchlength_label_size', 18)  # 字体大小
    # exp.set_export_param_value('branchlength_display', 1)  # 支长
    # exp.set_export_param_value('branchlength_label_rounding', 0.1)

    for key in Doption:
        exp.set_export_param_value(key, Doption[key])

    # 处理输入格式format
    Lformat = Doption['format'].split(',')
    Sformat = set(Lformat)
    allformat = {'svg', 'eps', 'pdf', 'png', 'newick', 'nexus', 'phyloxml'}
    Sdiff = Sformat.difference(allformat)
    Lsuccess = [x for x in Lformat if x not in Sdiff]

    for houzui in Lformat:
        if houzui not in Sdiff:
            exp.set_export_param_value('format', houzui)
            exp.export('%s.%s' % (fopath, houzui))
            # print('---> %s.%s 转换成功' % (fopath, houzui))
        else:
            print('Warning: %s.%s 转换跳过，格式不支持' % (fopath, houzui))
    return Lsuccess


def fmain(fipath, fopath, Doption={}):
    try:
        foname = fopath.split(os.sep)[-1]
        finame = 'tmp/%s.tree' % foname
        if not os.path.exists('tmp'):
            try:
                os.mkdir('tmp')
            except:
                pass
        if os.sep in fopath:
            fodir = os.sep.join(fopath.split(os.sep)[:-1])
            if not os.path.exists(fodir):
                os.mkdir(fodir)
        shutil.copy(fipath, finame)
        for i in range(10):
            stat, tree_id = upload(finame)
            if stat:
                print('---> Upload success. The ID is : https://itol.embl.de/tree/%s , filepath: %s' %
                      (tree_id, fipath))
                break
            else:
                print('[warning: ] %s 上传失败,正在重新尝试----第%s次' % (fipath, i + 1))
        else:
            print('[Error: ] Export tree failed. Please check: %s' % fipath)
            sys.exit(1)
        # 处理字典参数
        Doption['tree'] = tree_id
        if 'format' not in Doption:
            Doption['format'] = 'svg'
        Lsuccess = export(fopath, Doption)
        try:
            os.remove(finame)
        except Exception:
            pass
        print('[Ok] Export tree success. %s --> %s.%s' %
              (fipath, fopath, ','.join(Lsuccess)))
    except KeyboardInterrupt:
        print('运行终止！')


def main():
    # sys.argv=[
    #     '', '3.shanlichun_Mdom_RAxML_bestTree.A6PR.tre.pep.tre.bipartitions.tre', 'test']
    # sys.argv = ['', 'ceshi.tre', 'test2', '--option', '--1 1 --2 22 --3 33']
    # sys.argv = ['', '--help']
    finame, foname, Doption = fargv()
    if not Doption:
        Doption = {}
    fmain(finame, foname, Doption)


if __name__ == '__main__':
    main()
