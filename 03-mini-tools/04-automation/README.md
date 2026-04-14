# 自动化脚本

> **模块：** 03-小工具开发
> **难度：** 进阶
> **前置知识：** Python 基础（01-python-basics）、文件操作（08-file-operations）、模块与包（06-modules-packages）
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 功能描述

本目录包含两个实用的自动化脚本示例：

| 脚本 | 功能 | 依赖 |
|------|------|------|
| `file_organizer.py` | 按扩展名自动分类文件到子目录 | 标准库 |
| `system_info.py` | 收集系统信息（OS、CPU、内存、磁盘、Python 版本） | 标准库 |

两个脚本均使用 Python 标准库，无需安装第三方依赖。

## 使用方法

### 文件整理工具

```bash
# 整理当前目录下的文件
python examples/file_organizer.py /path/to/messy/folder

# 预览模式（不实际移动文件）
python examples/file_organizer.py /path/to/folder --dry-run

# 自定义分类规则文件
python examples/file_organizer.py /path/to/folder --rules custom_rules.json

# 撤销上次整理操作
python examples/file_organizer.py /path/to/folder --undo
```

### 系统信息收集

```bash
# 打印系统信息到终端
python examples/system_info.py

# 保存到文件
python examples/system_info.py --output system_report.txt

# 输出 JSON 格式
python examples/system_info.py --format json
```

## 参数说明

### file_organizer.py

| 参数 | 说明 | 必填 |
|------|------|------|
| `directory` | 要整理的目录路径 | 是 |
| `--dry-run` | 预览模式，不实际移动文件 | 否 |
| `--rules` | 自定义分类规则 JSON 文件 | 否 |
| `--undo` | 撤销上次整理操作 | 否 |

### system_info.py

| 参数 | 说明 | 必填 |
|------|------|------|
| `--output` | 输出文件路径 | 否 |
| `--format` | 输出格式：`text`（默认）或 `json` | 否 |

## 运行示例

```bash
# 文件整理预览
$ python examples/file_organizer.py ~/Downloads --dry-run
扫描目录: /Users/you/Downloads
发现 15 个文件

分类计划:
  图片 (4 个): photo1.jpg, photo2.png, screenshot.png, icon.svg
  文档 (3 个): report.pdf, notes.docx, data.xlsx
  代码 (2 个): script.py, app.js
  压缩包 (2 个): archive.zip, backup.tar.gz
  其他 (4 个): readme, config, .DS_Store, thumbs.db

预览完成，使用不带 --dry-run 参数执行实际整理。

# 系统信息
$ python examples/system_info.py
========== 系统信息报告 ==========
操作系统: macOS 14.0 (Darwin)
主机名: my-macbook
Python 版本: 3.12.0
CPU: Apple M1, 8 核
内存: 16.0 GB（已用 8.2 GB, 51.3%）
磁盘 /: 500.0 GB（已用 250.0 GB, 50.0%）
```

## Java 对比

| 特性 | Java | Python |
|------|------|--------|
| 文件移动 | `Files.move()` | `shutil.move()` / `Path.rename()` |
| 系统信息 | `System.getProperty()` / `Runtime` | `platform` / `os` / `shutil` |
| JSON 处理 | Jackson / Gson | `json` 标准库 |
| 进程信息 | `ProcessHandle` / `ManagementFactory` | `os` / `platform` |

> 💻 **完整可运行代码：** [file_organizer.py](examples/file_organizer.py) | [system_info.py](examples/system_info.py)

## 参考资料

- [Python 官方文档 - shutil](https://docs.python.org/zh-cn/3/library/shutil.html)
- [Python 官方文档 - platform](https://docs.python.org/zh-cn/3/library/platform.html)
- [Python 官方文档 - os](https://docs.python.org/zh-cn/3/library/os.html)
