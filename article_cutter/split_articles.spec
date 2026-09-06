# -*- mode: python ; coding: utf-8 -*-
"""
split_articles.spec

PyInstaller 打包配置文件

打包命令:
    pyinstaller split_articles.spec

生成结果:
    dist/文章分割工具.exe  （单文件可执行程序）

使用说明:
    将待分割的 .docx 文件放入 exe 同级的 docx/ 目录，
    双击 exe 运行，结果输出到 output/ 目录。
"""

from PyInstaller.utils.hooks import collect_data_files

# 收集 python-docx 的数据文件（关键：templates/default.docx）
# 否则打包后 Document() 无法加载默认模板
datas = collect_data_files("docx")

a = Analysis(
    ["split_articles.py"],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="文章分割工具",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
