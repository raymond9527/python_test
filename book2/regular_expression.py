# 验证美国手机号
import re


def is_phone_number(number):
    if re.fullmatch(r"\d{3}-\d{3}-\d{4}", number) is not None:
        print("你输入的电话号码正确！")
    else:
        print("你输入的电话号码有误！")


while True:
    number = input("请输入美式电话号码格式（123-456-7890）：")
    is_phone_number(number)
