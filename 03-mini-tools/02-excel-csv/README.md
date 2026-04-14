# Excel/CSV 数据处理工具

> **模块：** 03-小工具开发
> **难度：** 入门
> **前置知识：** Python 基础（01-python-basics）、文件操作（08-file-operations）
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 功能描述

`excel_processor.py` 是一个基于 Python 标准库 `csv` 的 CSV 数据处理命令行工具，**无需安装任何第三方依赖**即可直接运行。支持以下功能：

| 功能 | 说明 |
|------|------|
| `info` | 查看 CSV 文件基本信息（行数、列数、列名、数据预览） |
| `filter` | 按条件筛选数据行 |
| `stats` | 对数值列进行统计汇总（求和、平均值、最大/最小值） |
| `convert` | CSV 格式转换（分隔符转换、编码转换） |

## 使用方法

```bash
# 查看 CSV 文件信息
python excel_processor.py info sample_data/sales.csv

# 按条件筛选（支持 ==, !=, >, <, >=, <= 运算符）
python excel_processor.py filter sample_data/sales.csv --column "金额" --op ">" --value "1000" --output filtered.csv

# 统计汇总
python excel_processor.py stats sample_data/sales.csv --column "金额"

# 转换分隔符（CSV → TSV）
python excel_processor.py convert sample_data/sales.csv --output result.tsv --delimiter "\t"
```

## 参数说明

### 通用参数

| 参数 | 说明 | 必填 |
|------|------|------|
| `command` | 子命令：`info`/`filter`/`stats`/`convert` | 是 |
| `file` | 输入 CSV 文件路径 | 是 |
| `--encoding` | 文件编码，默认 `utf-8` | 否 |

### filter 子命令参数

| 参数 | 说明 | 必填 |
|------|------|------|
| `--column` | 筛选的列名 | 是 |
| `--op` | 比较运算符：`==`, `!=`, `>`, `<`, `>=`, `<=`, `contains` | 是 |
| `--value` | 比较值 | 是 |
| `--output` | 输出文件路径 | 否 |

### stats 子命令参数

| 参数 | 说明 | 必填 |
|------|------|------|
| `--column` | 要统计的数值列名 | 是 |

### convert 子命令参数

| 参数 | 说明 | 必填 |
|------|------|------|
| `--output` | 输出文件路径 | 是 |
| `--delimiter` | 输出分隔符，默认 `,` | 否 |
| `--out-encoding` | 输出编码，默认 `utf-8` | 否 |

## 运行示例

```bash
# 1. 先生成示例数据
python sample_data/generate_sample.py

# 2. 查看文件信息
$ python excel_processor.py info sample_data/sales.csv
文件: sample_data/sales.csv
行数: 20（不含表头）
列数: 5
列名: 日期, 产品, 类别, 金额, 数量

前 5 行预览:
  日期        产品      类别    金额    数量
  2025-01-05  笔记本电脑  电子产品  5999   2
  2025-01-12  机械键盘    电子产品  399    5
  ...

# 3. 筛选金额大于 1000 的记录
$ python excel_processor.py filter sample_data/sales.csv --column "金额" --op ">" --value "1000"
筛选条件: 金额 > 1000
匹配 8 行（共 20 行）

# 4. 统计金额列
$ python excel_processor.py stats sample_data/sales.csv --column "金额"
列: 金额
  总数: 20
  求和: 45680.00
  平均值: 2284.00
  最大值: 5999.00
  最小值: 29.90
```

## 设计说明

本工具仅使用 Python 标准库 `csv` 模块，不依赖 pandas 或 openpyxl，确保在任何 Python 3.9+ 环境下都能直接运行。如果需要处理 `.xlsx` 格式的 Excel 文件，可以先用 Excel 或 LibreOffice 导出为 CSV。

## Java 对比

| 特性 | Java | Python |
|------|------|--------|
| CSV 解析 | Apache Commons CSV / OpenCSV | `csv` 标准库 |
| Excel 操作 | Apache POI | openpyxl / xlrd |
| 数据处理 | Stream API | 列表推导式 / csv.DictReader |
| 命令行解析 | picocli / Commons CLI | `argparse` 标准库 |

> 💻 **完整可运行代码：** [excel_processor.py](excel_processor.py)

## 参考资料

- [Python 官方文档 - csv 模块](https://docs.python.org/zh-cn/3/library/csv.html)
- [Python 官方文档 - argparse](https://docs.python.org/zh-cn/3/library/argparse.html)
