"""
split_articles.py

按分页符分割 Word 文档

功能:
    读取 docx/ 目录下的所有 .docx 文件，
    以分页符为边界将每个文件分割成独立文章，
    每篇文章单独保存为一个 Word 文档。

命名规则:
    原文件名_两位序号.docx
    例如: 原文.docx -> 原文_01.docx, 原文_02.docx, ...

目录结构:
    article_cutter/
    ├── docx/              输入目录（待分割的 .docx）
    ├── output/            输出目录（分割结果）
    └── split_articles.py  本脚本

打包说明:
    使用 PyInstaller 打包后，docx/ 与 output/ 目录
    位于可执行文件（exe）旁边。

依赖:
    python-docx
"""

import io
import sys
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn

# =====================================================
# 路径配置
# =====================================================

# PyInstaller 打包后运行时，__file__ 指向临时解压目录，
# 因此改用 sys.executable 定位可执行文件所在目录，
# 使 docx/ 与 output/ 与 exe 放在一起。

if getattr(sys, "frozen", False):

    BASE_DIR = Path(sys.executable).parent

else:

    BASE_DIR = Path(__file__).resolve().parent

INPUT_DIR = BASE_DIR / "docx"

OUTPUT_DIR = BASE_DIR / "output"


# =====================================================
# 辅助函数
# =====================================================


def has_page_break(paragraph_element) -> bool:
    """
    判断段落是否包含分页符

    分页符是 <w:br w:type="page"/> 元素，
    位于段落的某个 run 内部。
    """

    for br in paragraph_element.iter(qn("w:br")):

        if br.get(qn("w:type")) == "page":

            return True

    return False


def is_empty_paragraph(paragraph_element) -> bool:
    """
    判断段落是否为空（无可见文字内容）
    """

    text = "".join(
        t.text or ""
        for t in paragraph_element.iter(qn("w:t"))
    )

    return not text.strip()


# =====================================================
# 分割逻辑
# =====================================================


def get_body_blocks(body):
    """
    返回 body 中所有块级元素（段落/表格），排除 sectPr
    """

    return [
        child for child in body
        if child.tag in (qn("w:p"), qn("w:tbl"))
    ]


def split_into_segment_ranges(blocks):
    """
    按分页符将块序列拆分成若干索引范围

    每个范围 [start, end) 代表一篇文章的块区间。
    分页符所在的段落作为分隔符，被丢弃。
    """

    ranges = []

    start = 0

    for i, block in enumerate(blocks):

        if block.tag == qn("w:p") and has_page_break(block):

            # 分页符段落：结束当前范围并丢弃该分隔段落

            if i > start:

                ranges.append((start, i))

            start = i + 1

    if start < len(blocks):

        ranges.append((start, len(blocks)))

    return ranges


def strip_empty_boundaries(blocks, start, end):
    """
    调整范围以去除首尾的空段落

    分页符常伴有空段落，分割后这些空段落
    会出现在文章的开头或结尾，需要清理。
    """

    while (
        start < end
        and blocks[start].tag == qn("w:p")
        and is_empty_paragraph(blocks[start])
    ):

        start += 1

    while (
        end > start
        and blocks[end - 1].tag == qn("w:p")
        and is_empty_paragraph(blocks[end - 1])
    ):

        end -= 1

    return start, end


def split_document(input_path, output_dir):
    """
    分割单个 Word 文档

    将源文档完整保存到内存，逐篇重新加载后
    删除不属于该文章的段落，从而完整保留
    超链接、图片等关系（避免出现断裂引用）。

    返回:
        分割出的文章数量
    """

    source = Document(input_path)

    body = source.element.body

    blocks = get_body_blocks(body)

    ranges = split_into_segment_ranges(blocks)

    # 将源文档完整保存到内存，
    # 供每篇文章重新加载以保留所有关系/样式

    buffer = io.BytesIO()

    source.save(buffer)

    source_bytes = buffer.getvalue()

    base_name = input_path.stem

    count = 0

    for start, end in ranges:

        start, end = strip_empty_boundaries(blocks, start, end)

        if start >= end:

            continue

        count += 1

        # 从源文档字节重新加载，得到完整副本

        new_doc = Document(io.BytesIO(source_bytes))

        new_body = new_doc.element.body

        new_blocks = get_body_blocks(new_body)

        # 删除范围之外的块

        for i, block in enumerate(new_blocks):

            if i < start or i >= end:

                new_body.remove(block)

        output_path = output_dir / f"{base_name}_{count:02d}.docx"

        new_doc.save(output_path)

        print(f"  已生成: {output_path.name}")

    return count


# =====================================================
# 主程序
# =====================================================


def main():
    """
    主程序入口
    """

    if not INPUT_DIR.exists():

        print(f"错误: 输入目录不存在 {INPUT_DIR}")

        return

    files = sorted(INPUT_DIR.glob("*.docx"))

    if not files:

        print(f"错误: {INPUT_DIR} 中没有找到 .docx 文件")

        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"找到 {len(files)} 个文件待处理\n")

    total = 0

    for file in files:

        print(f"处理: {file.name}")

        try:

            count = split_document(file, OUTPUT_DIR)

            total += count

            print(f"  -> 分割出 {count} 篇文章\n")

        # 批量处理场景下，单个文件损坏不应中断整批，
        # 因此此处有意捕获所有异常并继续处理其余文件

        except Exception as e:  # noqa: BLE001

            print(f"  -> 处理失败: {e}\n")

    print(f"完成，共分割出 {total} 篇文章，输出目录: {OUTPUT_DIR}")


if __name__ == "__main__":

    main()

    input("\n按 Enter 键退出...")
