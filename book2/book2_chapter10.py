# 程序功能
# TODO 编写一份为30人准备的试卷，试卷题目随机排列，生成30个试卷和30个答案txt文件
# TODO 创建考试文件和答案文件
# TODO 将考卷标题写入文件
# TODO 打乱省会的排列顺序
# TODO 随机生成考题

import random
from book2_chapter11 import compress_quizzes
provinces_capitals = {
    "北京市": "北京",
    "天津市": "天津",
    "河北省": "石家庄",
    "山西省": "太原",
    "内蒙古自治区": "呼和浩特",
    "辽宁省": "沈阳",
    "吉林省": "长春",
    "黑龙江省": "哈尔滨",
    "上海市": "上海",
    "江苏省": "南京",
    "浙江省": "杭州",
    "安徽省": "合肥",
    "福建省": "福州",
    "江西省": "南昌",
    "山东省": "济南",
    "河南省": "郑州",
    "湖北省": "武汉",
    "湖南省": "长沙",
    "广东省": "广州",
    "广西壮族自治区": "南宁",
    "海南省": "海口",
    "重庆市": "重庆",
    "四川省": "成都",
    "贵州省": "贵阳",
    "云南省": "昆明",
    "西藏自治区": "拉萨",
    "陕西省": "西安",
    "甘肃省": "兰州",
    "青海省": "西宁",
    "宁夏回族自治区": "银川",
    "新疆维吾尔自治区": "乌鲁木齐",
    "香港特别行政区": "香港",
    "澳门特别行政区": "澳门",
    "台湾省": "台北"
}

for quiz_num in range(30):
    # 创建考卷文件和答案文件
    quiz_file = open(
        f"book2/book2_chapter10_testdata/capitalsquiz{quiz_num+1}.txt",
        "w",
        encoding="utf-8"
    )
    answer_file = open(
        f"book2/book2_chapter10_answerdata/capitalsquiz_answers{quiz_num+1}.txt",
        "w",
        encoding="utf-8"
    )
    quiz_file.write(
        "Name:\n\nDate:\n\nPeriod:\n\n"
    )
    quiz_file.write(
        f"{' '*5} 省会知识小测试 "
        f"(Form {quiz_num+1})\n\n"
    )
  # 获取州列表

    states = list(provinces_capitals.keys())
    # 随机排列

    random.shuffle(states)

    for question_num in range(34):
        state = states[question_num]
        correct_answer = provinces_capitals[state]
        wrong_answers = list(provinces_capitals.values())
        wrong_answers.remove(correct_answer)
        wrong_answers = random.sample(
            wrong_answers,
            3
        )
        answer_options = wrong_answers + [
            correct_answer
        ]
        random.shuffle(answer_options)
        quiz_file.write(
            f"{question_num+1}. "
            f"What is the capital of {state}?\n"
        )
        for i in range(4):

            quiz_file.write(
                f"{'ABCD'[i]}. "
                f"{answer_options[i]}\n"
            )
        quiz_file.write("\n")
        correct_index = answer_options.index(
            correct_answer
        )
        answer_file.write(
            f"{question_num+1}. "
            f"{'ABCD'[correct_index]}\n"
        )
    quiz_file.close()
    answer_file.close()
print("35份随机考卷生成完成！")

compress_or_not = input("请输入是否压缩（Y/N）：")
if compress_or_not == "Y":
    compress_quizzes(r"book2\book2_chapter10_testdata",
                     r"book2\book2_chapter10_answerdata", r"book2\book2_chapter11_compress")
else:
    print("那好吧，再见!")
