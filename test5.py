import random
scene_pool = [
    "入口大厅",
    "废弃牢房",
    "蜘蛛巢穴",
    "地下水池",
    "骷髅墓室",
    "宝藏密室",
    "陷阱长廊",
    "恶魔祭坛",
    "图书馆",
    "军械库",
    "炼金实验室",
    "地下神殿",
    "被遗忘的监狱",
    "巨龙巢穴",
    "幽灵回廊"
]
hp = 100
food = 15
treasure = 0
floor = 0

print("欢迎你来到地牢，你的任务是在食物耗尽前找到宝藏，每探索一个房间都会消耗一个食物,注意，这里的房间似乎在不断变化，因此很难记录所有的路线")
print("===== 地牢探险开始 =====")
while food > 0 and hp > 0:
    floor += 1
    food -= 1
    input("按回车键进入下一个房间：")
    room = random.choice(scene_pool)

    print("\n-------------------")
    print(f"第 {floor} 次探索")
    print(f"生命值：{hp}")
    print(f"食物：{food}")
    print(f"宝藏：{treasure}")
    print(f"你来到：【{room}】")

    # 入口大厅
    if room == "入口大厅":
        print("这里很安全，你休息了一会。")
        hp += 10
        if hp > 100:
            hp = 100

    # 废弃牢房
    elif room == "废弃牢房":
        print("你搜索牢房...")
        if random.randint(1, 100) <= 50:
            print("找到一个宝藏！")
            treasure += 1
        else:
            print("踩到陷阱，损失10生命。")
            hp -= 10

    # 蜘蛛巢穴
    elif room == "蜘蛛巢穴":
        print("被巨型蜘蛛袭击！")
        hp -= 15

    # 地下水池
    elif room == "地下水池":
        print("喝下清澈泉水。")
        hp += 15
        if hp > 100:
            hp = 100

    # 骷髅墓室
    elif room == "骷髅墓室":
        print("骷髅战士攻击你！")
        hp -= 20

    # 宝藏密室
    elif room == "宝藏密室":
        print("发现宝箱！")
        treasure += 1

    # 陷阱长廊
    elif room == "陷阱长廊":
        damage = random.randint(5, 20)
        print(f"触发陷阱，受到{damage}点伤害。")
        hp -= damage

    # 恶魔祭坛
    elif room == "恶魔祭坛":
        choice = input("献祭10生命换1宝藏？(y/n)：")

        if choice.lower() == "y":
            hp -= 10
            treasure += 1
            print("交易成功。")

    # 图书馆
    elif room == "图书馆":
        print("阅读古籍。")
        hp += 5
        food += 2

    # 军械库
    elif room == "军械库":
        print("找到一些补给。")
        food += 3

    # 炼金实验室
    elif room == "炼金实验室":

        if random.randint(1, 2) == 1:
            print("药剂有效，恢复20生命。")
            hp += 20
            if hp > 100:
                hp = 100
        else:
            print("药剂有毒，损失20生命。")
            hp -= 20

    # 地下神殿
    elif room == "地下神殿":
        print("发现圣物！获得2个宝藏。")
        treasure += 2

    # 被遗忘的监狱
    elif room == "被遗忘的监狱":
        print("幽灵狱卒袭击你。")
        hp -= 10

    # 巨龙巢穴
    elif room == "巨龙巢穴":

        print("巨龙出现！")

        if random.randint(1, 100) <= 30:
            print("你击败了巨龙！")
            treasure += 3
        else:
            print("被巨龙重创！")
            hp -= 30

    # 幽灵回廊
    elif room == "幽灵回廊":
        print("寒冷的幽灵穿过你的身体。")
        hp -= 5

    # 限制生命值上限
    if hp > 100:
        hp = 100

    # 胜利判断
    if treasure >= 5:
        print("\n★★★★★")
        print("你收集到了足够的宝藏！")
        print("成功通关！")
        break

# 游戏结束判断
print("\n===== 游戏结束 =====")

if hp <= 0:
    print("你已经死亡。")

elif food <= 0:
    print("食物耗尽，被迫离开地牢。")

print(f"探索次数：{floor}")
print(f"最终生命：{hp}")
print(f"获得宝藏：{treasure}")
