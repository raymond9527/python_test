# 这是为文件批量重命名的python插件
# ! 需要提前下载这几个库   pip install hachoir Pillow PyPDF2
from datetime import datetime  # 处理日期和时间
from PyPDF2 import PdfReader   # 专门解析PDF文件
from PIL.ExifTags import TAGS  # 获取图片EXIF数据中的创建日期
from PIL import Image
from hachoir.metadata import extractMetadata   # 解析视频和音频的元数据
from hachoir.parser import createParser
import os   # 获取文件信息
import shutil  # 复制文件


def get_video_creation_date(filepath):
    """使用hachoir获取视频/音频的拍摄日期"""
    try:
        parser = createParser(filepath)
        if not parser:
            print(f"无法解析文件: {filepath}")
            return None

        with parser:
            metadata = extractMetadata(parser)
            if metadata:
                creation_date = metadata.get('creation_date')
                if creation_date:
                    return creation_date.strftime("%Y-%m-%d")
    except Exception as e:
        print(f"获取视频/音频拍摄日期失败: {e}")
    return None


def get_image_creation_date(filepath):
    """使用Pillow获取图片的拍摄日期"""
    try:
        image = Image.open(filepath)
        exif_data = image._getexif()  # 获取EXIF数据，字典形式
        if exif_data:
            for tag, value in exif_data.items():
                if TAGS.get(tag) == 'DateTimeOriginal':
                    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S").strftime("%Y-%m-%d")
    except Exception as e:
        print(f"获取图片拍摄日期失败: {e}")
    return None


def get_pdf_creation_date(filepath):
    """使用PyPDF2的PdfReader获取PDF的创建日期"""
    try:
        with open(filepath, 'rb') as f:
            reader = PdfReader(f)
            info = reader.metadata
            creation_date = info.get('/CreationDate')
            if creation_date:
                return datetime.strptime(creation_date[2:10], "%Y%m%d").strftime("%Y-%m-%d")
    except Exception as e:
        print(f"获取PDF创建日期失败: {e}")
    return None


def get_file_creation_date(filepath):
    """获取CSV、Excel和Word文件的创建日期"""
    try:
        creation_time = os.path.getctime(filepath)
        return datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d")
    except Exception as e:
        print(f"获取文件创建日期失败: {e}")
    return None


def rename_files(folder_path):
    """遍历文件夹中的多种类型文件并重命名"""
    supported_extensions = {
        'video': ['.mp4', '.mov', '.avi', '.mkv', '.flv'],
        'image': ['.jpg', '.jpeg', '.png', '.heic'],
        'audio': ['.mp3', '.wav', '.flac'],
        'pdf': ['.pdf'],
        'csv': ['.csv'],
        'excel': ['.xls', '.xlsx'],
        'word': ['.doc', '.docx']
    }
    # 每个类型下支持的拓展名
    existing_names = {}
    # 记录每个日期下的文件数量，确保不会重复的文件名

    # ! 新增：输出目录（自动创建）
    output_folder = os.path.join(
        folder_path, "renamed_output")  # 在目标文件夹下新建一个子文件夹
    os.makedirs(output_folder, exist_ok=True)

    # 遍历所有文件，获取每个文件的完整路径和文件扩展名
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        file_ext = os.path.splitext(filename)[1].lower()

        if os.path.isfile(filepath):
            creation_date = None

            # 根据文件扩展名判断文件类型
            if file_ext in supported_extensions['video'] or file_ext in supported_extensions['audio']:
                creation_date = get_video_creation_date(filepath)
            elif file_ext in supported_extensions['image']:
                creation_date = get_image_creation_date(filepath)
            elif file_ext in supported_extensions['pdf']:
                creation_date = get_pdf_creation_date(filepath)
            elif file_ext in supported_extensions['csv'] or file_ext in supported_extensions['excel'] or file_ext in supported_extensions['word']:
                creation_date = get_file_creation_date(filepath)

            # 如果拍摄日期没有找到，使用文件的创建日期
            if not creation_date:
                creation_date = get_file_creation_date(filepath)

            # 如果找到了创建日期，就进行重命名
            if creation_date:
                if creation_date not in existing_names:
                    existing_names[creation_date] = 1
                else:
                    existing_names[creation_date] += 1

                new_filename = f"{creation_date}_{existing_names[creation_date]}{file_ext}"
                #! new_filepath = os.path.join(folder_path, new_filename)
                new_filepath = os.path.join(output_folder, new_filename)

                #! 原先的直接重命名，现在修改为复制并重命名
                # os.rename(filepath, new_filepath)
                shutil.copy2(filepath, new_filepath)
                print(f"已复制并重命名 {filename} 为 {new_filename}")


if __name__ == "__main__":
    rename_files("./Bulk_Rename_test")  # 设置目标文件夹
