from docxtpl import DocxTemplate

# 加载模板

doc = DocxTemplate("template1.docx")

# 定义上下文变量

context = {

    "name": "小红",

    "course": "Python全栈开发",

    "date": "2025年4月1日"

}

# 渲染模板

doc.render(context)

# 保存新文档

doc.save("output.docx")

print("Word文档已生成！")

students = [

    {"name": "小红", "course": "Excel自动化", "date": "2025-04-01"},

    {"name": "小明", "course": "Python入门", "date": "2025-04-05"},

    {"name": "小强", "course": "数据分析", "date": "2025-04-08"},

    {"name": "小刚", "course": "前端开发", "date": "2025-04-09"},

    {"name": "小芳", "course": "Java基础", "date": "2025-04-10"},

]

for student in students:

    doc = DocxTemplate("template1.docx")

    doc.render(student)

    doc.save("output.docx")

print("批量生成完毕！")
