# 爬虫 速查卡片

## 核心概念

| 概念 | 说明 | 示例 |
|------|------|------|
| requests | HTTP 请求库 | `requests.get(url, timeout=10)` |
| BeautifulSoup | HTML 解析库 | `soup.select("div.class")` |
| Selenium | 浏览器自动化 | `driver.find_element(By.CSS_SELECTOR, "...")` |
| Playwright | 现代浏览器自动化 | `page.query_selector_all("...")` |
| Scrapy | 爬虫框架 | `scrapy crawl spider_name` |
| robots.txt | 爬虫协议 | `urllib.robotparser.RobotFileParser` |

## 常用语法

### requests 请求

```python
import requests

# GET 请求
resp = requests.get(url, params={"q": "python"}, timeout=10)
data = resp.json()

# POST 请求
resp = requests.post(url, json={"key": "value"}, timeout=10)

# Session 会话（自动维护 Cookie）
session = requests.Session()
session.headers.update({"User-Agent": "MyBot/1.0"})
resp = session.get(url)

# 超时与重试
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503])
session.mount("http://", HTTPAdapter(max_retries=retry))
```

### BeautifulSoup 解析

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")

# 查找元素
soup.find("h1")                    # 第一个 h1
soup.find_all("a", class_="link")  # 所有 class=link 的 a 标签
soup.select("div.content > p")     # CSS 选择器
soup.select_one("#title")          # ID 选择器

# 提取数据
tag.text                           # 文本内容
tag.get_text(strip=True)           # 去空白文本
tag["href"]                        # 属性值
tag.get("class", [])               # 安全获取属性
```

### 数据存储

```python
import json, csv, sqlite3

# JSON
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data_list, f, ensure_ascii=False, indent=2)

# CSV
with open("data.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "url"])
    writer.writeheader()
    writer.writerows(data_list)

# SQLite
conn = sqlite3.connect("data.db")
cursor = conn.cursor()
cursor.execute("INSERT INTO t (col) VALUES (?)", (value,))
conn.commit()
conn.close()
```

### 反爬应对

```python
import random, time

# User-Agent 轮换
UA_LIST = ["Mozilla/5.0 ...", "Mozilla/5.0 ..."]
headers = {"User-Agent": random.choice(UA_LIST)}

# 请求频率控制
time.sleep(random.uniform(1, 3))

# 指数退避重试
for attempt in range(3):
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        break
    except requests.exceptions.RequestException:
        time.sleep(2 ** attempt)
```

## 常见陷阱

- ⚠️ 忘记设置 `timeout`，请求永久阻塞
- ⚠️ 不检查 `status_code`，直接解析响应
- ⚠️ `tag.string` 有子标签时返回 `None`，用 `tag.get_text()`
- ⚠️ CSV 中文乱码：用 `encoding='utf-8-sig'`
- ⚠️ 不控制请求频率，IP 被封
- ⚠️ 忽略异常处理，单个页面失败导致整个爬虫崩溃
- ⚠️ 不遵守 robots.txt，可能面临法律风险

## 面试高频考点

- requests vs urllib 的区别
- BeautifulSoup 的解析器选择（html.parser / lxml / html5lib）
- Scrapy 的架构和数据流
- 如何处理动态渲染页面（API 分析 vs 浏览器自动化）
- 反爬策略及应对方法
- 爬虫的法律和道德边界
- 分布式爬虫的设计思路
