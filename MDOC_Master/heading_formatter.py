"""
heading_formatter.py

公文标题字体处理模块

功能:

1. 设置文章标题字体

2. 设置:
    一级标题
    二级标题
    三级标题

3. 支持手工编号标题

    一、标题
    （一）标题
    1.标题


4. 支持Word自动编号标题

    多级列表


5. 同步修改:

    标题正文字体

    Word自动编号字体


"""

import re

from copy import deepcopy

from docx import Document

from docx.enum.text import WD_ALIGN_PARAGRAPH

from docx.oxml import OxmlElement

from docx.oxml.ns import qn

from docx.shared import Pt


from config import (

    HEADING1_FONT_CN,
    HEADING1_FONT_EN,
    HEADING1_FONT_SIZE,

    HEADING2_FONT_CN,
    HEADING2_FONT_EN,
    HEADING2_FONT_SIZE,

    HEADING3_FONT_CN,
    HEADING3_FONT_EN,
    HEADING3_FONT_SIZE,

    TITLE_ALIGNMENT,
    TITLE_FONT_CN,
    TITLE_FONT_EN,
    TITLE_FONT_SIZE,

)


# =====================================================
# 手工编号规则
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
# 清除Run格式
# =====================================================


def clear_run_style(
        run
):

    run.bold = False

    run.italic = False

    run.underline = False

    run.font.strike = False

    run.font.highlight_color = None

    run.font.color.rgb = None


# =====================================================
# 设置Run字体
# =====================================================


def set_run_font(
        run,
        cn,
        en,
        size,
        bold=False
):

    clear_run_style(
        run
    )

    rPr = (
        run._element
        .get_or_add_rPr()
    )

    rFonts = (
        rPr
        .get_or_add_rFonts()
    )

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

    run.font.size = Pt(
        size
    )

    run.bold = bold


# =====================================================
# 获取Word自动编号等级
# =====================================================


def get_word_number_level(
        paragraph
):
    """
    获取Word自动编号级别


    返回:

    1 一级

    2 二级

    3 三级

    """

    pPr = (
        paragraph
        ._p
        .pPr
    )

    if pPr is None:

        return None

    numPr = pPr.find(
        qn("w:numPr")
    )

    if numPr is None:

        return None

    ilvl = numPr.find(
        qn("w:ilvl")
    )

    if ilvl is None:

        return None

    value = ilvl.get(
        qn("w:val")
    )

    if value is None:

        return None

    try:

        level = int(value)

    except ValueError:

        return None

    if level > 2:

        return None

    return level + 1


# =====================================================
# 修改Word编号字体
# =====================================================


def set_numbering_level_font(
        lvl,
        cn,
        en,
        size
):
    """
    修改 numbering.xml 中编号字体
    """

    rPr = lvl.find(
        qn("w:rPr")
    )

    if rPr is None:

        rPr = OxmlElement(
            "w:rPr"
        )

        lvl.append(
            rPr
        )

    rFonts = rPr.find(
        qn("w:rFonts")
    )

    if rFonts is None:

        rFonts = OxmlElement(
            "w:rFonts"
        )

        rPr.append(
            rFonts
        )

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

    sz = rPr.find(
        qn("w:sz")
    )

    if sz is None:

        sz = OxmlElement(
            "w:sz"
        )

        rPr.append(
            sz
        )

    sz.set(
        qn("w:val"),
        str(
            int(size * 2)
        )
    )


def format_word_numbering_font(
        document
):
    """
    同步修改Word自动编号字体
    """

    numbering_part = (
        document.part
        .numbering_part
    )

    root = numbering_part.element

    for abstract_num in root.findall(
            qn("w:abstractNum")
    ):

        for lvl in abstract_num.findall(
                qn("w:lvl")
        ):

            ilvl = lvl.get(
                qn("w:ilvl")
            )

            if ilvl == "0":

                set_numbering_level_font(
                    lvl,
                    HEADING1_FONT_CN,
                    HEADING1_FONT_EN,
                    HEADING1_FONT_SIZE
                )

            elif ilvl == "1":

                set_numbering_level_font(
                    lvl,
                    HEADING2_FONT_CN,
                    HEADING2_FONT_EN,
                    HEADING2_FONT_SIZE
                )

            elif ilvl == "2":

                set_numbering_level_font(
                    lvl,
                    HEADING3_FONT_CN,
                    HEADING3_FONT_EN,
                    HEADING3_FONT_SIZE
                )
# =====================================================
# 判断标题等级
# =====================================================


def detect_heading_level(
        paragraph
):
    """
    判断标题等级

    支持:

    1. 手工编号

    一、标题

    （一）标题

    1.标题


    2. Word自动编号

    """

    text = paragraph.text.strip()

    if not text:

        return None

    # ---------------------------------
    # 优先判断手工编号
    # ---------------------------------

    for level, pattern in HEADING_PATTERNS.items():

        if re.match(
                pattern,
                text
        ):

            return level

    # ---------------------------------
    # 判断Word自动编号
    # ---------------------------------

    return get_word_number_level(
        paragraph
    )


# =====================================================
# 获取标题结束位置
# =====================================================


def get_heading_end(
        text,
        level
):
    """
    获取标题文字结束位置

    支持:

    一、总体情况。正文

    （一）组织领导。正文

    1.任务要求。正文

    """

    if level == 3:

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
# 拆分Run
# =====================================================


def split_run(
        run,
        index
):
    """
    将标题和正文拆开


    原:

    一、标题。正文


    后:

    一、标题。
    正文

    """

    old_text = run.text

    before = old_text[:index]

    after = old_text[index:]

    run.text = before

    new_element = deepcopy(
        run._element
    )

    for child in list(new_element):

        if child.tag == qn("w:t"):

            new_element.remove(
                child
            )

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

    for run in list(
            paragraph.runs
    ):

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
# 判断文章主标题
# =====================================================


def is_document_title(
        paragraph
):

    text = paragraph.text.strip()

    if not text:

        return False

    if detect_heading_level(
            paragraph
    ):

        return False

    if len(text) > 50:

        return False

    return True


# =====================================================
# 设置文章主标题
# =====================================================


def format_title(
        paragraph
):

    for run in paragraph.runs:

        set_run_font(
            run,
            TITLE_FONT_CN,
            TITLE_FONT_EN,
            TITLE_FONT_SIZE
        )

    paragraph.paragraph_format.line_spacing = 1.5

    if TITLE_ALIGNMENT == "center":

        paragraph.alignment = (
            WD_ALIGN_PARAGRAPH.CENTER
        )


# =====================================================
# 主入口
# =====================================================


def format_headings(
        document
):
    """
    标题格式化入口

    """

    # ---------------------------------
    # 第一步:
    # 修改Word自动编号字体
    # ---------------------------------

    format_word_numbering_font(
        document
    )

    title_done = False

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if not text:

            continue

        # -----------------------------
        # 判断文章标题
        # -----------------------------

        if (
            not title_done
            and
            is_document_title(
                paragraph
            )
        ):

            format_title(
                paragraph
            )

            title_done = True

            continue

        # -----------------------------
        # 判断章节标题
        # -----------------------------

        level = detect_heading_level(
            paragraph
        )

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
