import fitz
import os
import sys


def get_base_path():
    """
    获取程序运行目录

    兼容：
    1. Python源码运行
    2. PyInstaller打包exe运行
    """

    if getattr(sys, "frozen", False):
        # exe运行
        return os.path.dirname(sys.executable)

    else:
        # Python运行
        return os.path.dirname(
            os.path.abspath(__file__)
        )


def remove_pdf_footer(
        input_pdf,
        output_pdf,
        footer_height=40
):
    """
    删除PDF页脚

    参数
    ----------
    input_pdf : 输入PDF路径

    output_pdf : 输出PDF路径

    footer_height : 页脚高度(pt)
    """

    doc = fitz.open(input_pdf)

    for page in doc:

        width = page.rect.width
        height = page.rect.height

        # 页脚区域
        footer_rect = fitz.Rect(
            0,
            height - footer_height,
            width,
            height
        )

        # 添加删除区域
        page.add_redact_annot(
            footer_rect,
            fill=(1, 1, 1)
        )

        # 执行删除
        page.apply_redactions()

    doc.save(
        output_pdf,
        garbage=4,
        deflate=True
    )

    doc.close()

    print("处理完成！")
    print(
        f"输出文件：{output_pdf}"
    )


if __name__ == "__main__":

    # 获取程序所在目录
    base_path = get_base_path()

    # 当前目录下的input.pdf
    input_file = os.path.join(
        base_path,
        "input.pdf"
    )

    # 输出output.pdf
    output_file = os.path.join(
        base_path,
        "output.pdf"
    )

    # 检查输入文件
    if not os.path.exists(input_file):

        print(
            "错误：当前目录没有找到 input.pdf"
        )

        input(
            "按Enter退出..."
        )

        sys.exit()

    remove_pdf_footer(
        input_file,
        output_file,
        footer_height=40
    )

    input(
        "按Enter退出..."
    )
