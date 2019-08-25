# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2018-12-11 15:25:28
# @Last Modified by:   JUN
# @Last Modified time: 2019-08-12 13:22:34

#! encoding:UTF-8
import cairosvg
import os
import sys


def exportsvg(fromDir, targetDir, exportType):
    print("开始执行转换命令...")
    num = 0
    for a, f, c in os.walk(fromDir):  # 使用walk遍历源目录
        for fileName in c:
            path = os.path.join(a, fileName)  # 获得文件路径
            if os.path.isfile(path) and fileName[-3:] == "svg":  # 判断文件是否为svg类型
                num += 1
                fileHandle = open(path)
                svg = fileHandle.read()
                fileHandle.close()
                exportPath = os.path.join(targetDir, fileName[:-3] + exportType)  # 生成目标文件路径
                exportFileHandle = open(exportPath, 'w')

                if exportType == "png":
                    try:
                        cairosvg.svg2png(bytestring=svg, write_to=exportPath)  # 转换为png文件
                    except:
                        print("error in convert svg file : %s to png." % (path))

                elif exportType == "pdf":
                    try:
                        cairosvg.svg2pdf(bytestring=svg, write_to=exportPath)  # 转换为pdf文件
                    except:
                        print("error in convert svg file: %s to pdf." % (path))

                exportFileHandle.close()
                print("Success Export ", exportType, " -> ", exportPath)

    print("已导出 ", num, "个文件")  # 统计转换文件数量


if __name__ == "__main__":
    #---------------------------------------
    # svgDir = './svg'  # svg文件夹路径
    # exportDir = './svg-new'  # 目的文件夹路径
    svgDir, exportDir = sys.argv[1], sys.argv[2]
    exportFormat = 'pdf'  # pdf#转换类型
    if not os.path.exists(exportDir):
        os.mkdir(exportDir)
    exportsvg(svgDir, exportDir, exportFormat)  # 转换主函数
    #---------------------------------------
