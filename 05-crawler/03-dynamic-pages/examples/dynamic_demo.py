#!/usr/bin/env python3
"""
动态页面爬取演示

模块: 05-crawler（爬虫）
知识点: 动态页面处理
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python dynamic_demo.py

描述:
    演示处理动态页面的两种思路：
    1. Selenium/Playwright 浏览器自动化（概念说明，需安装驱动）
    2. 分析 API 接口直接请求（可运行的替代方案）
    使用本地模拟服务器，不依赖外部网站。
"""

import json
import logging
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from urllib.parse import urlparse, parse_qs

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# 模拟动态页面的 API 服务器
# ---------------------------------------------------------------------------
MOCK_ARTICLES = [
    {"id": i, "title": f"文章 {i}", "content": f"这是第 {i} 篇文章的内容"}
    for i in range(1, 16)
]


class DynamicAPIHandler(BaseHTTPRequestHandler):
    """模拟前后端分离的 API 服务。"""

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        if parsed.path == "/api/articles":
            # 模拟分页 API
            page = int(params.get("page", [1])[0])
            size = int(params.get("size", [5])[0])
            start = (page - 1) * size
            end = start + size
            data = {
                "code": 200,
                "data": MOCK_ARTICLES[start:end],
                "total": len(MOCK_ARTICLES),
                "page": page,
                "pages": (len(MOCK_ARTICLES) + size - 1) // size,
            }
            self._send_json(200, data)
        elif parsed.path == "/api/search":
            keyword = params.get("q", [""])[0]
            results = [a for a in MOCK_ARTICLES if keyword in a["title"]]
            self._send_json(200, {"results": results, "count": len(results)})
        elif parsed.path == "/page":
            # 模拟一个 SPA 页面（HTML 中无数据，数据由 JS 加载）
            html = """<!DOCTYPE html>
<html><body>
<div id="app">加载中...</div>
<script>
// 实际网站中，这里会通过 fetch('/api/articles') 加载数据
// 然后动态渲染到 #app 中
</script>
</body></html>"""
            self._send_html(html)
        else:
            self._send_json(404, {"error": "Not Found"})

    def _send_json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html):
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)


def start_server(port=18081):
    server = HTTPServer(("127.0.0.1", port), DynamicAPIHandler)
    Thread(target=server.serve_forever, daemon=True).start()
    logger.info(f"模拟 API 服务器已启动: http://127.0.0.1:{port}")
    return server


# ---------------------------------------------------------------------------
# Selenium 概念说明（注释形式，需要安装浏览器驱动才能运行）
# ---------------------------------------------------------------------------
def selenium_concept():
    """
    Selenium 使用示例（概念说明，不实际运行）。

    安装:
        pip install selenium
        # 还需要下载对应浏览器的 WebDriver

    代码示例:
    ```python
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    # 创建浏览器实例（无头模式）
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        # 访问页面
        driver.get("http://example.com/spa-page")

        # 显式等待：等待元素出现（最多 10 秒）
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".article-list"))
        )

        # 提取数据
        articles = driver.find_elements(By.CSS_SELECTOR, ".article-item")
        for article in articles:
            title = article.find_element(By.TAG_NAME, "h2").text
            print(title)
    finally:
        driver.quit()
    ```
    """
    logger.info("[Selenium 概念] 需要安装浏览器驱动，此处仅展示概念")
    logger.info("  安装: pip install selenium")
    logger.info("  核心: webdriver.Chrome() → driver.get(url) → find_elements()")


# ---------------------------------------------------------------------------
# Playwright 概念说明
# ---------------------------------------------------------------------------
def playwright_concept():
    """
    Playwright 使用示例（概念说明，不实际运行）。

    安装:
        pip install playwright
        playwright install  # 自动下载浏览器

    代码示例:
    ```python
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("http://example.com/spa-page")

        # Playwright 内置自动等待
        page.wait_for_selector(".article-list")

        # 提取数据
        articles = page.query_selector_all(".article-item")
        for article in articles:
            title = article.query_selector("h2").inner_text()
            print(title)

        browser.close()
    ```
    """
    logger.info("[Playwright 概念] 需要安装浏览器，此处仅展示概念")
    logger.info("  安装: pip install playwright && playwright install")
    logger.info("  核心: sync_playwright() → page.goto() → query_selector_all()")


# ---------------------------------------------------------------------------
# 可运行的替代方案：直接请求 API
# ---------------------------------------------------------------------------
def demo_api_analysis():
    """演示分析 API 接口直接获取数据（推荐方法）。"""
    import requests

    logger.info("--- API 分析法（推荐）---")
    logger.info("思路: 用浏览器 F12 找到数据接口，直接用 requests 请求")

    base = "http://127.0.0.1:18081"

    # 1. 直接请求 API 获取数据
    try:
        resp = requests.get(f"{base}/api/articles", params={"page": 1, "size": 5}, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        logger.info(f"第 1 页数据 (共 {data['total']} 条, {data['pages']} 页):")
        for article in data["data"]:
            logger.info(f"  [{article['id']}] {article['title']}")
    except requests.exceptions.RequestException as e:
        logger.error(f"请求失败: {e}")

    # 2. 自动翻页获取所有数据
    logger.info("\n--- 自动翻页 ---")
    all_articles = []
    page = 1
    while True:
        try:
            resp = requests.get(
                f"{base}/api/articles",
                params={"page": page, "size": 5},
                timeout=5,
            )
            resp.raise_for_status()
            data = resp.json()
            all_articles.extend(data["data"])
            logger.info(f"第 {page}/{data['pages']} 页: 获取 {len(data['data'])} 条")
            if page >= data["pages"]:
                break
            page += 1
            time.sleep(0.5)  # 请求频率控制
        except requests.exceptions.RequestException as e:
            logger.error(f"第 {page} 页请求失败: {e}")
            break

    logger.info(f"共获取 {len(all_articles)} 条数据")

    # 3. 搜索接口
    logger.info("\n--- 搜索接口 ---")
    try:
        resp = requests.get(f"{base}/api/search", params={"q": "文章 1"}, timeout=5)
        results = resp.json()
        logger.info(f"搜索 '文章 1': 找到 {results['count']} 条结果")
    except requests.exceptions.RequestException as e:
        logger.error(f"搜索失败: {e}")


def main():
    """主函数。"""
    print("=" * 60)
    print("  动态页面爬取演示")
    print("  推荐优先分析 API 接口，浏览器自动化为备选")
    print("=" * 60)

    server = start_server(port=18081)

    try:
        selenium_concept()
        print()
        playwright_concept()
        print()
        demo_api_analysis()
    finally:
        server.shutdown()

    print("\n✅ 演示完成！")


if __name__ == "__main__":
    main()
