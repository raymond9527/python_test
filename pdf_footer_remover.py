from pypdf import PdfWriter
from pypdf import PdfReader
print(dir(tuple))

# 输入、输出文件
INPUT_PDF = "pdf_footer_remover\input.pdf"
OUTPUT_PDF = "pdf_footer_remover\output.pdf"

# 页脚高度（单位：Point）
FOOTER_HEIGHT = 40

reader = PdfReader(INPUT_PDF)
writer = PdfWriter()

for page in reader.pages:

    # 保持左边界不变
    left = page.cropbox.left

    # 保持右边界不变
    right = page.cropbox.right

    # 原来的上下边界
    bottom = page.cropbox.bottom
    top = page.cropbox.top

    # 只提高下边界（裁掉页脚）
    page.cropbox.lower_left = (
        left,
        bottom + FOOTER_HEIGHT
    )

    # 上边界保持不变
    page.cropbox.upper_right = (
        right,
        top
    )

    writer.add_page(page)

with open(OUTPUT_PDF, "wb") as f:
    writer.write(f)

print("页脚删除完成！")
