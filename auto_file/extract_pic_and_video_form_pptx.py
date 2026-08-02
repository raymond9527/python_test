from pathlib import Path
import zipfile
import shutil
from datetime import datetime
import sys
from pptx import Presentation
import xml.etree.ElementTree as ET

# ======================
# 配置
# ======================

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR / "output"

VIDEO_EXTENSIONS = {
    ".mp4",
    ".avi",
    ".mov",
    ".wmv"
}

IMAGE_EXTENSIONS = {

    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".gif",
    ".tif",
    ".tiff",
    ".svg",
    ".emf",
    ".wmf"

}

# ======================
# 格式化文件大小
# ======================


def format_size(size):

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

            return (
                f"{value:.2f}"
                f" {unit}"
            )

        value /= 1024

    return f"{value:.2f} PB"


# ======================
# 获取图片页码关系
# ======================

def get_image_slide_mapping(
        ppt_file
):

    mapping = {}

    with zipfile.ZipFile(
            ppt_file,
            "r"
    ) as z:

        for file in z.namelist():

            # 查找每页关系文件
            if (
                file.startswith(
                    "ppt/slides/_rels/"
                )
                and
                file.endswith(
                    ".xml.rels"
                )
            ):

                slide_name = (
                    Path(file)
                    .name
                )

                try:

                    slide_number = int(
                        slide_name
                        .replace(
                            "slide",
                            ""
                        )
                        .replace(
                            ".xml.rels",
                            ""
                        )
                    )

                except ValueError:

                    continue

                data = z.read(
                    file
                )

                root = ET.fromstring(
                    data
                )

                for rel in root:

                    target = (
                        rel.attrib
                        .get(
                            "Target"
                        )
                    )

                    if not target:
                        continue

                    media = (
                        Path(target)
                        .name
                    )

                    ext = (
                        Path(media)
                        .suffix
                        .lower()
                    )

                    if ext in IMAGE_EXTENSIONS:

                        mapping[
                            media
                        ] = slide_number

    return mapping

# ======================
# 提取图片
# ======================


def extract_images(
        ppt_file,
        output_dir
):

    image_dir = (
        output_dir /
        "images"
    )

    image_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # 获取图片对应页码
    mapping = (
        get_image_slide_mapping(
            ppt_file
        )
    )

    count = 0

    with zipfile.ZipFile(
            ppt_file,
            "r"
    ) as z:

        for file in z.namelist():

            if not file.startswith(
                    "ppt/media/"
            ):
                continue

            path = Path(file)

            ext = (
                path.suffix
                .lower()
            )

            if ext not in IMAGE_EXTENSIONS:
                continue

            media_name = (
                path.name
            )

            slide_no = (
                mapping
                .get(
                    media_name,
                    0
                )
            )

            count += 1

            filename = (

                f"slide_"
                f"{slide_no:03d}"
                f"_image_"
                f"{count:03d}"
                f"{ext}"

            )

            save_path = (
                image_dir /
                filename
            )

            with z.open(file) as source:

                with open(
                        save_path,
                        "wb"
                ) as target:

                    shutil.copyfileobj(
                        source,
                        target
                    )

    return count


# ======================
# 获取视频页码关系
# ======================


def get_video_slide_mapping(
        ppt_file
):

    mapping = {}

    with zipfile.ZipFile(
            ppt_file,
            "r"
    ) as z:

        files = z.namelist()

        for file in files:

            if (
                file.startswith(
                    "ppt/slides/_rels/"
                )
                and
                file.endswith(
                    ".rels"
                )
            ):

                slide_name = (
                    Path(file)
                    .name
                )

                slide_number = (
                    int(
                        slide_name
                        .replace(
                            "slide",
                            ""
                        )
                        .replace(
                            ".xml.rels",
                            ""
                        )

                    )
                )

                data = z.read(
                    file
                )

                root = ET.fromstring(
                    data
                )

                for rel in root:

                    target = (
                        rel.attrib
                        .get(
                            "Target"
                        )
                    )

                    if target:

                        media = (
                            Path(target)
                            .name
                        )

                        if media.startswith(
                            "media"
                        ):

                            mapping[
                                media
                            ] = slide_number

    return mapping


# ======================
# 提取视频
# ======================

def extract_videos(
        ppt_file,
        output_dir
):

    video_dir = (
        output_dir /
        "videos"
    )

    video_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    mapping = (
        get_video_slide_mapping(
            ppt_file
        )
    )

    count = 0

    with zipfile.ZipFile(
            ppt_file,
            "r"
    ) as z:

        for file in z.namelist():

            path = Path(file)

            if (

                "ppt/media/"
                in file

                and

                path.suffix.lower()
                in VIDEO_EXTENSIONS

            ):

                media_name = (
                    path.name
                )

                slide_no = (
                    mapping
                    .get(
                        media_name,
                        0
                    )
                )

                count += 1

                filename = (

                    f"slide_"
                    f"{slide_no:03d}"
                    f"_video_"
                    f"{count:03d}"
                    f"{path.suffix.lower()}"

                )

                save_path = (
                    video_dir /
                    filename
                )

                with z.open(file) as source:

                    with open(
                        save_path,
                        "wb"
                    ) as target:

                        shutil.copyfileobj(
                            source,
                            target
                        )

    return count


# ======================
# 单个PPT处理
# ======================

def process_ppt(
        ppt_file
):

    folder = (
        OUTPUT_DIR /
        ppt_file.stem
    )

    folder.mkdir(
        exist_ok=True
    )

    print(
        f"\n处理:"
        f"{ppt_file.name}"
    )

    prs = Presentation(
        ppt_file
    )

    slide_count = len(
        prs.slides
    )

    image_count = extract_images(
        ppt_file,
        folder
    )

    video_count = extract_videos(
        ppt_file,
        folder
    )

    generate_report(
        ppt_file,
        folder,
        slide_count,
        image_count,
        video_count
    )


# ======================
# 生成报告
# ======================

def generate_report(
        ppt_file,
        output_dir,
        slides,
        images,
        videos
):

    report = (
        output_dir /
        "extract_report.txt"
    )

    with open(
        report,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "PPT媒体提取报告\n"
        )

        f.write(
            "="*40+"\n\n"
        )

        f.write(
            f"文件:"
            f"{ppt_file.name}\n"
        )

        f.write(
            f"页数:"
            f"{slides}\n"
        )

        f.write(
            f"图片数量:"
            f"{images}\n"
        )

        f.write(
            f"视频数量:"
            f"{videos}\n"
        )

        f.write(
            f"完成时间:"
            f"{datetime.now()}\n"
        )


# ======================
# 主程序
# ======================

def main():

    OUTPUT_DIR.mkdir(
        exist_ok=True
    )

    ppt_files = list(
        BASE_DIR.glob(
            "*.pptx"
        )
    )

    if not ppt_files:

        print(
            "没有找到PPTX文件"
        )

        return

    print(
        f"发现{len(ppt_files)}个PPT"
    )

    for ppt in ppt_files:

        process_ppt(
            ppt
        )

    print(
        "\n全部完成"
    )


if __name__ == "__main__":

    main()
    input("\n按 Enter 键退出...")
