#!/usr/bin/env python3
"""
BeautifulSoup HTML 解析演示

模块: 05-crawler（爬虫）
知识点: HTML 解析
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    pip install beautifulsoup4
    python bs4_demo.py

描述:
    使用内嵌 HTML 字符串演示 BeautifulSoup 的各种解析技巧，
    包括标签查找、CSS 选择器、表格提取、嵌套遍历等。
    不依赖任何外部网站。
"""

from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# 内嵌 HTML 测试数据
# ---------------------------------------------------------------------------
SAMPLE_HTML = """
<!DOCTYPE html>
<html lang="zh">
<head><title>Python 爬虫学习</title></head>
<body>
    <h1 id="main-title">Python 爬虫学习指南</h1>
    <p class="intro">欢迎学习 Python 爬虫技术！</p>

    <nav>
        <a href="/basics" class="nav-link">基础入门</a>
        <a href="/advanced" class="nav-link">进阶技巧</a>
        <a href="/projects" class="nav-link active">实战项目</a>
    </nav>

    <div class="articles">
        <article class="post" data-id="1">
            <h2>requests 库入门</h2>
            <p class="summary">学习 HTTP 请求的基础知识</p>
            <span class="tag">入门</span>
            <span class="tag">HTTP</span>
        </article>
        <article class="post" data-id="2">
            <h2>BeautifulSoup 解析</h2>
            <p class="summary">掌握 HTML 文档解析技巧</p>
            <span class="tag">解析</span>
        </article>
        <article class="post" data-id="3">
            <h2>Scrapy 框架实战</h2>
            <p class="summary">使用 Scrapy 构建爬虫项目</p>
            <span class="tag">框架</span>
            <span class="tag">进阶</span>
        </article>
    </div>

    <table id="comparison">
        <thead>
            <tr><th>工具</th><th>用途</th><th>难度</th></tr>
        </thead>
        <tbody>
            <tr><td>requests</td><td>HTTP 请求</td><td>简单</td></tr>
            <tr><td>BeautifulSoup</td><td>HTML 解析</td><td>简单</td></tr>
            <tr><td>Scrapy</td><td>爬虫框架</td><td>中等</td></tr>
        </tbody>
    </table>
</body>
</html>
"""


def demo_basic_find():
    """演示基本的标签查找。"""
    print("--- 1. 基本标签查找 ---")
    soup = BeautifulSoup(SAMPLE_HTML, "html.parser")

    # find() — 查找第一个匹配元素
    title = soup.find("h1")
    print(f"页面标题: {title.text}")
    print(f"标题 ID: {title.get('id')}")

    # find_all() — 查找所有匹配元素
    all_h2 = soup.find_all("h2")
    print(f"所有 h2 标签 ({len(all_h2)} 个):")
    for h2 in all_h2:
        print(f"  - {h2.text}")

    # 按属性查找
    intro = soup.find("p", class_="intro")
    print(f"简介: {intro.text}")


def demo_css_selectors():
    """演示 CSS 选择器。"""
    print("\n--- 2. CSS 选择器 ---")
    soup = BeautifulSoup(SAMPLE_HTML, "html.parser")

    # 类选择器
    nav_links = soup.select("a.nav-link")
    print(f"导航链接 ({len(nav_links)} 个):")
    for link in nav_links:
        active = " [当前]" if "active" in link.get("class", []) else ""
        print(f"  {link['href']} -> {link.text}{active}")

    # ID 选择器
    main_title = soup.select_one("#main-title")
    print(f"主标题: {main_title.text}")

    # 层级选择器
    article_titles = soup.select("div.articles article h2")
    print(f"文章标题: {[t.text for t in article_titles]}")

    # 属性选择器
    active_link = soup.select_one("a.active")
    print(f"当前激活链接: {active_link.text if active_link else '无'}")


def demo_table_extraction():
    """演示表格数据提取。"""
    print("\n--- 3. 表格数据提取 ---")
    soup = BeautifulSoup(SAMPLE_HTML, "html.parser")

    table = soup.select_one("#comparison")
    # 提取表头
    headers = [th.text for th in table.select("thead th")]
    print(f"表头: {headers}")

    # 提取数据行
    rows = []
    for tr in table.select("tbody tr"):
        row = [td.text for td in tr.select("td")]
        rows.append(dict(zip(headers, row)))

    print("表格数据:")
    for row in rows:
        print(f"  {row}")


def demo_nested_traversal():
    """演示嵌套结构遍历。"""
    print("\n--- 4. 嵌套结构遍历 ---")
    soup = BeautifulSoup(SAMPLE_HTML, "html.parser")

    articles = soup.select("article.post")
    print(f"共 {len(articles)} 篇文章:")

    for article in articles:
        data_id = article.get("data-id")
        title = article.find("h2").text
        summary = article.find("p", class_="summary").text
        tags = [tag.text for tag in article.select("span.tag")]
        print(f"  [{data_id}] {title}")
        print(f"      摘要: {summary}")
        print(f"      标签: {', '.join(tags)}")


def demo_text_extraction():
    """演示文本提取技巧。"""
    print("\n--- 5. 文本提取技巧 ---")
    soup = BeautifulSoup(SAMPLE_HTML, "html.parser")

    # get_text() — 获取所有文本（去除标签）
    nav = soup.find("nav")
    print(f"导航文本（原始）: {repr(nav.get_text())}")
    print(f"导航文本（清理）: {nav.get_text(separator=' | ', strip=True)}")

    # .string vs .text
    h1 = soup.find("h1")
    print(f"h1.string: {h1.string}")  # 直接文本
    print(f"h1.text: {h1.text}")      # 等同于 get_text()

    # 提取所有链接
    print("所有链接:")
    for a in soup.find_all("a", href=True):
        print(f"  {a['href']} -> {a.text.strip()}")


def main():
    """主函数。"""
    print("=" * 60)
    print("  BeautifulSoup HTML 解析演示")
    print("  使用内嵌 HTML，不依赖外部网站")
    print("=" * 60)

    demo_basic_find()
    demo_css_selectors()
    demo_table_extraction()
    demo_nested_traversal()
    demo_text_extraction()

    print("\n✅ 所有解析演示完成！")


if __name__ == "__main__":
    main()
