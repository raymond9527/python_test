@echo off
chcp 65001 >nul
echo ============================================
echo   文章分割工具 - PyInstaller 打包脚本
echo ============================================
echo.

REM 切换到脚本所在目录
cd /d "%~dp0"

echo [1/2] 清理旧的构建产物...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo [2/2] 开始打包...
python -m PyInstaller split_articles.spec --noconfirm

echo.
if exist "dist\文章分割工具.exe" (
    echo ============================================
    echo   打包成功！
    echo   生成文件: dist\文章分割工具.exe
    echo.
    echo   使用方法:
    echo     1. 将 文章分割工具.exe 复制到任意目录
    echo     2. 在 exe 同级新建 docx 文件夹
    echo     3. 将待分割的 .docx 放入 docx 文件夹
    echo     4. 双击 exe 运行，结果输出到 output 文件夹
    echo ============================================
) else (
    echo 打包失败，请检查上方错误信息。
)

echo.
pause
