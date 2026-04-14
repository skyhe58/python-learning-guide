# Python 环境搭建指南

> **模块：** 01-Python 基础
> **难度：** 入门
> **前置知识：** 无
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

环境搭建是学习任何编程语言的第一步。对于 Java 开发者来说，你已经熟悉了 JDK 安装、Maven/Gradle 依赖管理、IDE 配置等流程。Python 的环境搭建思路类似，但在工具链和管理方式上有显著差异。

Python 环境搭建的核心包括四个部分：**Python 解释器安装**、**虚拟环境配置**、**包管理工具使用**和 **IDE 配置**。与 Java 不同，Python 没有编译步骤，代码直接由解释器执行；Python 的依赖管理更轻量，但也更容易出现版本冲突问题，因此虚拟环境的使用至关重要。

理解这些差异，能帮助你避免很多 Java 开发者初学 Python 时常犯的错误，比如在全局环境中安装所有包、忽略虚拟环境隔离等。

## Java 对比

| 特性 | Java | Python |
|------|------|--------|
| 运行时 | JDK（JRE + 编译器） | Python 解释器（CPython） |
| 版本管理 | 手动安装或 SDKMAN | pyenv / 官方安装包 |
| 项目隔离 | Maven/Gradle 项目级依赖 | venv / conda 虚拟环境 |
| 包管理工具 | Maven（pom.xml）/ Gradle（build.gradle） | pip（requirements.txt）/ Poetry（pyproject.toml） |
| 依赖文件 | `pom.xml` / `build.gradle` | `requirements.txt` / `pyproject.toml` |
| 包仓库 | Maven Central / JCenter | PyPI（Python Package Index） |
| IDE | IntelliJ IDEA / Eclipse | PyCharm / VS Code |
| 构建过程 | 编译 → 字节码 → JVM 执行 | 直接解释执行（无需显式编译） |
| 环境变量 | `JAVA_HOME` | 虚拟环境自动管理路径 |

**Java 写法：**
```java
// Java 项目初始化（Maven）
// 1. 安装 JDK
// 2. 配置 JAVA_HOME
// 3. 创建 pom.xml 声明依赖
// 4. mvn install 下载依赖
// 5. IDE 自动识别项目结构

// pom.xml 示例
// <dependency>
//     <groupId>com.google.code.gson</groupId>
//     <artifactId>gson</artifactId>
//     <version>2.10.1</version>
// </dependency>
```

**Python 写法：**
```python
# Python 项目初始化
# 1. 安装 Python
# 2. 创建虚拟环境: python -m venv .venv
# 3. 激活虚拟环境: source .venv/bin/activate (Linux/Mac)
# 4. 安装依赖: pip install requests
# 5. 导出依赖: pip freeze > requirements.txt

# requirements.txt 示例
# requests==2.31.0
# flask==3.0.0
```

## 1. Python 安装

### Windows

1. 访问 [Python 官网](https://www.python.org/downloads/) 下载最新版本（>= 3.9）
2. 运行安装程序，**务必勾选 "Add Python to PATH"**
3. 选择 "Customize installation"，确保勾选 pip、tcl/tk、py launcher
4. 验证安装：

```bash
python --version
# 输出示例: Python 3.12.4

pip --version
# 输出示例: pip 24.0 from ... (python 3.12)
```

### macOS

**方式一：官网安装包（推荐新手）**

1. 访问 [Python 官网](https://www.python.org/downloads/) 下载 macOS 安装包
2. 双击 `.pkg` 文件按提示安装

**方式二：Homebrew 安装（推荐开发者）**

```bash
# 安装 Homebrew（如果尚未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 Python
brew install python@3.12

# 验证
python3 --version
```

> ⚠️ macOS 自带的 Python 2.x 已过时，请使用 `python3` 命令调用新版本。

### Linux（Ubuntu/Debian）

```bash
# 更新包列表
sudo apt update

# 安装 Python 3 和 pip
sudo apt install python3 python3-pip python3-venv

# 验证
python3 --version
pip3 --version
```

### 使用 pyenv 管理多版本（进阶）

如果你需要在同一台机器上管理多个 Python 版本（类似 Java 的 SDKMAN），推荐使用 pyenv：

```bash
# 安装 pyenv（Linux/macOS）
curl https://pyenv.run | bash

# 安装指定版本
pyenv install 3.12.4

# 设置全局版本
pyenv global 3.12.4

# 设置项目级版本
pyenv local 3.11.9
```

## 2. 虚拟环境配置

### 为什么需要虚拟环境？

Java 开发者习惯了 Maven/Gradle 的项目级依赖管理——每个项目的 `pom.xml` 独立声明依赖，互不干扰。Python 默认将包安装到全局环境，如果不使用虚拟环境，不同项目的依赖版本会互相冲突。

**虚拟环境 = Python 版的项目级依赖隔离**，类似于每个项目有自己独立的 `node_modules`（Node.js）或独立的 Maven 本地仓库。

### venv（Python 内置，推荐）

```bash
# 创建虚拟环境（在项目根目录执行）
python -m venv .venv

# 激活虚拟环境
# Linux/macOS:
source .venv/bin/activate

# Windows CMD:
.venv\Scripts\activate.bat

# Windows PowerShell:
.venv\Scripts\Activate.ps1

# 激活后命令行前缀会显示 (.venv)
# (.venv) $ python --version

# 退出虚拟环境
deactivate
```

### conda（Anaconda/Miniconda）

conda 是另一个流行的环境管理工具，特别适合数据科学和 AI 项目，因为它能管理非 Python 依赖（如 CUDA、MKL 等）。

```bash
# 安装 Miniconda（推荐，比 Anaconda 更轻量）
# 从 https://docs.conda.io/en/latest/miniconda.html 下载

# 创建环境
conda create -n myproject python=3.12

# 激活环境
conda activate myproject

# 退出环境
conda deactivate

# 查看所有环境
conda env list

# 删除环境
conda env remove -n myproject
```

### venv vs conda 对比

| 特性 | venv | conda |
|------|------|-------|
| 安装方式 | Python 内置 | 需额外安装 |
| Python 版本管理 | 不支持（需配合 pyenv） | 支持 |
| 非 Python 依赖 | 不支持 | 支持（如 CUDA、MKL） |
| 包来源 | PyPI | conda-forge + PyPI |
| 适用场景 | 通用 Python 开发 | 数据科学 / AI 项目 |
| 磁盘占用 | 较小 | 较大 |
| 推荐度 | ⭐ 通用首选 | ⭐ AI/数据科学首选 |

## 3. pip 包管理

pip 是 Python 的标准包管理工具，类似于 Java 的 Maven/Gradle。

### 常用命令

```bash
# 安装包
pip install requests

# 安装指定版本
pip install requests==2.31.0

# 安装最低版本
pip install "requests>=2.28.0"

# 升级包
pip install --upgrade requests

# 卸载包
pip uninstall requests

# 查看已安装的包
pip list

# 查看包详情
pip show requests

# 搜索包（在 https://pypi.org 上搜索更方便）
```

### requirements.txt 依赖管理

```bash
# 导出当前环境所有依赖（类似 Maven 的 dependency:tree）
pip freeze > requirements.txt

# 从 requirements.txt 安装所有依赖（类似 mvn install）
pip install -r requirements.txt
```

**requirements.txt 示例：**

```text
# Web 框架
flask==3.0.0
requests==2.31.0

# 数据处理
pandas==2.1.0
numpy==1.26.0

# 测试
pytest==7.4.0
```

### pip vs Maven/Gradle 对比

| 操作 | Maven | pip |
|------|-------|-----|
| 安装依赖 | `mvn install` | `pip install -r requirements.txt` |
| 添加依赖 | 编辑 `pom.xml` | `pip install <包名>` |
| 导出依赖 | `mvn dependency:tree` | `pip freeze > requirements.txt` |
| 依赖文件 | `pom.xml` | `requirements.txt` |
| 仓库地址 | Maven Central | PyPI (pypi.org) |
| 镜像配置 | `settings.xml` | `pip config set global.index-url <url>` |

### 配置国内镜像（加速下载）

```bash
# 临时使用
pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple

# 永久配置（推荐）
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

常用国内镜像：
- 清华：`https://pypi.tuna.tsinghua.edu.cn/simple`
- 阿里云：`https://mirrors.aliyun.com/pypi/simple/`
- 中科大：`https://pypi.mirrors.ustc.edu.cn/simple/`

## 4. IDE 配置

### VS Code（推荐）

VS Code 轻量、免费、插件丰富，是 Python 开发的主流选择。

**必装插件：**

| 插件名 | 说明 |
|--------|------|
| Python (Microsoft) | Python 语言支持、IntelliSense、调试 |
| Pylance | 高性能类型检查和自动补全 |
| Python Debugger | 调试支持 |
| autoDocstring | 自动生成 docstring |
| Ruff | 代码格式化和 lint（替代 Black + Flake8） |

**配置建议（settings.json）：**

```json
{
    "python.defaultInterpreterPath": ".venv/bin/python",
    "python.analysis.typeCheckingMode": "basic",
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.fixAll": "explicit",
            "source.organizeImports": "explicit"
        }
    }
}
```

### PyCharm

PyCharm 是 JetBrains 出品的 Python IDE，如果你习惯了 IntelliJ IDEA，PyCharm 的操作方式会非常熟悉。

**配置步骤：**

1. 下载 [PyCharm Community Edition](https://www.jetbrains.com/pycharm/download/)（免费版足够日常使用）
2. 创建项目时选择 "New environment using Virtualenv"
3. 配置 Python 解释器：`Settings → Project → Python Interpreter`
4. 安装依赖：在 Terminal 中执行 `pip install -r requirements.txt`

**PyCharm vs IntelliJ IDEA 对比：**

| 功能 | IntelliJ IDEA (Java) | PyCharm (Python) |
|------|----------------------|------------------|
| 项目创建 | New Project → Maven/Gradle | New Project → Virtualenv |
| 依赖管理 | pom.xml 自动同步 | requirements.txt 手动安装 |
| 运行配置 | Run Configuration | Run Configuration（几乎一样） |
| 调试 | 断点调试 | 断点调试（操作一致） |
| 重构 | Refactor 菜单 | Refactor 菜单（快捷键相同） |

## 实战代码

### 示例 1：环境验证脚本

**文件：** `verify_env.py`

```python
"""环境验证脚本 — 检查 Python 环境是否正确配置"""

import sys
import importlib

def main():
    # 检查 Python 版本
    version = sys.version_info
    if version >= (3, 9):
        print(f"✓ Python 版本: {sys.version}")
    else:
        print(f"✗ Python 版本过低: {sys.version}（需要 >= 3.9）")

    # 检查 pip
    try:
        import pip
        print(f"✓ pip 可用: {pip.__version__}")
    except ImportError:
        print("✗ pip 不可用")

    # 检查标准库模块
    for mod in ["json", "os", "sys", "pathlib", "datetime", "re"]:
        try:
            importlib.import_module(mod)
            print(f"✓ {mod} 模块可用")
        except ImportError:
            print(f"✗ {mod} 模块不可用")

if __name__ == "__main__":
    main()
```

**运行方式：**
```bash
python verify_env.py
```

**预期输出：**
```
✓ Python 版本: 3.12.4 (main, Jun  6 2024, 18:26:44) [Clang 15.0.0 (clang-1500.3.9.4)]
✓ pip 可用: 24.0
✓ json 模块可用
✓ os 模块可用
✓ sys 模块可用
✓ pathlib 模块可用
✓ datetime 模块可用
✓ re 模块可用

环境检查完成: 8/8 项通过
```

## 常见陷阱

### 1. 忘记激活虚拟环境

Java 开发者习惯了 Maven 自动管理依赖，容易忘记在安装包之前激活虚拟环境，导致包被安装到全局环境。

```bash
# ✗ 错误：直接在全局安装
pip install flask

# ✓ 正确：先激活虚拟环境
source .venv/bin/activate
pip install flask
```

### 2. Windows 上 python 和 python3 混淆

在 Windows 上，Python 安装后通常使用 `python` 命令；在 Linux/macOS 上，可能需要使用 `python3`。建议统一在虚拟环境中使用 `python`。

### 3. PATH 环境变量未配置

安装 Python 时忘记勾选 "Add Python to PATH"，导致命令行找不到 `python` 命令。解决方法：重新运行安装程序，勾选该选项；或手动将 Python 安装路径添加到系统 PATH。

### 4. pip 安装速度慢

默认从 PyPI 官方源下载，国内网络可能很慢。解决方法：配置国内镜像源（见上文"配置国内镜像"章节）。

### 5. 不同项目依赖版本冲突

不使用虚拟环境时，项目 A 需要 `requests==2.28.0`，项目 B 需要 `requests==2.31.0`，会导致冲突。**每个项目都应该创建独立的虚拟环境。**

### 6. 混用 conda 和 pip

在 conda 环境中混用 `conda install` 和 `pip install` 可能导致依赖冲突。建议：优先使用 `conda install`，只有 conda 仓库中没有的包才用 `pip install`。

## 参考资料

> 💻 **完整可运行代码：** [verify_env.py](verify_env.py)

- [Python 官方文档 - 安装指南](https://docs.python.org/zh-cn/3/using/index.html)
- [Python 官方文档 - venv 模块](https://docs.python.org/zh-cn/3/library/venv.html)
- [pip 官方文档](https://pip.pypa.io/en/stable/)
- [conda 官方文档](https://docs.conda.io/en/latest/)
- [VS Code Python 扩展文档](https://code.visualstudio.com/docs/python/python-tutorial)
- [PyCharm 官方文档](https://www.jetbrains.com/help/pycharm/)
- [pyenv 项目主页](https://github.com/pyenv/pyenv)
