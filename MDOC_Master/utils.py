import shutil
from datetime import datetime
from pathlib import Path

# =====================================================
# 创建目录
# =====================================================

def create_directory(
        directory: Path
):
    """
    创建目录

    如果目录不存在则创建
    """

    directory.mkdir(
        parents=True,
        exist_ok=True
    )


# =====================================================
# 获取时间字符串
# =====================================================

def get_time_string():
    """
    返回当前时间

    格式:
        2026-08-04_12-30-20
    """

    return datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )


# =====================================================
# 文件备份
# =====================================================

def backup_file(
        file_path: Path,
        backup_dir: Path
):
    """
    备份原始Word文件

    参数:
        file_path:
            原文件

        backup_dir:
            备份目录

    返回:
        备份文件路径
    """

    if not file_path.exists():

        return None

    create_directory(
        backup_dir
    )

    backup_name = (
        file_path.stem
        +
        "_backup_"
        +
        get_time_string()
        +
        file_path.suffix
    )

    backup_path = (
        backup_dir /
        backup_name
    )

    shutil.copy2(
        file_path,
        backup_path
    )

    return backup_path


# =====================================================
# 获取Word文件
# =====================================================

def get_word_files(
        directory: Path
):
    """
    获取目录下所有docx文件
    """

    return list(
        directory.glob(
            "*.docx"
        )
    )


# =====================================================
# 文件大小格式化
# =====================================================

def format_file_size(
        size
):
    """
    文件大小转换

    byte:
        KB
        MB
        GB
    """

    units = [
        "B",
        "KB",
        "MB",
        "GB"
    ]

    value = float(size)

    for unit in units:

        if value < 1024:

            return (
                f"{value:.2f}"
                f"{unit}"
            )

        value /= 1024

    return (
        f"{value:.2f}TB"
    )


# =====================================================
# 日志输出
# =====================================================

def write_log(
        message,
        log_file=None
):
    """
    输出运行日志

    同时:
        1. 控制台输出
        2. 写入日志文件
    """

    text = (
        f"[{datetime.now()}]"
        f" {message}"
    )

    print(
        text
    )

    if log_file:

        with open(
                log_file,
                "a",
                encoding="utf-8"
        ) as f:

            f.write(
                text
                +
                "\n"
            )


# =====================================================
# 异常记录
# =====================================================

def log_exception(
        error,
        log_file
):
    """
    记录异常信息
    """

    write_log(
        f"ERROR: {error}",
        log_file
    )
