# 成语接龙
import random
idioms = [
    "一心一意",
    "意气风发",
    "发扬光大",
    "大展宏图",
    "图穷匕见",
    "见多识广",
    "广开言路",
    "路不拾遗",
    "遗臭万年",
    "年富力强",
    "强词夺理",
    "理直气壮"
]
start = random.choice(idioms)
lastcase = 11
while idioms.index(start) == lastcase:
    start = random.choice(idioms)
while True:
    try:
        print(f"现在开始成语接龙，你的成语是：{start}")
        answer = input("请输入下一个成语：")
        while len(answer) != 4:
            answer = input("请输入四字成语：")
        if answer[0] == start[-1] and answer in idioms:
            print(f"回答正确！你接的成语是：{answer}")
            index = idioms.index(answer)
            start = idioms[index+1]
        else:
            input("答案错误！游戏结束。")
            break
    except IndexError:
        print("恭喜你过关！")
        break
