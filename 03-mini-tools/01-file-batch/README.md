# 文件批量处理工具

> **模块：** 03-小工具开发
> **难度：** 入门
> **前置知识：** Python 基础（01-python-basics）、文件操作（08-file-operations）
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 功能描述

`batch_rename.py` 是一个文件批量重命名命令行工具，支持以下四种重命名模式：

| 模式 | 说明 | 示例 |
|------|------|------|
| `prefix` | 添加前缀 | `file.txt` → `new_file.txt` |
| `suffix` | 添加后缀（文件名部分） | `file.txt` → `file_v2.txt` |
| `replace` | 替换文件名中的字符串 | `old_name.txt` → `new_name.txt` |
| `sequence` | 按序号重命名 | `*.txt` → `001.txt`, `002.txt`, ... |

所有模式均支持 `--dry-run` 预览，不实际修改文件。

## 使用方法

```bash
# 添加前缀
python batch_rename.py /path/to/dir --mode prefix --prefix "2025_"

# 添加后缀
python batch_rename.py /path/to/dir --mode suffix --suffix "_backup"

# 替换字符串
python batch_rename.py /path/to/dir --mode replace --old "旧文本" --new "新文本"

# 序号重命名
python batch_rename.py /path/to/dir --mode sequence --start 1 --digits 3

# 预览模式（不实际重命名）
python batch_rename.py /path/to/dir --mode prefix --prefix "new_" --dry-run

# 按扩展名过滤
python batch_rename.py /path/to/dir --mode prefix --prefix "img_" --ext .jpg
```

## 参数说明

| 参数 | 说明 | 必填 |
|------|------|------|
| `directory` | 目标目录路径 | 是 |
| `--mode` | 重命名模式：`prefix`/`suffix`/`replace`/`sequence` | 是 |
| `--prefix` | 要添加的前缀字符串（prefix 模式） | 否 |
| `--suffix` | 要添加的后缀字符串（suffix 模式） | 否 |
| `--old` | 要替换的旧字符串（replace 模式） | 否 |
| `--new` | 替换后的新字符串（replace 模式） | 否 |
| `--start` | 序号起始值，默认 1（sequence 模式） | 否 |
| `--digits` | 序号位数，默认 3（sequence 模式） | 否 |
| `--ext` | 只处理指定扩展名的文件（如 `.txt`） | 否 |
| `--dry-run` | 预览模式，只显示将要执行的操作 | 否 |

## 运行示例

```bash
# 1. 先生成测试文件
python test_files/generate_test_files.py

# 2. 预览添加前缀效果
$ python batch_rename.py test_files --mode prefix --prefix "2025_" --dry-run
[预览] report_q1.txt -> 2025_report_q1.txt
[预览] report_q2.txt -> 2025_report_q2.txt
[预览] data.csv -> 2025_data.csv
共 3 个文件将被重命名

# 3. 实际执行
$ python batch_rename.py test_files --mode prefix --prefix "2025_"
[重命名] report_q1.txt -> 2025_report_q1.txt
[重命名] report_q2.txt -> 2025_report_q2.txt
[重命名] data.csv -> 2025_data.csv
完成！共重命名 3 个文件
```

## Java 对比

| 特性 | Java | Python |
|------|------|--------|
| 文件操作 | `java.nio.file.Files.move()` | `pathlib.Path.rename()` |
| 目录遍历 | `Files.list()` / `Files.walk()` | `Path.iterdir()` / `os.listdir()` |
| 命令行解析 | Apache Commons CLI / picocli | `argparse`（标准库） |
| 路径处理 | `java.nio.file.Path` | `pathlib.Path` |

> 💻 **完整可运行代码：** [batch_rename.py](batch_rename.py)

## 参考资料

- [Python 官方文档 - argparse](https://docs.python.org/zh-cn/3/library/argparse.html)
- [Python 官方文档 - pathlib](https://docs.python.org/zh-cn/3/library/pathlib.html)
- [Python 官方文档 - os.rename](https://docs.python.org/zh-cn/3/library/os.html#os.rename)
