# 日记记录软件 ，能够写每日的日记，并且根据日记查找指定日记
import os
folder = "D:/python_project/python_test/diary/"
print("""日记本
      1.记录新日记
      2.查看所有日记
      3.退出
      """)
while True:
    try:
        doing = int(input("请输入你要进行的操作(1写日记/2查看日记/3退出)："))
    except ValueError:
        print("请输入数字")
        continue
    if doing == 1:
        date = input("请输入日期（如2026-06-26）：")
        lines = []
        while True:
            line = input("请输入日记内容（回车换行，输入end结束）：")
            if line == "end":
                break
            lines.append(line)
        content = "\n".join(lines)

        with open(folder+date + ".txt", "w", encoding="utf-8") as f:
            f.write(content)
    elif doing == 2:
        print("下面是已记录的日记:")
        for file in os.listdir(folder):
            if file.endswith(".txt"):
                print(file)
        check = input("请输入想要查看的日记名（后缀文件名不需要输入，回车键返回）:")
        if check == "":
            continue
        filepath = os.path.join(folder, check+".txt")
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                print("\n------ 日记内容 ------")
                print(content)
        except FileNotFoundError:
            print("没有找到该日记文件！")

    elif doing == 3:
        print("感谢使用，欢迎下次光临，再见！")
        break
    else:
        print("请输入正确的数字。")
