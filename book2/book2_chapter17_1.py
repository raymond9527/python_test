# 此文件用于测试pdf模块
import pypdf
reader = pypdf.PdfReader("book2\pypdf_multifeature_test.pdf")
print(len(reader.pages))
# 提取所有图片

for page_number, page in enumerate(reader.pages):

    for image_number, image in enumerate(page.images):

        filename = f"page_{page_number+1}_{image_number+1}_{image.name}"

        with open(filename, "wb") as f:
            f.write(image.data)

# 提取所有文字

text = ""

for page in reader.pages:
    text += page.extract_text()

print(text)
