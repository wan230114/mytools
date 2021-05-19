#!/usr/bin/env python3

import sys
import argparse


parser = argparse.ArgumentParser(description='Process introduction.')
parser.add_argument('finame', type=str,
                    help='输入制表的tsv列表文件')
parser.add_argument('-o', '--foname', type=str, default=None,
                    help='输出的html')
parser.add_argument('-f', '--force', action='store_true',
                    help='是否强制所有行使用表格，不判断只有第一列的行。')
args = parser.parse_args()


# finame, foname = sys.argv[1:3]
finame, foname = args.finame, args.foname
force = args.force

with open(finame) as fi:
    Llines = [line.strip().split() for line in fi.readlines()]

header = """<!DOCTYPE html>
<html>

<head>
    <title>table</title>
    <style>
        p {
            margin: 0 0 10.5px;
            display: block;
            margin-block-start: 0.3em;
            margin-block-end: 1em;
            margin-inline-start: 0px;
            margin-inline-end: 0px;
        }

        table {
            border-collapse: collapse;
            min-width: 450px;
            font-size: 12px;
            border-spacing: 0;
            text-align: left;
            /* width: 1000px; */
            border-width: 1px;
            border-style: double;
            /* color: blue; */
        }

        td {
            padding: 5px 10px;
            font-family:'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
            vertical-align: top;
            width: 500px;
            border-width: 1px;
            /* border-style: dashed; */
            word-wrap:break-word;
            word-break:break-all;
            font-size:14px;
            color: #434242;
            /* color: #605d5d; */
            valign: top;
        }

        img {
            width: 400px;
        }
    </style>
</head>
"""

L_result = []
if foname:
    L_result.append(header)
    L_result.append("<body>\n")
table_in = 0
for Lline in Llines:
    if len(Lline) == 1 and not force:
        if table_in == 1:
            L_result.append("</table>\n")
        L_result.append("<p>%s</p>\n" % Lline[0])
        table_in = 0
    else:
        if table_in == 0:
            L_result.append("<table>\n")
        L_result.append("<tr>")
        for x in Lline:
            if x.endswith(".png"):
                L_result.append('  <td><p>%s</p><img src="%s" /></td>' % (x, x))
            elif x.endswith(".svg"):
                L_result.append(
                    '  <td><p>%s</p><object data="%s" type="image/svg+xml"></object></td>' % (x, x))
        L_result.append("</tr>\n")
        table_in = 1
if table_in:
    L_result.append("</table>\n")
if foname:
    L_result.append("</body>")

foname = open(foname, "w") if foname else sys.stdout
print(*L_result, sep="", end="", file=foname)
