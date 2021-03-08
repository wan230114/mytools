#!/usr/bin/env python3

import sys
import argparse


parser = argparse.ArgumentParser(description='Process introduction.')
parser.add_argument('finame', type=str,
                    help='输入制表的tsv列表文件')
parser.add_argument('foname', type=str,
                    help='输出的html')
parser.add_argument('-f', '--force', action='store_true',
                    help='是否强制所有行使用表格，不判断只有第一列的行。')
args = parser.parse_args()


# finame, foname = sys.argv[1:3]
finame, foname = args.finame, args.foname


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

with open(foname, 'w') as fo:
    fo.write(header)
    fo.write("<body>\n")
    table_in = 0
    for Lline in Llines:
        if len(Lline) == 1 and not args.force:
            if table_in == 1:
                fo.write("</table>\n")
            fo.write("<p>%s</p>\n" % Lline[0])
            table_in = 0
        else:
            if table_in == 0:
                fo.write("<table>\n")
            fo.write("<tr>")
            for x in Lline:
                if x.endswith(".png"):
                    fo.write('  <td><p>%s</p><img src="%s" /></td>' % (x, x))
                elif x.endswith(".svg"):
                    fo.write(
                        '  <td><p>%s</p><object data="%s" type="image/svg+xml"></object></td>' % (x, x))
            fo.write("</tr>\n")
            table_in = 1
    fo.write("</table>\n</body>")
