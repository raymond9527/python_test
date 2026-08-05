"""
heading_formatter.py

公文标题字体处理模块

功能:

1. 设置文章标题字体

2. 设置:
    一级标题
    二级标题
    三级标题

3. 支持标题正文同段

例如:

一、总体情况。正文内容……

只修改:

一、总体情况。

不影响:

正文内容

"""


import re

from copy import deepcopy

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn


from config import (

    TITLE_FONT_CN,
    TITLE_FONT_EN,
    TITLE_FONT_SIZE,
    TITLE_ALIGNMENT,


    HEADING1_FONT_CN,
    HEADING1_FONT_EN,
    HEADING1_FONT_SIZE,


    HEADING2_FONT_CN,
    HEADING2_FONT_EN,
    HEADING2_FONT_SIZE,


    HEADING3_FONT_CN,
    HEADING3_FONT_EN,
    HEADING3_FONT_SIZE,

)


# =====================================================
# 标题编号
# =====================================================


HEADING_PATTERNS = {


    1:
    r"^[一二三四五六七八九十百]+[、．.]",


    2:
    r"^[（(][一二三四五六七八九十百]+[）)]",


    3:
    r"^\d+[、．.]"

}


# =====================================================
# 清除格式
# =====================================================


def clear_run_style(run):

    run.bold = False
    run.italic = False
    run.underline = False

    run.font.strike = False

    run.font.highlight_color = None

    run.font.color.rgb = None


# =====================================================
# 设置字体
# =====================================================

def set_run_font(
        run,
        cn,
        en,
        size,
        bold=False
):

    clear_run_style(run)

    rPr = run._element.get_or_add_rPr()

    rFonts = rPr.get_or_add_rFonts()

    rFonts.set(
        qn("w:eastAsia"),
        cn
    )

    rFonts.set(
        qn("w:ascii"),
        en
    )

    rFonts.set(
        qn("w:hAnsi"),
        en
    )

    run.font.name = en

    run.font.size = Pt(size)

    # 新增
    run.bold = bold
# =====================================================
# 判断标题等级
# =====================================================


def detect_heading_level(text):

    text = text.strip()

    for level, pattern in HEADING_PATTERNS.items():

        if re.match(
                pattern,
                text
        ):

            return level

    return None


# =====================================================
# 获取标题结束位置
# =====================================================


def get_heading_end(
        text,
        level
):
    """
    获取标题结束位置

    支持:

    一、总体情况。正文

    （一）加强组织领导。正文

    1.建立任务机制。正文

    """

    # 一级、二级、三级统一处理

    if level == 3:

        # 跳过编号中的点

        match = re.search(
            r"\d+[、．.](.+?[。．.])",
            text
        )

    else:

        match = re.search(
            r".+?[。．.]",
            text
        )

    if match:

        return match.end()

    return len(text)

# =====================================================
# XML方式拆分Run
# =====================================================


def split_run(
        run,
        index
):
    """
    将一个Run拆分为两个Run

    原:

    标题正文


    后:

    标题
    正文

    """

    old_text = run.text

    before = old_text[:index]

    after = old_text[index:]

    run.text = before

    new_element = deepcopy(
        run._element
    )

    # 删除原文字节点

    for child in new_element:

        if child.tag == qn("w:t"):

            new_element.remove(child)

    from docx.oxml import OxmlElement

    text_element = OxmlElement(
        "w:t"
    )

    text_element.text = after

    new_element.append(
        text_element
    )

    run._element.addnext(
        new_element
    )


# =====================================================
# 修改标题Run
# =====================================================


def format_heading_runs(
        paragraph,
        length,
        level
):

    if level == 1:

        cn = HEADING1_FONT_CN
        en = HEADING1_FONT_EN
        size = HEADING1_FONT_SIZE
        bold = False

    elif level == 2:

        cn = HEADING2_FONT_CN
        en = HEADING2_FONT_EN
        size = HEADING2_FONT_SIZE
        bold = False

    else:

        cn = HEADING3_FONT_CN
        en = HEADING3_FONT_EN
        size = HEADING3_FONT_SIZE
        bold = True

    remain = length

    for run in list(paragraph.runs):

        if remain <= 0:

            break

        text = run.text

        if not text:

            continue

        text_len = len(text)

        if text_len <= remain:

            set_run_font(
                run,
                cn,
                en,
                size,
                bold
            )

            remain -= text_len

        else:

            split_run(
                run,
                remain
            )

            set_run_font(
                run,
                cn,
                en,
                size,
                bold
            )

            break


# =====================================================
# 判断主标题
# =====================================================


def is_document_title(
        paragraph
):

    text = paragraph.text.strip()

    if not text:

        return False

    if detect_heading_level(text):

        return False

    # 防止正文误判

    if len(text) > 50:

        return False

    return True


# =====================================================
# 设置主标题
# =====================================================


def format_title(paragraph):

    for run in paragraph.runs:

        set_run_font(
            run,
            TITLE_FONT_CN,
            TITLE_FONT_EN,
            TITLE_FONT_SIZE,
        )
    paragraph.paragraph_format.line_spacing = 1.5
    # 修改为1.5倍行距

    if TITLE_ALIGNMENT == "center":

        paragraph.alignment = (
            WD_ALIGN_PARAGRAPH.CENTER
        )


# =====================================================
# 主入口
# =====================================================


def format_headings(document):

    title_done = False

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if not text:

            continue

        if not title_done and is_document_title(paragraph):

            format_title(
                paragraph
            )

            title_done = True

            continue

        level = detect_heading_level(text)

        if level:

            end = get_heading_end(
                text,
                level
            )

            format_heading_runs(
                paragraph,
                end,
                level
            )

    return document


# =====================================================
# 测试
# =====================================================

if __name__ == "__main__":

    from config import INPUT_FILE

    doc = Document(
        INPUT_FILE
    )

    format_headings(
        doc
    )

    doc.save(
        "heading_test.docx"
    )

    print(
        "标题处理完成"
    )
