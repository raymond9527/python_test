from __future__ import annotations

import os
import time
from pathlib import Path
from dataclasses import dataclass
from collections import Counter
from datetime import datetime


# ===============================
# 配置区域
# ===============================

SCAN_PATH = Path("C:/")

# 单文件超过 1GB 记录
FILE_THRESHOLD = 1 * 1024 ** 3

# 文件夹超过 5GB 记录
DIR_THRESHOLD = 5 * 1024 ** 3


# 输出数量
TOP_NUMBER = 50

REPORT_FILE = "C盘分析报告.txt"


# ===============================
# 数据结构
# ===============================

@dataclass(slots=True)
class FileInfo:
    path: Path
    size: int


@dataclass(slots=True)
class DirInfo:
    path: Path
    size: int


# ===============================
# 工具函数
# ===============================

def format_size(size: int) -> str:
    """
    字节转换为可读格式
    """

    units = [
        "B",
        "KB",
        "MB",
        "GB",
        "TB"
    ]

    value = float(size)

    for unit in units:
        if value < 1024:
            return f"{value:.2f} {unit}"

        value /= 1024

    return f"{value:.2f} PB"


# ===============================
# 扫描文件
# ===============================

def scan_files(root: Path):
    """
    扫描所有文件
    """

    print("开始扫描文件...")

    large_files = []

    extension_counter = Counter()

    total_files = 0

    for current, dirs, files in os.walk(root):

        current_path = Path(current)

        for filename in files:

            file_path = current_path / filename

            try:

                size = file_path.stat().st_size

                total_files += 1

                # 文件类型统计
                suffix = file_path.suffix.lower()

                if suffix:
                    extension_counter[suffix] += size
                else:
                    extension_counter["无扩展名"] += size

                # 大文件
                if size >= FILE_THRESHOLD:

                    large_files.append(
                        FileInfo(
                            file_path,
                            size
                        )
                    )

            except PermissionError:

                print(
                    f"无权限访问: {file_path}"
                )

            except FileNotFoundError:

                pass

            except OSError:

                pass

        if total_files % 10000 == 0:

            print(
                f"已扫描文件: {total_files}"
            )

    return (
        large_files,
        extension_counter,
        total_files
    )


# ===============================
# 扫描文件夹大小
# ===============================

def scan_directories(root: Path):
    """
    计算所有文件夹大小
    """

    print("\n开始计算文件夹大小...")

    folder_sizes = {}

    for current, dirs, files in os.walk(root):

        current_path = Path(current)

        total_size = 0

        for filename in files:

            file_path = current_path / filename

            try:

                total_size += file_path.stat().st_size

            except (
                PermissionError,
                FileNotFoundError,
                OSError
            ):

                pass

        folder_sizes[current_path] = total_size

    # 计算父目录大小

    for folder in sorted(
        folder_sizes.keys(),
        key=lambda x: len(x.parts),
        reverse=True
    ):

        parent = folder.parent

        if parent in folder_sizes:

            folder_sizes[parent] += folder_sizes[folder]

    result = []

    for path, size in folder_sizes.items():

        if size >= DIR_THRESHOLD:

            result.append(
                DirInfo(
                    path,
                    size
                )
            )

    return result


# ===============================
# 生成报告
# ===============================

def generate_report(
        files,
        folders,
        extensions,
        total_files,
        elapsed
):

    print("\n生成报告...")

    files.sort(
        key=lambda x: x.size,
        reverse=True
    )

    folders.sort(
        key=lambda x: x.size,
        reverse=True
    )

    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "C盘空间分析报告\n"
        )

        f.write(
            "="*50+"\n\n"
        )

        f.write(
            f"扫描时间:"
            f"{datetime.now()}\n"
        )

        f.write(
            f"扫描文件数量:"
            f"{total_files}\n"
        )

        f.write(
            f"耗时:"
            f"{elapsed:.2f} 秒\n\n"
        )

        # 大文件

        f.write(
            "\n一、最大文件 TOP50\n"
        )

        f.write(
            "-"*50+"\n"
        )

        for index, item in enumerate(
            files[:TOP_NUMBER],
            1
        ):

            f.write(
                f"{index}. "
                f"{format_size(item.size)}\n"
            )

            f.write(
                f"{item.path}\n\n"
            )

        # 文件夹

        f.write(
            "\n二、最大文件夹 TOP50\n"
        )

        f.write(
            "-"*50+"\n"
        )

        for index, item in enumerate(
            folders[:TOP_NUMBER],
            1
        ):

            f.write(
                f"{index}. "
                f"{format_size(item.size)}\n"
            )

            f.write(
                f"{item.path}\n\n"
            )

        # 类型统计

        f.write(
            "\n三、文件类型占用 TOP30\n"
        )

        f.write(
            "-"*50+"\n"
        )

        for suffix, size in extensions.most_common(30):

            f.write(
                f"{suffix}: "
                f"{format_size(size)}\n"
            )

    print(
        f"\n报告生成完成:"
        f"{REPORT_FILE}"
    )


# ===============================
# 主程序
# ===============================

def main():

    start = time.time()

    print(
        "C盘空间分析工具启动"
    )

    print(
        f"扫描目录:{SCAN_PATH}"
    )

    files, extensions, total = scan_files(
        SCAN_PATH
    )

    folders = scan_directories(
        SCAN_PATH
    )

    elapsed = time.time()-start

    generate_report(
        files,
        folders,
        extensions,
        total,
        elapsed
    )


if __name__ == "__main__":

    main()
