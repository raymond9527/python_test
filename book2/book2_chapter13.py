import time
import webbrowser
import urllib.parse
import pyperclip
import re
import sys
# ! 监测剪贴板，如果是常用的地址，那么就打开谷歌地图搜索这个地址
# todo 编写一个bat文件来自动执行这个


def is_address(text):
    """
    简单判断复制内容是否像地址
    """

    if not text:
        return False

    # 地址关键词
    keywords = [
        "路",
        "街",
        "号",
        "省",
        "市",
        "区",
        "县",
        "road",
        "street",
        "avenue"
    ]

    for word in keywords:
        if word.lower() in text.lower():
            return True

    # 英文地址数字较多
    if re.search(r"\d+", text):
        return True

    return False


def open_google_map(address):
    """
    打开Google地图搜索地址
    """

    encoded_address = urllib.parse.quote(
        address
    )

    url = (
        "https://www.google.com/maps/search/"
        + encoded_address
    )

    webbrowser.open_new_tab(url)


def monitor_clipboard():
    """
    实时监听剪贴板
    """

    print(
        "剪贴板监听启动..."
    )

    print(
        "复制地址后自动打开Google地图"
    )

    old_content = ""

    while True:

        try:

            new_content = pyperclip.paste()

            # 判断内容是否变化

            if new_content != old_content:

                old_content = new_content

                print(
                    "\n检测到新复制内容:"
                )

                print(
                    new_content
                )

                if is_address(new_content):

                    print(
                        "识别为地址，打开Google地图..."
                    )

                    open_google_map(
                        new_content
                    )

                else:

                    print(
                        "不是地址，忽略"
                    )

            time.sleep(1)

        except KeyboardInterrupt:

            print(
                "\n程序退出"
            )

            break


if __name__ == "__main__":
    monitor_clipboard()
