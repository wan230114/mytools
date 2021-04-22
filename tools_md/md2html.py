#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# @ Author: Chen Jun
# @ Author Email: 1170101471@qq.com
# @ Created Date: 2021-04-20, 23:08:09
# @ Modified By: Chen Jun
# @ Last Modified: 2021-04-22, 10:48:44
#############################################

# ref: [[python]自动化将markdown文件转成html文件 - Ron Ngai - 博客园](https: // www.cnblogs.com/rond/p/5897625.html)
# pip install markdown
# pip install importlib

# 使用方法 python markdown_convert.py filename

# %%
import sys
import os
import datetime
import re
import markdown
import codecs
from bs4 import BeautifulSoup

css = '''
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<style type="text/css">
ul.md_ul li{
    list-style: disc !important;
}
ol.md_ol li{
    list-style: decimal !important;
}
.rightmain {
    background: #ffffff;
}
# md_a {
    text-decoration: underline;
    color: #6090cf;
}
hr {
    display: block;
    unicode-bidi: isolate;
    margin-block-start: 0.5em;
    margin-block-end: 0.5em;
    margin-inline-start: auto;
    margin-inline-end: auto;
    overflow: hidden;
    border-style: inset;
    border-width: 1px;
}
strong {
    font-weight: bold;
}
body {
    display: block;
    margin: 8px;
}

h1 {
    font-size: 2em;
    margin-block-start: 0.67em;
    margin-block-end: 0.67em;
}

h2 {
    font-size: 1.5em;
    margin-block-start: 0.83em;
    margin-block-end: 0.83em;
}

h3 {
    font-size: 1.17em;
    margin-block-start: 1em;
    margin-block-end: 1em;
}


h4 {
    margin-block-start: 1.33em;
    margin-block-end: 1.33em;
}


h5 {
    font-size: 0.83em;
    margin-block-start: 1.67em;
    margin-block-end: 1.67em;
}

h1 h2 h3 h4 h5 {
    display: block;
    margin-inline-start: 0px;
    margin-inline-end: 0px;
    font-weight: bold;
}
</style>
<style type="text/css">
    table {
        border-collapse: collapse;
        border-spacing: 0;
        empty-cells: show;
        border: 1px solid #cbcbcb;
    }

    td, th {
        padding: 0;
        border-left: 1px solid #cbcbcb;
        border-width: 0 0 0 1px;
        font-size: inherit;
        margin: 0;
        overflow: visible;
        padding: .5em 1em;
        background-color: transparent;
        border-bottom: 1px solid #cbcbcb;
    }

    thead {
        background-color: #e0e0e0;
        color: #000;
        text-align: left;
        vertical-align: bottom;
    }

    tbody>tr:last-child>td {
        border-bottom-width: 0;
    }

</style>
</head>
'''
# %%


def main(in_file):
    name = os.path.splitext(in_file)[0]
    out_file = '%s.html' % name
    input_file = codecs.open(in_file, mode="r", encoding="utf-8")
    text = input_file.read()
    # html = markdown.markdown(text)
    html = text.replace('<div ', '<div markdown="1" ')
    # html = text.replace('<center', '<center markdown="block" ')
    # html = text.replace('<table', '<table markdown="block" ')
    # html = text.replace('<tr', '<tr markdown="block" ')
    # html = text.replace('<td', '<td markdown="block" ')
    html = markdown.markdown(text, extensions=[
        'markdown.extensions.tables',
        'markdown.extensions.codehilite',
        'markdown.extensions.fenced_code',
        'markdown.extensions.md_in_html',
        'markdown.extensions.sane_lists'
    ])

    pattern = r'(<img.*?) title=":size=([\d%]*)x*([\d%]*)" />'
    tihuan = r'\1 width="\2" height="\3" />'
    html = re.sub(pattern, tihuan, html)

    pattern = r'''!\[.*?\]\((.*?)(?: +["']:size=([\d%]*)x*([\d%]*)["'])* *\)'''
    tihuan = r'''<img src="\1" width="\2" height="\3" />'''
    html = re.sub(pattern, tihuan, html)

    # pattern, tihuan = r'!\[.*?\]\((.*?)\)', r'<img src="\1" width="320" />'
    html = re.sub(pattern, tihuan, html)
    html = html.replace('<p><center></p>', '<center>')
    html = html.replace('<p></center></p>', '</center>')

    soup = BeautifulSoup(html, 'html.parser')

    # html = html.replace('<a', '<a id="md_a" ')
    for tag in soup.find_all("a"):
        tag.attrs.setdefault("id", []).append("md_a")

    for tag in soup.find_all("ol"):
        tag.attrs.setdefault("class", []).append("md_ol")

    for tag in soup.find_all("ul"):
        tag.attrs.setdefault("class", []).append("md_ul")

    html = str(soup)

    output_file = codecs.open(
        out_file, "w", encoding="utf-8", errors="xmlcharrefreplace")
    output_file.write(css+html)

    print(datetime.datetime.now(), name + ".md  -->  " + name + ".html")

# %%


if __name__ == "__main__":
    # in_file = "/Users/chenjun/GitHub/Product-Lines/README-guanwang"
    for in_file in sys.argv[1:]:
        if os.path.exists(in_file):
            main(in_file)
        else:
            print(datetime.datetime.now(), "Warning, 文件不存在:", in_file)
