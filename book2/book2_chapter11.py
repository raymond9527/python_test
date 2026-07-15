# 使用第11章所学习的压缩技巧，将第十章生成的试卷和答案压缩（按照试卷存放，一套试卷和答案放在一个文件夹内，然后压缩）
# TODO 打开一个压缩包；读取答案和试卷；将答案和试卷分别存放在一个文件夹内；关闭压缩
"""
compress_backup.py

功能：
1. 将每份试卷和答案放入独立文件夹
2. 将所有文件夹压缩成一个 ZIP 文件
3. 若已有同名 ZIP,则自动在文件名后加数字
"""

import os
import shutil
import zipfile


def compress_quizzes(
        quiz_folder,
        answer_folder,
        output_folder,
        zip_name="ProvinceQuiz"
):
    """
    参数
    ----------
    quiz_folder
        试卷所在目录

    answer_folder
        答案所在目录

    output_folder
        压缩包保存目录

    zip_name
        压缩包名称（不需要 .zip）
    """

    # ======================
    # 创建临时整理目录
    # ======================

    temp_folder = os.path.join(
        output_folder,
        "_TempQuizFolder"
    )

    # 如果存在旧目录，先删除
    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)

    os.makedirs(temp_folder)

    # ======================
    # 将试卷和答案分别放到对应文件夹
    # ======================

    quiz_files = sorted(os.listdir(quiz_folder))
    answer_files = sorted(os.listdir(answer_folder))

    for quiz_file, answer_file in zip(
            quiz_files,
            answer_files
    ):

        # 提取编号
        number = "".join(
            filter(str.isdigit, quiz_file)
        )

        form_folder = os.path.join(
            temp_folder,
            f"Form{number}"
        )

        os.makedirs(
            form_folder,
            exist_ok=True
        )

        shutil.copy2(
            os.path.join(
                quiz_folder,
                quiz_file
            ),
            os.path.join(
                form_folder,
                quiz_file
            )
        )

        shutil.copy2(
            os.path.join(
                answer_folder,
                answer_file
            ),
            os.path.join(
                form_folder,
                answer_file
            )
        )

    # ======================
    # 自动寻找可用压缩包名称
    # ======================

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    zip_path = os.path.join(
        output_folder,
        zip_name + ".zip"
    )

    count = 1

    while os.path.exists(zip_path):

        zip_path = os.path.join(
            output_folder,
            f"{zip_name}_{count}.zip"
        )

        count += 1

    # ======================
    # 开始压缩
    # ======================

    with zipfile.ZipFile(
            zip_path,
            "w",
            compression=zipfile.ZIP_DEFLATED
    ) as zip_file:

        for root, dirs, files in os.walk(
                temp_folder
        ):

            for file in files:

                file_path = os.path.join(
                    root,
                    file
                )

                relative_path = os.path.relpath(
                    file_path,
                    temp_folder
                )

                zip_file.write(
                    file_path,
                    relative_path
                )

    # ======================
    # 删除临时目录
    # ======================

    shutil.rmtree(temp_folder)

    print()
    print("压缩完成！")
    print(f"压缩文件：{zip_path}")
    print(f"这是第{count}次压缩")
