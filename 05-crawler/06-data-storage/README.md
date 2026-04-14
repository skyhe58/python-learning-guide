# 爬虫数据存储

> **模块：** 05-crawler（爬虫）
> **难度：** 入门
> **前置知识：** Python 基础、文件操作、数据库操作
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

爬取到的数据需要持久化存储，常见的存储方式有三种：
1. **JSON 文件** — 适合结构化数据，便于后续处理
2. **CSV 文件** — 适合表格数据，可用 Excel 打开
3. **SQLite 数据库** — 适合大量数据，支持查询和去重

选择哪种存储方式取决于数据量、数据结构和后续使用场景。

## 存储方式对比

| 特性 | JSON | CSV | SQLite |
|------|------|-----|--------|
| 数据结构 | 嵌套/复杂 | 扁平/表格 | 关系型 |
| 数据量 | 小~中 | 中 | 中~大 |
| 查询能力 | 弱 | 弱 | 强（SQL） |
| 去重 | 需手动 | 需手动 | UNIQUE 约束 |
| 可读性 | 好 | 好（Excel） | 需工具 |
| 追加写入 | 不便 | 方便 | 方便 |

## 实战代码

### 示例：数据存储演示

**文件：** `examples/storage_demo.py`

演示内容：
- JSON 文件存储与读取
- CSV 文件存储与读取
- SQLite 数据库存储与查询

**运行方式：**
```bash
python examples/storage_demo.py
```

**预期输出：**
```
=== 爬虫数据存储演示 ===
[JSON] 已保存 5 条数据
[CSV] 已保存 5 条数据
[SQLite] 已保存 5 条数据，查询验证通过
```

## 常见陷阱

- ⚠️ JSON 追加写入不方便，需要读取全部 → 追加 → 重写
- ⚠️ CSV 写入中文时注意编码（`encoding='utf-8-sig'` 兼容 Excel）
- ⚠️ SQLite 并发写入需要注意锁机制
- ⚠️ 大量数据建议用数据库而非文件存储

> 💻 **完整可运行代码：** [storage_demo.py](examples/storage_demo.py)

## 参考资料

- [Python json 模块](https://docs.python.org/3/library/json.html)
- [Python csv 模块](https://docs.python.org/3/library/csv.html)
- [Python sqlite3 模块](https://docs.python.org/3/library/sqlite3.html)
