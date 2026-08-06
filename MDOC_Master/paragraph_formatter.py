"""
paragraph_formatter.py

Word正文段落格式处理模块


功能:

1. 设置正文段落格式
2. 设置首行缩进
3. 设置固定行距
4. 设置段前段后
5. 设置正文对齐


说明:

本模块只负责正文段落。

不负责:

1. 字体设置
2. 标题格式
3. 表格格式
4. 页面格式


标题格式由:

    heading_formatter.py

负责。


依赖:

python-docx
"""


from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.shared import Cm, Pt

from config import FIRST_LINE_INDENT, LINE_SPACING, SPACE_AFTER, SPACE_BEFORE

# =====================================================
# 设置正文段落格式
# =====================================================


def format_paragraph(
        paragraph
):
    """
    设置单个正文段落格式


    包括:

    1. 首行缩进
    2. 固定行距
    3. 段前段后
    4. 两端对齐

    """

    paragraph_format = (
        paragraph.paragraph_format
    )

    # ---------------------------------
    # 首行缩进
    # ---------------------------------

    paragraph_format.first_line_indent = Cm(
        FIRST_LINE_INDENT
    )

    # ---------------------------------
    # 固定行距
    # ---------------------------------

    paragraph_format.line_spacing_rule = (
        WD_LINE_SPACING.EXACTLY
    )

    paragraph_format.line_spacing = Pt(
        LINE_SPACING
    )

    # ---------------------------------
    # 段前段后
    # ---------------------------------

    paragraph_format.space_before = Pt(
        SPACE_BEFORE
    )

    paragraph_format.space_after = Pt(
        SPACE_AFTER
    )

    # ---------------------------------
    # 正文两端对齐
    # ---------------------------------

    paragraph.alignment = (
        WD_ALIGN_PARAGRAPH.JUSTIFY
    )


# =====================================================
# 格式化所有正文段落
# =====================================================


def format_body_paragraphs(
        document: Document
):
    """
    格式化正文段落


    注意:

    不判断标题。

    标题格式由heading_formatter
    在后续步骤覆盖。


    不处理:

    1. 表格
    2. 页眉
    3. 页脚

    """

    for paragraph in document.paragraphs:

        # 跳过空段落

        if not paragraph.text.strip():

            continue

        format_paragraph(
            paragraph
        )


# =====================================================
# 总入口
# =====================================================


def format_paragraphs(
        document: Document
):
    """
    段落格式统一入口


    main.py调用:

        format_paragraphs(doc)

    """

    format_body_paragraphs(
        document
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

    format_paragraphs(
        doc
    )

    doc.save(
        "paragraph_test.docx"
    )

    print(
        "正文段落格式处理完成"
    )
