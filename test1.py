# 简单计算器
print("欢迎使用简单计算器！")
keepgoing = "y"
countlist = ["+", "-", "*", "/", "%", "//", "**"]
while keepgoing == "y":
    try:
        test1 = float(input("请输入第一个数字："))
        count1 = input("请输入运算方式（+，-，*，/，%，//，**）：")
        if count1 in countlist:
            test2 = float(input("请输入第二个数字："))
            result = eval(test1+count1+test2)
            print(f"计算的结果是：{result}")
            keepgoing = input("是否继续?（输入y继续)：").lower()
        else:
            print("你是不是弱智？加减乘除都能输入错误！")
    except ValueError:
        print("请检查你输入的数字！")
