#!/usr/bin/env python3
"""
数据采集模块

模块: 05-crawler（爬虫）
知识点: 完整爬虫项目
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python crawler.py

描述:
    完整爬虫项目的入口。使用内嵌 HTML 模拟网页数据，
    演示 采集 → 清洗 → 存储 的完整流程。
"""

import logging
import time
from bs4 import BeautifulSoup

from cleaner import DataCleaner
from storage import DataStorage

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# 内嵌 HTML 模拟数据（替代真实网站）
# ---------------------------------------------------------------------------
MOCK_PAGES = [
    """
    <html><body>
    <div class="article-list">
        <div class="article" data-id="1">
            <h2 class="title">  Python 入门指南  </h2>
            <span class="author">张三</span>
            <span class="views">1520</span>
            <span class="date">2025-01-15</span>
            <div class="tags"><span>Python</span><span>入门</span></div>
        </div>
        <div class="article" data-id="2">
            <h2 class="title">爬虫实战教程</h2>
            <span class="author">李四</span>
            <span class="views">2340</span>
            <span class="date">2025-02-20</span>
            <div class="tags"><span>爬虫</span><span>实战</span></div>
        </div>
        <div class="article" data-id="3">
            <h2 class="title">数据分析基础</h2>
            <span class="author">王五</span>
            <span class="views">890</span>
            <span class="date">2025-03-10</span>
            <div class="tags"><span>数据</span><span>Pandas</span></div>
        </div>
    </div>
    </body></html>
    """,
    """
    <html><body>
    <div class="article-list">
        <div class="article" data-id="4">
            <h2 class="title">Web 开发入门</h2>
            <span class="author">赵六</span>
            <span class="views">1100</span>
            <span class="date">2025-04-05</span>
            <div class="tags"><span>Web</span><span>Flask</span></div>
        </div>
        <div class="article" data-id="5">
            <h2 class="title">Python 高级技巧</h2>
            <span class="author">孙七</span>
            <span class="views">3100</span>
            <span class="date">2025-05-12</span>
            <div class="tags"><span>Python</span><span>进阶</span></div>
        </div>
        <div class="article" data-id="2">
            <h2 class="title">爬虫实战教程</h2>
            <span class="author">李四</span>
            <span class="views">2340</span>
            <span class="date">2025-02-20</span>
            <div class="tags"><span>爬虫</span><span>实战</span></div>
        </div>
    </div>
    </body></html>
    """,
    """
    <html><body>
    <div class="article-list">
        <div class="article" data-id="6">
            <h2 class="title">深度学习实战</h2>
            <span class="author">周八</span>
            <span class="views">5200</span>
            <span class="date">2025-06-01</span>
            <div class="tags"><span>AI</span><span>深度学习</span></div>
        </div>
        <div class="article" data-id="7">
            <h2 class="title">爬虫框架对比</h2>
            <span class="author">吴九</span>
            <span class="views">2800</span>
            <span class="date">2025-06-15</span>
            <div class="tags"><span>Scrapy</span><span>爬虫</span></div>
        </div>
        <div class="article" data-id="8">
            <h2 class="title"></h2>
            <span class="author"></span>
            <span class="views">abc</span>
            <span class="date">invalid</span>
            <div class="tags"></div>
        </div>
    </div>
    </body></html>
    """,
]


class ArticleCrawler:
    """文章采集器。"""

    def __init__(self):
        self.raw_articles: list[dict] = []

    def crawl_page(self, html: str, page_num: int) -> list[dict]:
        """解析单个页面，提取文章数据。"""
        articles = []
        try:
            soup = BeautifulSoup(html, "html.parser")
            for article_tag in soup.select("div.article"):
                article = {
                    "id": article_tag.get("data-id", ""),
                    "title": article_tag.select_one(".title").get_text(strip=True),
                    "author": article_tag.select_one(".author").get_text(strip=True),
                    "views": article_tag.select_one(".views").get_text(strip=True),
                    "date": article_tag.select_one(".date").get_text(strip=True),
                    "tags": [t.text.strip() for t in article_tag.select(".tags span")],
                }
                articles.append(article)
            logger.info(f"第 {page_num} 页: 提取到 {len(articles)} 篇文章")
        except Exception as e:
            logger.error(f"第 {page_num} 页解析失败: {e}")
        return articles

    def crawl_all(self, pages: list[str]) -> list[dict]:
        """采集所有页面。"""
        logger.info(f"开始采集，共 {len(pages)} 个页面")
        for i, page_html in enumerate(pages, 1):
            articles = self.crawl_page(page_html, i)
            self.raw_articles.extend(articles)
            time.sleep(0.1)  # 模拟请求间隔
        logger.info(f"采集完成，共 {len(self.raw_articles)} 条原始数据")
        return self.raw_articles


def main():
    """主函数：运行完整的采集 → 清洗 → 存储流程。"""
    print("=" * 60)
    print("  文章采集系统（完整爬虫项目演示）")
    print("  使用内嵌 HTML 模拟，不依赖外部网站")
    print("=" * 60)

    # 1. 数据采集
    crawler = ArticleCrawler()
    raw_data = crawler.crawl_all(MOCK_PAGES)

    # 2. 数据清洗
    cleaner = DataCleaner()
    clean_data = cleaner.clean(raw_data)

    # 3. 数据存储
    storage = DataStorage()
    storage.save_all(clean_data)

    # 4. 查询验证
    storage.query_top_articles(n=3)

    print("\n✅ 完整爬虫流程执行完毕！")


if __name__ == "__main__":
    main()
