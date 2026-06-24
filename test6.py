import random

width = 10
height = 10

# 生成二维地图
map_data = [
    [
        1 if x == 0 or y == 0 or x == width-1 or y == height-1
        else random.choices([0, 1], weights=[80, 20])[0]
        for x in range(width)
    ]
    for y in range(height)
]

# 随机放置出口
while True:
    ex = random.randint(1, width - 2)
    ey = random.randint(1, height - 2)

    if map_data[ey][ex] == 0:
        map_data[ey][ex] = 2
        break
# 随机人物位置
while True:
    rx = random.randint(1, width - 2)
    ry = random.randint(1, height - 2)

    if map_data[ry][rx] == 0:
        map_data[ry][rx] = 9
        break


# 打印地图
for row in map_data:
    print(row)
print("现在开始走迷宫，1是墙壁，0是可以走的道路，9是你目前的位置，2是最终出口，按下wasd操纵上下左右行动")
nx = rx
ny = ry
while True:
    movement = input("请输入wasd进行操控方向:")
    if movement == "w":
        ny -= 1
    elif movement == "a":
        nx -= 1
    elif movement == "s":
        ny += 1
    elif movement == "d":
        nx += 1
    if map_data[ny][nx] == 1:
        print("此路不通，请换一条路走")
        nx = rx
        ny = ry
    elif map_data[ny][nx] == 2:
        print("恭喜你找到出口！")
        break
    else:
        map_data[ny][nx] = 9
        map_data[ry][rx] = 0
        rx = nx
        ry = ny
    for row in map_data:
        print(row)
