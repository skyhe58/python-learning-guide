# Scrapy 框架入门

> **模块：** 05-crawler（爬虫）
> **难度：** 进阶
> **前置知识：** HTTP 基础、HTML 解析
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

Scrapy 是 Python 最强大的爬虫框架，提供了完整的爬虫开发解决方案。它采用异步架构，内置请求调度、数据管道、中间件等组件，适合构建大规模爬虫项目。

对于简单的爬取任务，`requests + BeautifulSoup` 足够；但当需要处理大量页面、管理请求队列、持久化数据时，Scrapy 是更好的选择。

## 架构概览

```
Scrapy 架构（数据流向）:

  ┌─────────┐     ┌────────────┐     ┌──────────┐
  │  Spider  │────>│   Engine   │────>│Downloader│
  │ (定义爬取│<────│  (调度中心) │<────│ (下载器)  │
  │  逻辑)   │     └─────┬──────┘     └──────────┘
  └─────────┘           │
                        ▼
              ┌──────────────────┐
              │  Item Pipeline   │
              │ (数据清洗/存储)   │
              └──────────────────┘
```

### 核心组件

| 组件 | 职责 | 类比 |
|------|------|------|
| Spider | 定义爬取逻辑和数据提取规则 | Controller |
| Item | 定义数据结构 | Model / DTO |
| Pipeline | 数据清洗、验证、存储 | Service / Repository |
| Middleware | 请求/响应的中间处理 | Filter / Interceptor |
| Engine | 协调各组件工作 | Spring IoC Container |
| Scheduler | 管理请求队列和去重 | 任务调度器 |

## 实战代码

### 示例：Scrapy 概念演示

**文件：** `examples/scrapy_intro.py`

演示内容：
- Spider / Item / Pipeline 的代码结构（概念演示）
- 不需要创建完整 Scrapy 项目即可理解核心概念

**运行方式：**
```bash
pip install scrapy
python examples/scrapy_intro.py
```

## Scrapy 项目创建流程

```bash
# 1. 创建项目
scrapy startproject myspider

# 2. 创建 Spider
cd myspider
scrapy genspider example example.com

# 3. 运行爬虫
scrapy crawl example

# 4. 导出数据
scrapy crawl example -o output.json
```

## 常见陷阱

- ⚠️ Scrapy 是异步框架，不要在 Spider 中使用 `requests` 库
- ⚠️ `yield` 是 Scrapy 的核心，Spider 通过 yield 返回 Request 和 Item
- ⚠️ Pipeline 的 `process_item` 必须返回 item 或抛出 `DropItem`
- ⚠️ 注意 `ROBOTSTXT_OBEY` 设置，默认遵守 robots.txt

> 💻 **完整可运行代码：** [scrapy_intro.py](examples/scrapy_intro.py)

## 参考资料

- [Scrapy 官方文档](https://docs.scrapy.org/en/latest/)
- [Scrapy 中文教程](https://scrapy-chs.readthedocs.io/)
