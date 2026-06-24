# 个人记账本，记录收入和支出，查看所有交易记录
print("欢迎来到个人记账本")
print("""
      请输入数字来选择要进行的操作：
      1.添加收入/支出
      2.查看记录
      3.计算总余额
      4.退出
      """)
money = 0
dict1 = {}
i = 0
count = 0
while True:
    doing = int(input("请输入你要进行的操作数字(1添加记录/2查看记录/3计算余额/4退出)："))
    if doing == 1:
        io = input("你想要添加收入(i)还是支出(o)?请输入字母i/o:")
        if io == "i":
            reason = input("请输入收入名称：")
            reason_tag = f"{reason}_{i}"
            count = float(input("请输入具体金额："))
            dict1[reason_tag] = count
            money += count
            i += 1
        elif io == "o":
            reason = input("请输入支出名称：")
            reason_tag = f"{reason}_{i}"
            count = -float(input("请输入具体金额："))
            dict1[reason_tag] = count
            money += count
            i += 1
        else:
            print("你有没有文化?请重新开始！")
    elif doing == 2:
        for key, value in dict1.items():
            print(key, value)
    elif doing == 3:
        print(f"现在的总余额是{money}元")
    elif doing == 4:
        print("感谢您使用本系统！")
        break
    else:
        print("请重新输入正确的数字！")
    count = 0
