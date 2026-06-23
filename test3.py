# 打字测试
import random
import time
from difflib import SequenceMatcher
# 先生成5个选项（一分钟之内打完的），再设计数组
sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "Typing speed improves with daily consistent practice.",
    "Clear focus and steady rhythm help you type faster.",
    "Accuracy is more important than raw typing speed.",
    "Good posture and relaxed hands improve typing efficiency."
]
choice = random.choice(sentences)
print(f"请用最快的速度将这段话打字：{choice}")
input("按回车键开始计时...")
start = time.time()
answer = input("开始输入吧！:")
end = time.time()
s = SequenceMatcher(None, answer, choice)
size = len(choice)
totaltime = end-start
speed = float(size)/totaltime
print(f"恭喜完成，你一共打了{size}个字符，你一共用时：{totaltime:.2f}秒")
print(f"你的打字速率是每分钟{speed * 60:.2f}个字")
print(f"你的正确率是：{s.ratio() * 100:.2f}%")
