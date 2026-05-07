#!/usr/bin/env python3
"""
Scrapy 框架概念演示

模块: 05-crawler（爬虫）
知识点: Scrapy 框架入门
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python scrapy_intro.py

描述:
    演示 Scrapy 的核心概念：Spider、Item、Pipeline。
    使用纯 Python 模拟 Scrapy 的工作流程，帮助理解架构思想。
    无需创建完整 Scrapy 项目即可学习核心概念。
"""

import json
import logging
from dataclasses import dataclass, field, asdict
from typing import Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ===========================================================================
# 1. Item — 定义数据结构（类似 Scrapy 的 scrapy.Item）
# ===========================================================================
@dataclass
class ArticleItem:
    """
    文章数据项。

    在 Scrapy 中对应:
        class ArticleItem(scrapy.Item):
            title = scrapy.Field()
            url = scrapy.Field()
            author = scrapy.Field()
            tags = scrapy.Field()
    """
    title: str = ""
    url: str = ""
    author: str = ""
    tags: list[str] = field(default_factory=list)


# ===========================================================================
# 2. Spider — 定义爬取逻辑（类似 Scrapy 的 scrapy.Spider）
# ===========================================================================
class ArticleSpider:
    """
    文章爬虫。

    在 Scrapy 中对应:
        class ArticleSpider(scrapy.Spider):
            name = "articles"
            start_urls = ["http://example.com/articles"]

            def parse(self, response):
                for article in response.css("article"):
                    item = ArticleItem()
                    item["title"] = article.css("h2::text").get()
                    item["url"] = article.css("a::attr(href)").get()
                    yield item
    """
    name = "articles"
    start_urls = ["http://example.com/articles"]

    # 模拟 HTML 响应
    MOCK_HTML = """
    <div class="article-list">
        <article>
            <h2>Python 爬虫入门</h2>
            <a href="/post/1">阅读全文</a>
            <span class="author">张三</span>
            <span class="tag">Python</span>
            <span class="tag">爬虫</span>
        </article>
        <article>
            <h2>Scrapy 框架实战</h2>
            <a href="/post/2">阅读全文</a>
            <span class="author">李四</span>
            <span class="tag">Scrapy</span>
        </article>
        <article>
            <h2>数据清洗技巧</h2>
            <a href="/post/3">阅读全文</a>
            <span class="author">王五</span>
            <span class="tag">数据处理</span>
            <span class="tag">Pandas</span>
        </article>
    </div>
    """

    def parse(self, html: str):
        """
        解析页面，提取数据。

        在 Scrapy 中，response 是 Scrapy 的 Response 对象，
        这里简化为直接传入 HTML 字符串。
        """
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "html.parser")
        for article in soup.select("article"):
            item = ArticleItem(
                title=article.select_one("h2").text.strip(),
                url=article.select_one("a")["href"],
                author=article.select_one(".author").text.strip(),
                tags=[t.text.strip() for t in article.select(".tag")],
            )
            yield item  # Scrapy 的核心：通过 yield 返回 Item


# ===========================================================================
# 3. Pipeline — 数据处理管道（类似 Scrapy 的 Pipeline）
# ===========================================================================
class CleanPipeline:
    """
    数据清洗管道。

    在 Scrapy 中对应 settings.py:
        ITEM_PIPELINES = {
            'myproject.pipelines.CleanPipeline': 300,
            'myproject.pipelines.StoragePipeline': 400,
        }
    """

    def process_item(self, item: ArticleItem) -> ArticleItem | None:
        """清洗数据：去除空白、验证必填字段。"""
        if not item.title:
            logger.warning(f"丢弃无标题的 Item: {item}")
            return None  # Scrapy 中用 raise DropItem()
        item.title = item.title.strip()
        item.author = item.author.strip() or "未知"
        return item


class StoragePipeline:
    """数据存储管道。"""

    def __init__(self):
        self.items: list[dict[str, Any]] = []

    def process_item(self, item: ArticleItem) -> ArticleItem:
        """存储数据。"""
        self.items.append(asdict(item))
        return item

    def close_spider(self):
        """爬虫结束时的清理工作。"""
        logger.info(f"共存储 {len(self.items)} 条数据")
        return self.items


# ===========================================================================
# 4. 模拟 Scrapy Engine 的工作流程
# ===========================================================================
def simulate_scrapy_workflow():
    """模拟 Scrapy 的完整工作流程。"""
    logger.info("--- 模拟 Scrapy 工作流程 ---")

    # 初始化组件
    spider = ArticleSpider()
    clean_pipeline = CleanPipeline()
    storage_pipeline = StoragePipeline()

    logger.info(f"Spider: {spider.name}")
    logger.info(f"Start URLs: {spider.start_urls}")

    # 模拟 Engine 调度流程
    # 1. Engine 从 Spider 获取 start_urls
    # 2. Engine 将 URL 交给 Downloader 下载
    # 3. Downloader 返回 Response 给 Engine
    # 4. Engine 将 Response 交给 Spider.parse() 处理
    # 5. Spider yield Item 给 Engine
    # 6. Engine 将 Item 交给 Pipeline 处理

    logger.info("\n[Step 1] Spider.parse() 提取数据:")
    for item in spider.parse(spider.MOCK_HTML):
        logger.info(f"  提取: {item.title} by {item.author}")

        # Pipeline 链式处理
        cleaned = clean_pipeline.process_item(item)
        if cleaned:
            storage_pipeline.process_item(cleaned)

    # 爬虫结束
    logger.info("\n[Step 2] Pipeline 存储结果:")
    results = storage_pipeline.close_spider()
    print(json.dumps(results, ensure_ascii=False, indent=2))


def show_scrapy_project_structure():
    """展示标准 Scrapy 项目结构。"""
    logger.info("\n--- 标准 Scrapy 项目结构 ---")
    structure = """
    myspider/
    ├── scrapy.cfg              # 部署配置
    └── myspider/
        ├── __init__.py
        ├── items.py            # 数据结构定义
        ├── middlewares.py      # 中间件
        ├── pipelines.py        # 数据管道
        ├── settings.py         # 项目设置
        └── spiders/            # 爬虫目录
            ├── __init__.py
            └── article_spider.py
    """
    print(structure)

    logger.info("常用 Scrapy 命令:")
    commands = [
        ("scrapy startproject myspider", "创建项目"),
        ("scrapy genspider example example.com", "创建爬虫"),
        ("scrapy crawl example", "运行爬虫"),
        ("scrapy crawl example -o data.json", "运行并导出 JSON"),
        ("scrapy shell 'http://example.com'", "交互式调试"),
    ]
    for cmd, desc in commands:
        logger.info(f"  {cmd:45s} # {desc}")


def main():
    """主函数。"""
    print("=" * 60)
    print("  Scrapy 框架概念演示")
    print("  模拟 Spider → Pipeline 工作流程")
    print("=" * 60)

    simulate_scrapy_workflow()
    show_scrapy_project_structure()

    print("\n✅ Scrapy 概念演示完成！")


if __name__ == "__main__":
    main()
