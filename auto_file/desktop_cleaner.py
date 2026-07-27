# 每日将桌面上的常用文件收集进入指定文件夹（按每日日期命名），并且按照文件类型分类（不常用的放进杂项），随后将文件放入回收站
from pathlib import Path
from shutil import copy2
from datetime import datetime

# ==========================
# 1. 获取桌面路径
# ==========================

desktop = Path.home() / "Desktop"

# ==========================
# 2. 创建日期文件夹
# ==========================

today = datetime.now().strftime("%Y-%m-%d")

root_folder = desktop / "分类归档" / today

root_folder.mkdir(parents=True, exist_ok=True)

# ==========================
# 3. 文件分类规则
# ==========================

file_types = {

    ".doc": "Word",
    ".docx": "Word",

    ".xls": "Excel",
    ".xlsx": "Excel",

    ".ppt": "PPT",
    ".pptx": "PPT",

    ".pdf": "PDF",

    ".jpg": "Image",
    ".jpeg": "Image",
    ".png": "Image",
    ".bmp": "Image",
    ".gif": "Image",

    ".mp4": "Video",
    ".avi": "Video",
    ".mov": "Video",

    ".mp3": "Audio",
    ".wav": "Audio",

    ".zip": "Zip",
    ".rar": "Zip",
    ".7z": "Zip",

    ".txt": "Text",

}

# ==========================
# 4. 遍历桌面
# ==========================

for file in desktop.iterdir():

    # 只处理文件
    if not file.is_file():
        continue
    if file.suffix.lower() == ".lnk":
        continue

    suffix = file.suffix.lower()

    category = file_types.get(suffix, "Other")

    target_folder = root_folder / category

    target_folder.mkdir(exist_ok=True)

    copy2(file, target_folder / file.name)

print("文件分类完成！")
