#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# @ Author: Chen Jun
# @ Author Email: 1170101471@qq.com
# @ Created Date: 2021-04-21, 10:20:34
# @ Modified By: Chen Jun
# @ Last Modified: 2021-04-21, 18:10:21
#############################################

# %%

import sys,os
from bs4 import BeautifulSoup

infile = sys.argv[1] if len(sys.argv) > 1 and os.path.exists(
    sys.argv[1]) else "test.html"

data = open(infile).read()
# data = """
# <body>
#     <p style='blah; color=red' id='bla1'>paragraph1</p>
#     <p style='blah' id='bla2'>paragraph2</p>
#     <p style='blah' id='bla3'>paragraph3</p>
#     <h1 style='blah' id='bla3'>paragraph3</h1>
#     <img style="awesome_image"/>
# </body>"""


soup = BeautifulSoup(data, 'html.parser')

dellist = [
    "blockquote",
    "center",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "hr",
    "ol",
    "p",
    "ul",
    "th",
    "td"
]

styles = {}


def func_split(p):
    return {x.strip() for x in p.attrs['style'].split(";") if x.strip()}


for kw in dellist:
    for p in soup.find_all(kw):
        if 'style' in p.attrs:
            # print(kw, p.attrs['style'])
            styles.setdefault(kw, func_split(p)).update(func_split(p))
            del p.attrs['style']

#%%
# set(soup.__dict__)
#%%
# soup[0]
#%%

print("<style>")
for kw in styles:
    print(kw, '{')
    print(';\n'.join(styles[kw]))
    print('}')
print("</style>")
print(soup)
