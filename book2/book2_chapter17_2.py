# 此文件用于测试word模块
from docx import Document

doc = Document("book2\python_docx_test.docx")
for i, p in enumerate(doc.paragraphs):
    print(i, repr(p.text))
