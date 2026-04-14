# PDF 操作工具

> **模块：** 03-小工具开发
> **难度：** 入门
> **前置知识：** Python 基础（01-python-basics）、文件操作（08-file-operations）
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 功能描述

`pdf_info.py` 是一个 PDF 信息查看命令行工具，支持以下功能：

| 功能 | 说明 |
|------|------|
| `info` | 查看 PDF 基本信息（页数、元数据、文件大小） |
| `pages` | 统计 PDF 页数 |
| `meta` | 读取 PDF 元数据（标题、作者、创建日期等） |

> **依赖说明：** 本工具使用 `PyPDF2` 库解析 PDF 文件。脚本会自动检查依赖是否安装，未安装时给出安装提示。

## 使用方法

```bash
# 安装依赖
pip install PyPDF2

# 查看 PDF 完整信息
python pdf_info.py info document.pdf

# 只查看页数
python pdf_info.py pages document.pdf

# 只查看元数据
python pdf_info.py meta document.pdf
```

## 参数说明

| 参数 | 说明 | 必填 |
|------|------|------|
| `command` | 子命令：`info`/`pages`/`meta` | 是 |
| `file` | PDF 文件路径 | 是 |

## 运行示例

```bash
# 1. 先生成测试 PDF（使用纯 Python 生成简单 PDF）
python sample_pdfs/generate_sample_pdf.py

# 2. 查看 PDF 信息
$ python pdf_info.py info sample_pdfs/sample.pdf
文件: sample_pdfs/sample.pdf
大小: 1.2 KB
页数: 2
元数据:
  标题: 示例 PDF 文档
  作者: Python 学习知识库
  创建工具: generate_sample_pdf.py

# 3. 如果未安装 PyPDF2
$ python pdf_info.py info sample.pdf
错误：需要安装 PyPDF2 库。请运行：
  pip install PyPDF2
```

## 生成测试 PDF

`sample_pdfs/generate_sample_pdf.py` 使用纯 Python 手动构建最小化的 PDF 文件，不依赖任何第三方库（如 reportlab）。生成的 PDF 可以用任何 PDF 阅读器打开。

## Java 对比

| 特性 | Java | Python |
|------|------|--------|
| PDF 读取 | Apache PDFBox | PyPDF2 / pdfplumber |
| PDF 生成 | iText / PDFBox | reportlab / fpdf2 |
| 依赖管理 | Maven/Gradle 自动下载 | `pip install` 手动安装 |
| 依赖检查 | 编译时检查 | 运行时 `try/except ImportError` |

> 💻 **完整可运行代码：** [pdf_info.py](pdf_info.py)

## 参考资料

- [PyPDF2 官方文档](https://pypdf2.readthedocs.io/)
- [Python 官方文档 - argparse](https://docs.python.org/zh-cn/3/library/argparse.html)
- [PDF 文件格式规范](https://www.adobe.com/devnet/pdf/pdf_reference.html)
