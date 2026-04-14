# HTML 解析（BeautifulSoup）

> **模块：** 05-crawler（爬虫）
> **难度：** 入门
> **前置知识：** HTTP 基础与 requests
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

HTML 解析是爬虫的核心环节。获取到网页 HTML 后，需要从中提取有用的数据（标题、链接、表格等）。BeautifulSoup 是 Python 最流行的 HTML 解析库，提供了直观的 API 来遍历和搜索 HTML 文档树。

BeautifulSoup 支持多种解析器：`html.parser`（内置）、`lxml`（速度快）、`html5lib`（容错强）。对于大多数场景，内置的 `html.parser` 已经足够。

## Java 对比

| 特性 | Java | Python |
|------|------|--------|
| HTML 解析 | Jsoup | BeautifulSoup |
| CSS 选择器 | Jsoup select() | soup.select() |
| XPath | javax.xml.xpath | lxml.etree |
| DOM 遍历 | Node.getChildNodes() | tag.children |

**Java 写法（Jsoup）：**
```java
Document doc = Jsoup.parse(html);
Elements links = doc.select("a[href]");
for (Element link : links) {
    System.out.println(link.attr("href") + " -> " + link.text());
}
```

**Python 写法（BeautifulSoup）：**
```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, "html.parser")
for link in soup.select("a[href]"):
    print(f"{link['href']} -> {link.text}")
```

## 核心知识点

### 1. 查找元素的方法

| 方法 | 说明 | 示例 |
|------|------|------|
| `find()` | 查找第一个匹配元素 | `soup.find("h1")` |
| `find_all()` | 查找所有匹配元素 | `soup.find_all("a")` |
| `select()` | CSS 选择器查找 | `soup.select("div.content p")` |
| `select_one()` | CSS 选择器查找第一个 | `soup.select_one("#title")` |

### 2. 常用 CSS 选择器

| 选择器 | 含义 | 示例 |
|--------|------|------|
| `tag` | 标签名 | `soup.select("p")` |
| `.class` | 类名 | `soup.select(".article")` |
| `#id` | ID | `soup.select("#header")` |
| `tag[attr]` | 属性存在 | `soup.select("a[href]")` |
| `parent > child` | 直接子元素 | `soup.select("ul > li")` |
| `tag:nth-child(n)` | 第 n 个子元素 | `soup.select("li:nth-child(2)")` |

### 3. 提取数据

```python
tag.text          # 获取文本内容
tag.string        # 获取直接文本（无子标签时）
tag.get_text(strip=True)  # 去除空白的文本
tag["href"]       # 获取属性值
tag.get("class")  # 安全获取属性（不存在返回 None）
tag.attrs         # 获取所有属性字典
```

## 实战代码

### 示例：BeautifulSoup 解析演示

**文件：** `examples/bs4_demo.py`

演示内容：
- 使用内嵌 HTML 字符串（不依赖外部网站）
- find/find_all 查找元素
- CSS 选择器
- 表格数据提取
- 嵌套结构遍历

**运行方式：**
```bash
pip install beautifulsoup4
python examples/bs4_demo.py
```

**预期输出：**
```
=== BeautifulSoup HTML 解析演示 ===
[标签查找] 标题: Python 爬虫学习
[CSS 选择器] 找到 3 个链接
[表格提取] 提取到 3 行数据
[嵌套遍历] 文章列表提取完成
```

## 常见陷阱

- ⚠️ `tag.string` 在标签有子标签时返回 `None`，用 `tag.get_text()` 更安全
- ⚠️ `find()` 找不到元素返回 `None`，直接取属性会报 `AttributeError`
- ⚠️ 不同解析器对不规范 HTML 的处理结果可能不同
- ⚠️ `select()` 返回列表，`select_one()` 返回单个元素或 `None`

> 💻 **完整可运行代码：** [bs4_demo.py](examples/bs4_demo.py)

## 参考资料

- [BeautifulSoup 官方文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/)
- [CSS 选择器参考](https://developer.mozilla.org/zh-CN/docs/Web/CSS/CSS_Selectors)
