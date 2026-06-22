import random
result = random.randint(1, 100)
guess = 0
while guess != result:
    try:
        guess = int(input("现在开始猜数字（100以内整数），请输入数字："))
        times = 1
        while guess != result:

            if guess > 100:
                print("请不要输入大于100的数！（此次作废）")

            if guess < result:
                print("你的数字太小了！")
                times += 1
            if guess > result:
                print("你的数字太大了！")
                times += 1

            guess = int(input("请继续猜数字："))
        print(f"恭喜你猜对了，你一共猜测了{times}次")
        break
    except ValueError:
        print("我他妈叫你输入100以内整数!")
