# 密码管理器
import json
try:
    with open("passbook_test8.json", "r", encoding="utf-8") as f:
        passbook = json.load(f)
except FileNotFoundError:
    passbook = {}
except json.JSONDecodeError:
    passbook = {}

print("""欢迎使用密码管理器！
      1.添加账号密码
      2.查找账号密码
      3.删除账号密码
      4.显示所有账号
      5.退出
      """)
while True:
    try:
        doing = int(input("请输入操作(1添加/2查找/3删除/4显示所有/5保存并退出)："))
    except ValueError:
        print("请输入数字")
        continue
    if doing == 1:
        account = input("请输入账号名称：")
        password = input("请输入账号密码：")
        if account in passbook:
            replace = input("该用户名已存在，是否覆盖原有账号密码?(y/n):")
            if replace == "y":
                pass
            if replace == "n":
                continue
        passbook[account] = password

    elif doing == 2:
        looking = input("请输入你要查找的账号名称：")
        if looking in passbook:
            print(f"账户名称为：{looking}")
            print(f"账户密码为：{passbook[looking]}")
        else:
            print("查无此账号")
    elif doing == 3:
        looking = input("请输入你要删除的账号名称：")
        if looking in passbook:
            del passbook[looking]
            print("账号已删除")
        else:
            print("查无此账号")
    elif doing == 4:
        print("下面是所有的账号和密码：")
        for key, value in passbook.items():
            print("账户名:", key)
            print("密码:", value)
            print("")
    elif doing == 5:
        print("数据已保存，感谢你的使用，欢迎下次继续使用")
        with open("passbook_test8.json", "w", encoding="utf-8") as f:
            json.dump(passbook, f, ensure_ascii=False, indent=4)
        break

    else:
        print("请输入正确的数字。")
