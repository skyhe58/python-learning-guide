#!/usr/bin/env python3
"""
爬虫数据存储演示

模块: 05-crawler（爬虫）
知识点: 数据存储
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python storage_demo.py

描述:
    演示爬虫数据的三种常见存储方式：JSON、CSV、SQLite。
    使用模拟数据，无需外部依赖。
"""

import csv
import json
import logging
import os
import sqlite3
import tempfile
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# 模拟爬取到的数据
CRAWLED_DATA = [
    {"id": 1, "title": "Python 入门指南", "author": "张三", "views": 1520, "tags": ["Python", "入门"]},
    {"id": 2, "title": "爬虫实战教程", "author": "李四", "views": 2340, "tags": ["爬虫", "实战"]},
    {"id": 3, "title": "数据分析基础", "author": "王五", "views": 890, "tags": ["数据", "分析"]},
    {"id": 4, "title": "Web 开发入门", "author": "赵六", "views": 1100, "tags": ["Web", "Flask"]},
    {"id": 5, "title": "机器学习概览", "author": "孙七", "views": 3200, "tags": ["AI", "ML"]},
]


def demo_json_storage(output_dir: str):
    """演示 JSON 文件存储。"""
    logger.info("--- 1. JSON 文件存储 ---")
    filepath = os.path.join(output_dir, "articles.json")

    # 写入 JSON
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(CRAWLED_DATA, f, ensure_ascii=False, indent=2)
    logger.info(f"已保存 {len(CRAWLED_DATA)} 条数据到 {filepath}")

    # 读取 JSON
    with open(filepath, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    logger.info(f"读取验证: {len(loaded)} 条数据")

    # 逐行写入 JSON Lines 格式（适合大数据量追加）
    jsonl_path = os.path.join(output_dir, "articles.jsonl")
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for item in CRAWLED_DATA:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    logger.info(f"JSON Lines 格式已保存到 {jsonl_path}")


def demo_csv_storage(output_dir: str):
    """演示 CSV 文件存储。"""
    logger.info("\n--- 2. CSV 文件存储 ---")
    filepath = os.path.join(output_dir, "articles.csv")

    # 写入 CSV（utf-8-sig 编码兼容 Excel）
    fieldnames = ["id", "title", "author", "views", "tags"]
    with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in CRAWLED_DATA:
            row = {**item, "tags": "|".join(item["tags"])}  # 列表转字符串
            writer.writerow(row)
    logger.info(f"已保存 {len(CRAWLED_DATA)} 条数据到 {filepath}")

    # 读取 CSV
    with open(filepath, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    logger.info(f"读取验证: {len(rows)} 条数据")
    logger.info(f"  示例: {rows[0]['title']} by {rows[0]['author']}")


def demo_sqlite_storage(output_dir: str):
    """演示 SQLite 数据库存储。"""
    logger.info("\n--- 3. SQLite 数据库存储 ---")
    db_path = os.path.join(output_dir, "articles.db")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # 创建表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT,
                views INTEGER DEFAULT 0,
                tags TEXT
            )
        """)

        # 插入数据（使用参数化查询防止 SQL 注入）
        for item in CRAWLED_DATA:
            cursor.execute(
                "INSERT OR REPLACE INTO articles (id, title, author, views, tags) VALUES (?, ?, ?, ?, ?)",
                (item["id"], item["title"], item["author"], item["views"], "|".join(item["tags"])),
            )
        conn.commit()
        logger.info(f"已保存 {len(CRAWLED_DATA)} 条数据到 {db_path}")

        # 查询数据
        cursor.execute("SELECT COUNT(*) FROM articles")
        count = cursor.fetchone()[0]
        logger.info(f"数据库中共 {count} 条记录")

        # 条件查询
        cursor.execute("SELECT title, views FROM articles WHERE views > 1000 ORDER BY views DESC")
        popular = cursor.fetchall()
        logger.info(f"浏览量 > 1000 的文章 ({len(popular)} 篇):")
        for title, views in popular:
            logger.info(f"  {title}: {views} 次浏览")

    finally:
        conn.close()


def main():
    """主函数。"""
    print("=" * 60)
    print("  爬虫数据存储演示")
    print("  JSON / CSV / SQLite 三种方式")
    print("=" * 60)

    # 使用临时目录存储演示文件
    with tempfile.TemporaryDirectory(prefix="crawler_storage_") as tmpdir:
        logger.info(f"临时目录: {tmpdir}\n")

        demo_json_storage(tmpdir)
        demo_csv_storage(tmpdir)
        demo_sqlite_storage(tmpdir)

        # 列出生成的文件
        logger.info("\n--- 生成的文件 ---")
        for f in sorted(Path(tmpdir).iterdir()):
            size = f.stat().st_size
            logger.info(f"  {f.name}: {size} bytes")

    print("\n✅ 数据存储演示完成！（临时文件已清理）")


if __name__ == "__main__":
    main()
