#!/usr/bin/env python3
"""
数据存储模块

模块: 05-crawler（爬虫）
知识点: 完整爬虫项目 - 数据存储
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    由 crawler.py 调用

描述:
    将清洗后的数据存储到 JSON 文件和 SQLite 数据库。
"""

import json
import logging
import os
import sqlite3
import tempfile

logger = logging.getLogger(__name__)


class DataStorage:
    """数据存储器：支持 JSON 和 SQLite 双重存储。"""

    def __init__(self, output_dir: str | None = None):
        self.output_dir = output_dir or tempfile.mkdtemp(prefix="crawler_output_")
        self.db_path = os.path.join(self.output_dir, "articles.db")
        self.json_path = os.path.join(self.output_dir, "articles.json")
        logger.info(f"存储目录: {self.output_dir}")

    def save_all(self, data: list[dict]):
        """同时保存到 JSON 和 SQLite。"""
        self.save_json(data)
        self.save_sqlite(data)

    def save_json(self, data: list[dict]):
        """保存到 JSON 文件。"""
        try:
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"[JSON] 已保存 {len(data)} 条数据到 {self.json_path}")
        except IOError as e:
            logger.error(f"[JSON] 保存失败: {e}")

    def save_sqlite(self, data: list[dict]):
        """保存到 SQLite 数据库。"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    author TEXT DEFAULT '未知',
                    views INTEGER DEFAULT 0,
                    date TEXT,
                    tags TEXT
                )
            """)

            for item in data:
                cursor.execute(
                    "INSERT OR REPLACE INTO articles (id, title, author, views, date, tags) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        item["id"],
                        item["title"],
                        item["author"],
                        item["views"],
                        item["date"],
                        "|".join(item.get("tags", [])),
                    ),
                )

            conn.commit()
            logger.info(f"[SQLite] 已保存 {len(data)} 条数据到 {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"[SQLite] 保存失败: {e}")
        finally:
            conn.close()

    def query_top_articles(self, n: int = 5):
        """查询浏览量最高的文章。"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT title, author, views FROM articles ORDER BY views DESC LIMIT ?",
                (n,),
            )
            results = cursor.fetchall()
            logger.info(f"\n浏览量 Top {n} 文章:")
            for i, (title, author, views) in enumerate(results, 1):
                logger.info(f"  {i}. {title} by {author} ({views} views)")
            conn.close()
        except sqlite3.Error as e:
            logger.error(f"查询失败: {e}")


if __name__ == "__main__":
    # 单独测试存储模块
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    test_data = [
        {"id": 1, "title": "测试文章1", "author": "作者A", "views": 100, "date": "2025-01-01", "tags": ["Python"]},
        {"id": 2, "title": "测试文章2", "author": "作者B", "views": 200, "date": "2025-02-01", "tags": ["爬虫"]},
    ]
    storage = DataStorage()
    storage.save_all(test_data)
    storage.query_top_articles()
