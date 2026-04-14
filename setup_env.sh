#!/bin/bash
# ============================================================
# Python 学习知识库 — 一键环境搭建脚本（Linux/Mac）
# ============================================================
# 功能：
#   1. 检查 Python 版本（要求 >= 3.9）
#   2. 创建虚拟环境
#   3. 安装项目依赖
# 用法：
#   chmod +x setup_env.sh
#   ./setup_env.sh
# ============================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "============================================"
echo "  Python 学习知识库 — 环境搭建"
echo "============================================"
echo ""

# ----- 步骤 1：检查 Python 版本 -----
echo -e "${YELLOW}[1/3] 检查 Python 版本...${NC}"

# 尝试查找 Python 命令
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}错误：未找到 Python。请先安装 Python 3.9 或更高版本。${NC}"
    echo "  下载地址：https://www.python.org/downloads/"
    exit 1
fi

# 获取 Python 版本
PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PYTHON_MAJOR=$($PYTHON_CMD -c "import sys; print(sys.version_info.major)")
PYTHON_MINOR=$($PYTHON_CMD -c "import sys; print(sys.version_info.minor)")

echo "  找到 Python: $PYTHON_CMD (版本 $PYTHON_VERSION)"

# 检查版本是否满足要求
if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 9 ]); then
    echo -e "${RED}错误：Python 版本过低（当前 $PYTHON_VERSION，要求 >= 3.9）${NC}"
    echo "  请升级 Python：https://www.python.org/downloads/"
    exit 1
fi

echo -e "${GREEN}  ✓ Python 版本满足要求（$PYTHON_VERSION >= 3.9）${NC}"
echo ""

# ----- 步骤 2：创建虚拟环境 -----
echo -e "${YELLOW}[2/3] 创建虚拟环境...${NC}"

VENV_DIR="venv"

if [ -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}  虚拟环境已存在，跳过创建。${NC}"
    echo "  如需重建，请先删除 $VENV_DIR 目录后重新运行本脚本。"
else
    $PYTHON_CMD -m venv "$VENV_DIR"
    echo -e "${GREEN}  ✓ 虚拟环境创建成功（$VENV_DIR/）${NC}"
fi

# 激活虚拟环境
source "$VENV_DIR/bin/activate"
echo -e "${GREEN}  ✓ 虚拟环境已激活${NC}"
echo ""

# ----- 步骤 3：安装依赖 -----
echo -e "${YELLOW}[3/3] 安装项目依赖...${NC}"

# 升级 pip
pip install --upgrade pip -q

# 安装依赖
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt -q
    echo -e "${GREEN}  ✓ 项目依赖安装完成${NC}"
else
    echo -e "${RED}  错误：未找到 requirements.txt${NC}"
    exit 1
fi

echo ""
echo "============================================"
echo -e "${GREEN}  ✅ 环境搭建完成！${NC}"
echo "============================================"
echo ""
echo "后续使用时，请先激活虚拟环境："
echo "  source venv/bin/activate"
echo ""
echo "开始学习吧！建议从 01-python-basics 模块开始。"
