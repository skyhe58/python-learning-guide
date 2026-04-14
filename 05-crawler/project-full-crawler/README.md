# 完整爬虫项目：文章采集系统

> **模块：** 05-crawler（爬虫）
> **难度：** 进阶
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## ⚖️ 爬虫法律与道德规范

**在开始任何爬虫项目之前，请务必了解并遵守以下规范：**

### 法律法规
- 遵守《中华人民共和国网络安全法》《数据安全法》《个人信息保护法》
- 不爬取个人隐私数据（姓名、手机号、身份证号等）
- 不绕过网站的技术保护措施（如验证码、登录墙）
- 不将爬取数据用于非法商业用途

### 道德规范
- **遵守 robots.txt**：始终检查并遵守目标网站的 robots.txt 协议
- **控制请求频率**：不对目标服务器造成过大压力
- **标明身份**：在 User-Agent 中标明爬虫身份
- **尊重版权**：爬取的内容仅用于学习和研究

### 最佳实践
```python
# 每次请求前检查 robots.txt
from urllib.robotparser import RobotFileParser
rp = RobotFileParser()
rp.set_url("https://example.com/robots.txt")
rp.read()
if rp.can_fetch("*", "/target-page"):
    # 允许爬取
    pass
```

---

## 项目说明

本项目演示一个完整的爬虫工作流程：**数据采集 → 数据清洗 → 数据存储**。

为了不依赖外部网站，项目使用**内嵌 HTML 模拟**作为数据源，完整展示爬虫的核心流程。

## 项目结构

```
project-full-crawler/
├── README.md          # 项目说明（含法律道德规范）
├── crawler.py         # 数据采集模块
├── cleaner.py         # 数据清洗模块
└── storage.py         # 数据存储模块
```

## 运行方式

```bash
# 安装依赖
pip install beautifulsoup4

# 运行完整流程（在 project-full-crawler 目录下）
python crawler.py
```

## 数据流程

```
内嵌 HTML 数据 → crawler.py（采集） → cleaner.py（清洗） → storage.py（存储）
                     ↓                      ↓                     ↓
               提取原始数据            去重/格式化           JSON + SQLite
```

## 预期输出

```
=== 文章采集系统 ===
[采集] 从 3 个页面提取到 9 篇文章
[清洗] 去重后剩余 8 篇，清洗完成
[存储] 已保存到 JSON 和 SQLite
[查询] 浏览量 Top 3 文章:
  1. 深度学习实战 (5200 views)
  2. Python 高级技巧 (3100 views)
  3. 爬虫框架对比 (2800 views)
```

> 💻 **完整可运行代码：** [crawler.py](crawler.py) | [cleaner.py](cleaner.py) | [storage.py](storage.py)
