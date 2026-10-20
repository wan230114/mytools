#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""将 Markdown 转成同目录下可离线浏览的 HTML。

依赖：python3 -m pip install markdown beautifulsoup4
用法：python3 bin/md2html.py 文档.md [其他文档.md ...]

图片按原始比例缩小，默认不超过正文宽度、屏幕高度的 70% 和 640px。
可用 ![说明](图片路径 ":size=320x240") 进一步限制预览尺寸；只写宽度、
只写高度（:size=x240）和百分比也支持，百分比高度按屏幕高度计算。
点击未设置链接的图片可查看原图。
支持列表内缩进的代码围栏，保留代码内容和原有列表层级。
"""

import argparse
import datetime
from html import escape
from pathlib import Path
import re
import sys

import markdown
from bs4 import BeautifulSoup, Comment
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.util import HTML_PLACEHOLDER_RE


STYLES = """
* {
    box-sizing: border-box;
}
body {
    max-width: 1000px;
    margin: 0 auto;
    padding: 24px;
    color: #24292f;
    background: #fff;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
                 "Microsoft YaHei", sans-serif;
    font-size: 16px;
    line-height: 1.7;
    overflow-wrap: anywhere;
}
a {
    color: #0969da;
    text-underline-offset: 0.15em;
}
a:hover {
    color: #0550ae;
}
h1, h2, h3, h4, h5, h6 {
    margin: 1.5em 0 0.6em;
    font-weight: 600;
    line-height: 1.3;
}
h1 { font-size: 2em; }
h2 { font-size: 1.5em; }
h3 { font-size: 1.25em; }
h4 { font-size: 1em; }
h5 { font-size: 0.875em; }
h6 { font-size: 0.85em; color: #57606a; }
body > :first-child { margin-top: 0; }
p, ul, ol, blockquote, pre, .table-scroll {
    margin: 0 0 1em;
}
li > p { margin: 0.5em 0; }
li > ul, li > ol { margin-bottom: 0; }
blockquote {
    margin-left: 0;
    padding: 0 1em;
    color: #57606a;
    border-left: 4px solid #d0d7de;
}
hr {
    margin: 1.5em 0;
    border: 0;
    border-top: 1px solid #d0d7de;
}
img {
    width: auto;
    height: auto;
    max-width: 100%;
    max-width: min(100%, var(--md-image-width, 100%));
    max-height: 640px;
    max-height: min(70vh, 640px, var(--md-image-height, 640px));
    object-fit: contain;
    vertical-align: middle;
}
.md-image-link img { cursor: zoom-in; }
code, pre {
    font-family: SFMono-Regular, Consolas, "Liberation Mono", monospace;
    font-size: 0.9em;
}
code {
    padding: 0.15em 0.35em;
    background: #f6f8fa;
    border-radius: 4px;
}
pre {
    max-width: 100%;
    padding: 16px;
    overflow-x: auto;
    background: #f6f8fa;
    border-radius: 6px;
    overflow-wrap: normal;
}
pre code {
    padding: 0;
    background: transparent;
    font-size: inherit;
}
.table-scroll {
    max-width: 100%;
    overflow-x: auto;
}
table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.95em;
}
th, td {
    padding: 8px 12px;
    border: 1px solid #d0d7de;
}
th { background: #f6f8fa; text-align: left; }
tbody tr:nth-child(even) { background: #f6f8fa; }
@media (max-width: 600px) {
    body { padding: 16px; }
}
@media print {
    body { max-width: none; padding: 0; }
    img { max-height: 18cm; }
    pre { white-space: pre-wrap; overflow-wrap: anywhere; }
    .table-scroll { overflow: visible; }
}
"""

IMAGE_SIZE = re.compile(r":size=(\d+%?)?(?:x(\d+%?)?)?")
DIMENSION = re.compile(r"\d+%?")
FENCE = re.compile(r"^( *)(`{3,}|~{3,})(.*)$")


class ListFencedCodePreprocessor(Preprocessor):
    """复用内置围栏渲染器，保留列表层级和代码原始缩进。"""

    LIST_ITEM = re.compile(r"^( *)(?:[-+*]|\d+\.)[ \t]+")

    @staticmethod
    def find_closing(lines, start, opening):
        closing = re.compile(r"^" + re.escape(opening.group(1) + opening.group(2)) + r" *$")
        for index in range(start + 1, len(lines)):
            if closing.fullmatch(lines[index]):
                return index
        return None

    def run(self, lines):
        result = []
        list_indents = []
        index = 0
        tab_length = self.md.tab_length
        renderer = self.md.preprocessors["fenced_code_block"]
        while index < len(lines):
            line = lines[index]
            if not line.strip():
                result.append(line)
                index += 1
                continue

            indent = len(line) - len(line.lstrip(" "))
            while list_indents and indent < list_indents[-1]:
                list_indents.pop()
            opening = FENCE.match(line)
            if (opening and list_indents
                    and list_indents[-1] <= indent < list_indents[-1] + tab_length):
                end = self.find_closing(lines, index, opening)
                if end is not None:
                    source = lines[index:end + 1]
                    prefix = " " * indent
                    # 不接受跨出列表的代码行，避免吞入后续普通正文。
                    if all(not entry.strip() or entry.startswith(prefix) for entry in source):
                        source = [entry[indent:] if entry.strip() else "" for entry in source]
                        placeholder = "\n".join(renderer.run(source)).strip("\n")
                        if HTML_PLACEHOLDER_RE.fullmatch(placeholder):
                            result.extend(["", prefix + placeholder, ""])
                            index = end + 1
                            continue

            marker = self.LIST_ITEM.match(line)
            if marker and (indent < tab_length or
                           (list_indents and indent < list_indents[-1] + tab_length)):
                list_indents.append((indent // tab_length + 1) * tab_length)

            result.append(line)
            index += 1
        return result


class ListFencedCodeExtension(Extension):
    def extendMarkdown(self, md):
        # 正常围栏与原始 HTML 已被保护，再处理列表内的缩进围栏。
        md.preprocessors.register(ListFencedCodePreprocessor(md), "list_fenced_code", 19)


def prepare_image(soup, image):
    """把尺寸作为缩略图上限，避免固定宽高导致长图变形。"""
    size = IMAGE_SIZE.fullmatch(image.get("title", ""))
    if size and any(size.groups()):
        del image["title"]
        for attribute, value in zip(("width", "height"), size.groups()):
            if value:
                image[attribute] = value

    limits = []
    for attribute in ("width", "height"):
        value = str(image.get(attribute, ""))
        if not DIMENSION.fullmatch(value):
            continue
        if value.endswith("%"):
            # 高度百分比不依赖未定义的父元素高度。
            unit_value = value if attribute == "width" else value[:-1] + "vh"
        else:
            unit_value = value + "px"
        limits.append("--md-image-{}: {}".format(attribute, unit_value))
    if limits:
        styles = image.get("style", "").rstrip().rstrip(";")
        image["style"] = "; ".join(filter(None, [styles] + limits)) + ";"

    # 保留已有交互行为，以及 picture 中 source/img 的直接子元素关系。
    if (image.get("src") and not image.has_attr("usemap")
            and image.find_parent(["a", "picture", "button", "label", "summary"]) is None):
        link = soup.new_tag("a", href=image["src"], title="查看原图")
        link["class"] = "md-image-link"
        link["target"] = "_blank"
        link["rel"] = "noopener"
        image.wrap(link)


def render_document(text, title):
    html = markdown.markdown(text, extensions=[
        "markdown.extensions.tables",
        "markdown.extensions.codehilite",
        "markdown.extensions.fenced_code",
        "markdown.extensions.md_in_html",
        "markdown.extensions.sane_lists",
        ListFencedCodeExtension(),
    ], extension_configs={
        # 高亮样式随 HTML 一起保存，离线打开不需要额外 CSS 文件。
        "markdown.extensions.codehilite": {"noclasses": True},
    })
    soup = BeautifulSoup(html, "html.parser")
    # 兼容旧文档直接写在 center/div 内的图片；只解析这些容器的文本节点，
    # 不再对整个 HTML 做正则替换，以免修改代码示例和属性中的字面文本。
    for node in list(soup.find_all(string=True)):
        if (isinstance(node, Comment) or node.parent.name not in ("center", "div")
                or node.find_parent(["pre", "code", "script", "style", "textarea"])
                or "![" not in node):
            continue
        # 文本节点里的实体已被解码，重新转义后才交给 Markdown，保留字面标签。
        fragment = BeautifulSoup(markdown.markdown(escape(str(node), quote=False)), "html.parser")
        if fragment.find("img") is not None:
            for paragraph in fragment.find_all("p"):
                paragraph.unwrap()
            node.replace_with(*list(fragment.contents))

    for image in soup.find_all("img"):
        prepare_image(soup, image)

    for table in soup.find_all("table"):
        wrapper = soup.new_tag("div", tabindex="0")
        wrapper["class"] = "table-scroll"
        wrapper["role"] = "region"
        wrapper["aria-label"] = "表格（可横向滚动）"
        table.wrap(wrapper)

    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
{styles}
</style>
</head>
<body>
{body}
</body>
</html>
""".format(title=escape(title), styles=STYLES, body=soup)


def main(in_file):
    input_path = Path(in_file)
    output_path = input_path.with_suffix(".html")
    if (input_path.resolve() == output_path.resolve()
            or (output_path.exists() and input_path.samefile(output_path))):
        raise ValueError("输入文件和输出文件相同，无法转换: {}".format(input_path))
    text = input_path.read_text(encoding="utf-8-sig")
    html = render_document(text, input_path.stem)
    output_path.write_text(html, encoding="utf-8", errors="xmlcharrefreplace")
    print(datetime.datetime.now(), "{}  -->  {}".format(input_path, output_path))
    return output_path


def cli():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", metavar="文件.md", help="要转换的 Markdown 文件")
    args = parser.parse_args()
    failed = False
    for in_file in args.files:
        try:
            main(in_file)
        except (OSError, UnicodeError, ValueError) as error:
            print("转换失败: {}: {}".format(in_file, error), file=sys.stderr)
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(cli())
