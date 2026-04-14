@echo off
REM ============================================================
REM Python 学习知识库 — 一键环境搭建脚本（Windows）
REM ============================================================
REM 功能：
REM   1. 检查 Python 版本（要求 >= 3.9）
REM   2. 创建虚拟环境
REM   3. 安装项目依赖
REM 用法：
REM   setup_env.bat
REM ============================================================

echo ============================================
echo   Python 学习知识库 — 环境搭建
echo ============================================
echo.

REM ----- 步骤 1：检查 Python 版本 -----
echo [1/3] 检查 Python 版本...

where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo 错误：未找到 Python。请先安装 Python 3.9 或更高版本。
    echo   下载地址：https://www.python.org/downloads/
    echo   安装时请勾选 "Add Python to PATH"
    exit /b 1
)

REM 获取 Python 版本并检查
for /f "tokens=*" %%i in ('python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"') do set PYTHON_VERSION=%%i
for /f "tokens=*" %%i in ('python -c "import sys; print(sys.version_info.major)"') do set PYTHON_MAJOR=%%i
for /f "tokens=*" %%i in ('python -c "import sys; print(sys.version_info.minor)"') do set PYTHON_MINOR=%%i

echo   找到 Python 版本: %PYTHON_VERSION%

if %PYTHON_MAJOR% lss 3 (
    echo 错误：Python 版本过低（当前 %PYTHON_VERSION%，要求 ^>= 3.9）
    echo   请升级 Python：https://www.python.org/downloads/
    exit /b 1
)
if %PYTHON_MAJOR% equ 3 if %PYTHON_MINOR% lss 9 (
    echo 错误：Python 版本过低（当前 %PYTHON_VERSION%，要求 ^>= 3.9）
    echo   请升级 Python：https://www.python.org/downloads/
    exit /b 1
)

echo   √ Python 版本满足要求（%PYTHON_VERSION% ^>= 3.9）
echo.

REM ----- 步骤 2：创建虚拟环境 -----
echo [2/3] 创建虚拟环境...

if exist venv (
    echo   虚拟环境已存在，跳过创建。
    echo   如需重建，请先删除 venv 目录后重新运行本脚本。
) else (
    python -m venv venv
    echo   √ 虚拟环境创建成功（venv\）
)

REM 激活虚拟环境
call venv\Scripts\activate.bat
echo   √ 虚拟环境已激活
echo.

REM ----- 步骤 3：安装依赖 -----
echo [3/3] 安装项目依赖...

pip install --upgrade pip -q

if exist requirements.txt (
    pip install -r requirements.txt -q
    echo   √ 项目依赖安装完成
) else (
    echo   错误：未找到 requirements.txt
    exit /b 1
)

echo.
echo ============================================
echo   环境搭建完成！
echo ============================================
echo.
echo 后续使用时，请先激活虚拟环境：
echo   venv\Scripts\activate
echo.
echo 开始学习吧！建议从 01-python-basics 模块开始。
