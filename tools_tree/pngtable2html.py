import sys

finame, foname = sys.argv[1:3]

with open(finame) as fi:
    Llines = [line.strip().split() for line in fi.readlines()]

header = """<!DOCTYPE html>
<html>

<head>
    <title>YJ</title>
    <style>
        table {
            text-align: left;
            /* width: 1000px; */
            border-width: 1px;
            border-style: double;
            /* color: blue; */
        }

        td {
            width: 300px;
            border-width: 1px;
            border-style: dashed;
            valign: top
        }

        img {
            width: 600px;
        }
    </style>
</head>
"""

with open(foname, 'w') as fo:
    fo.write(header)
    fo.write("<body>\n")
    table_in = 0
    for Lline in Llines:
        if len(Lline) == 1:
            if table_in == 1:
                fo.write("</table>\n")
            fo.write("<p>%s</p>\n" % Lline[0])
            table_in = 0
        elif len(Lline) > 1:
            if table_in == 0:
                fo.write("<table>\n")
            fo.write("<tr>")
            for x in Lline:
                if x.endswith(".png"):
                    fo.write('  <td><p>%s</p><img src="%s" /></td>' % (x, x))
                elif x.endswith(".svg"):
                    fo.write('  <td><p>%s</p><object data="%s" type="image/svg+xml"></object></td>' % (x, x))
            fo.write("</tr>\n")
            table_in = 1
    fo.write("</table></body>")
