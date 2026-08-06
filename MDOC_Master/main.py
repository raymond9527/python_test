import sys
from pathlib import Path

from document_reader import load_document, save_document
from heading_formatter import format_headings
from page_formatter import format_page
from page_number import add_page_number
from paragraph_formatter import format_paragraphs
from style_formatter import format_document_style
from table_formatter import format_tables
from utils import backup_file, create_directory, log_exception, write_log

# =====================================================
# 路径配置
# =====================================================

if getattr(sys, "frozen", False):

    BASE_DIR = Path(
        sys.executable
    ).parent

else:

    BASE_DIR = Path(
        __file__
    ).resolve().parent


# 输入文件

INPUT_DIR = (
    BASE_DIR /
    "input"
)


# 输出目录

OUTPUT_DIR = (
    BASE_DIR /
    "output"
)


# 备份目录

BACKUP_DIR = (
    BASE_DIR /
    "backup"
)


# =====================================================
# Word格式化主函数
# =====================================================

def format_word(
        input_file,
        output_file
):
    """
    执行Word公文格式转换
    """

    write_log(
        f"开始处理: {input_file.name}"
    )

    # ---------------------------------
    # 读取Word
    # ---------------------------------

    doc = load_document(
        input_file
    )

    # ---------------------------------
    # 字体格式
    # ---------------------------------

    write_log(
        "设置字体格式"
    )

    format_document_style(
        doc
    )

    # ---------------------------------
    # 页面格式
    # ---------------------------------

    write_log(
        "设置页面格式"
    )

    format_page(
        doc
    )

    # ---------------------------------
    # 段落格式
    # ---------------------------------

    write_log(
        "设置段落格式"
    )

    format_paragraphs(
        doc
    )

    # ---------------------------------
    # 标题格式
    # ---------------------------------

    write_log(
        "设置标题格式"
    )

    format_headings(
        doc
    )

   # ---------------------------------
    # 表格格式
    # ---------------------------------
    format_tables(doc)
    write_log(
        "设置表格格式"
    )
    # ---------------------------------
    # 页码
    # ---------------------------------

    write_log(
        "添加页码"
    )

    add_page_number(
        doc
    )

    # ---------------------------------
    # 保存
    # ---------------------------------

    save_document(
        doc,
        output_file
    )

    write_log(
        f"完成: {output_file.name}"
    )


# =====================================================
# 主程序
# =====================================================

def main():

    try:

        # 创建目录

        create_directory(
            INPUT_DIR
        )

        create_directory(
            OUTPUT_DIR
        )

        create_directory(
            BACKUP_DIR
        )

        # 查找Word文件

        files = list(
            INPUT_DIR.glob(
                "*.docx"
            )
        )

        if not files:

            print(
                "未找到Word文件"
            )

            return

        for file in files:

            try:

                # ---------------------
                # 备份
                # ---------------------

                backup = backup_file(
                    file,
                    BACKUP_DIR
                )

                if backup:

                    write_log(
                        f"备份文件: {backup.name}"
                    )

                # ---------------------
                # 输出文件
                # ---------------------

                output_file = (
                    OUTPUT_DIR /
                    file.name
                )

                # ---------------------
                # 格式化
                # ---------------------

                format_word(
                    file,
                    output_file
                )

            except Exception as e:

                log_exception(
                    e,
                    BASE_DIR /
                    "error.log"
                )

    except Exception as e:

        log_exception(
            e,
            BASE_DIR /
            "error.log"
        )


# =====================================================
# 程序入口
# =====================================================
if __name__ == "__main__":

    main()

    input(
        "\n按 Enter 键退出..."
    )
