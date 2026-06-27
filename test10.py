import random

board = [[" " for x in range(3)] for y in range(3)]


def print_board():
    print("\n  1   2   3")
    for i in range(3):
        print(i + 1, end=" ")
        print(" | ".join(board[i]))
        if i != 2:
            print(" ---+---+---")


def check_win(player):
    # 行
    for row in board:
        if row == [player, player, player]:
            return True

    # 列
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True

    # 主对角线
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True

    # 副对角线
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True

    return False


def check_draw():
    for row in board:
        if " " in row:
            return False
    return True


while True:

    print_board()

    # 玩家
    while True:

        try:
            row = int(input("请输入行(1~3)：")) - 1
            col = int(input("请输入列(1~3)：")) - 1
        except ValueError:
            print("请输入数字！")
            continue

        if row not in range(3) or col not in range(3):
            print("坐标错误")
            continue

        if board[row][col] != " ":
            print("已有棋子")
            continue

        board[row][col] = "X"
        break

    if check_win("X"):
        print_board()
        print("玩家获胜！")
        break

    if check_draw():
        print_board()
        print("平局！")
        break

    # 电脑
    while True:
        r = random.randint(0, 2)
        c = random.randint(0, 2)

        if board[r][c] == " ":
            board[r][c] = "O"
            break

    if check_win("O"):
        print_board()
        print("电脑获胜！")
        break

    if check_draw():
        print_board()
        print("平局！")
        break
