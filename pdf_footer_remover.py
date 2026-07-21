import fitz


def remove_pdf_footer(
        input_pdf,
        output_pdf,
        footer_height=40
):
    """
    删除PDF页脚

    参数
    ----------
    input_pdf : 输入PDF

    output_pdf : 输出PDF

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

        # 添加擦除标记
        page.add_redact_annot(
            footer_rect,
            fill=(1, 1, 1)      # 白色填充
        )

        # 真正删除对象
        page.apply_redactions()

    doc.save(
        output_pdf,
        garbage=4,
        deflate=True
    )

    doc.close()

    print("处理完成！")


if __name__ == "__main__":

    remove_pdf_footer(
        "pdf_footer_remover\input.pdf",
        "pdf_footer_remover\output.pdf",
        footer_height=40
    )
